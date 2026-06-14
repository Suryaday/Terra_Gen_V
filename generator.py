from __future__ import annotations

import logging
import os
import re
import textwrap
import hashlib

from collections import defaultdict, deque, Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from collections import OrderedDict
from collections import defaultdict

from openai import OpenAI
from dotenv import load_dotenv

from auto_dependency_map import RESOURCE_DEPENDENCIES

from dependency_expander import expand_entities
from architecture_expander import extract_architecture
from architecture_expander import complete_architecture
from architecture_validator import validate_entities
from query_corrector import QueryCorrector
from hybrid_retriever import hybrid_retrieve
from bm25_search import BM25Engine

from retrieval_types import RetrievalResult

from context_builder import build_xml_context

import schema_index
from schema_normalizer import normalize_block_vs_argument
from schema_index import (find_argument_type, find_argument_type_by_path, block_object_type)
from schema_typing import terraform_type_to_hcl
from schema_validator import validate_resource
from schema_index import print_conflict_summary

###########################################################################################################

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

INDEX_FILE = Path("vectorstore/bm25.pkl").resolve()

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2048"))

SCHEMA_FINDING_COUNTS = Counter()

_client: Optional[OpenAI] = None

RESOURCE_ALIASES = {
    "aws_alb": "aws_lb",
    "aws_alb_listener": "aws_lb_listener",
    "aws_alb_target_group": "aws_lb_target_group",
}

PLANNER_NAME_ALIASES = {

    "aws_rds_db_instance":
        "aws_db_instance",

    "aws_rds_db_subnet_group":
        "aws_db_subnet_group",
}

ARGUMENT_ALIASES = {
    "aws_db_instance": {
        "name": "db_name",
    },
    "aws_ecs_task_definition": {
        "size_in_gb": "size_in_gib",
    },
    "aws_sqs_queue": {
        "maximum_message_size": "max_message_size",
    },
    "aws_ecs_cluster": {
        "cloudwatch_log_group_name": "cloud_watch_log_group_name"
    }
}

ATTRIBUTE_ALIASES = {

    ("aws_key_pair", "name"): "key_name",

}

# ======================================================
# TYPES
# ======================================================

@dataclass
class ResourceNode:
    entity: str
    label: str          # Terraform resource label, e.g. "main"
    is_root: bool       # True = user explicitly requested this resource
    hard_deps: list[str] = field(default_factory=list)

@dataclass
class GenerationPlan:
    query: str
    root_entities: list[str]
    ordered_nodes: list[ResourceNode]   # topologically sorted: deps first

@dataclass
class GeneratedBlock:
    entity: str
    label: str
    hcl: str                            # raw HCL for this resource block
    var_refs: list[str]                 # var.xxx names extracted from HCL
    var_sources: dict[str, tuple[str, str]]

@dataclass
class GenerationResult:
    query: str
    plan: GenerationPlan
    files: dict[str, str]               # filename → content
    warnings: list[str]

@dataclass
class RetrievalBundle:
    primary_chunks: list
    architecture_chunks: list
    dependency_chunks: list
    example_chunks: list

@dataclass
class GenerationState:

    naming_prefix: str
    environment: str
    tags: dict[str, str]
    generated_resources: dict[str, str]

# ======================================================
# SECTION PRIORITY (matches hybrid_retriever)
# ======================================================

SECTION_PRIORITY = {
    "argument reference": 0,
    "example usage":      1,
    "basic usage":        2,
    "overview":           50,
}

# P1 FIX: minimum number of argument-reference chunks every TARGET resource
# must receive, regardless of what the global retriever returned. Resources
# the retriever only partially found used to be frozen with as little as a
# single argument-reference chunk, producing incomplete schema and
# `terraform validate` failures. See assemble_context().
ARGREF_FLOOR = 6


# ======================================================
# ENGINE SETUP (lazy-loaded singletons)
# ======================================================

_bm25: Optional[BM25Engine] = None
_corrector: Optional[QueryCorrector] = None
_known_entities: Optional[set[str]] = None

def _get_bm25() -> BM25Engine:

    global _bm25

    if _bm25 is None:

        _bm25 = BM25Engine(INDEX_FILE)
        _bm25._load()

    return _bm25

def retrieve_generation_context(query: str,):

    rows = hybrid_retrieve(query, k=24)

    for row in rows[:20]:
        logger.info("GLOBAL | %s | metadata_id=%s | dependency=%s", row.chunk_id, id(row.metadata), row.metadata.get("_dependency"))

    logger.info("Global retrieval returned " f"{len(rows)} rows")

    logger.info("RETRIEVED ENTITY COUNTS=%s", Counter(r.metadata.get("entity") for r in rows))

    return rows

#6th June
def _family_from_text(text: str) -> str:
    for line in text.splitlines():
        s = line.strip()

        if s.startswith("### "):
            return s[4:].split()[0]

    return ""

#30 MAY
def retrieve_entity_rows(entity: str, bm25, k: int = 4) -> list[RetrievalResult]:
    """
    Direct metadata scan sorted by SECTION_PRIORITY.
    Guarantees argument_reference comes before example_usage comes before overview.
    Never uses BM25 scoring — entity is exact, section priority is deterministic.
    """
    candidates = [
        row for row in bm25._metadata
        if row["metadata"].get("entity") == entity
        and row["metadata"].get("doc_type") == "resource"
    ]

    logger.info("%s total_candidates=%s", entity, len(candidates))
    for row in candidates[:10]:
        logger.info(
            "CHUNK=%s",
            row["text"][:250]
        )
    
    candidates.sort(
        key=lambda r: (
            SECTION_PRIORITY.get(r["metadata"].get("section", "").lower(), 50),
        )
    )

    argref = [
        r
        for r in candidates
        if r["metadata"].get("section", "").lower()
        == "argument reference"
    ]

    other = [
        r
        for r in candidates
        if r["metadata"].get("section", "").lower()
        != "argument reference"
    ]

    buckets = OrderedDict()

    for row in argref:

        family = _family_from_text(row["text"])
        logger.info("BALANCED ORDER | %s | %s", _family_from_text(row["text"]), row["chunk_id"])

        buckets.setdefault(family, []).append(row)

    ordered_families = []

    if "" in buckets:
        ordered_families.append("")

    ordered_families.extend(
        family
        for family in buckets
        if family != ""
    )

    interleaved = []

    while any(buckets.values()):

        for family in ordered_families:

            if buckets[family]:
                interleaved.append(
                    buckets[family].pop(0)
                )

    candidates = interleaved + other
    
    for row in candidates[:10]:

        logger.info(
            "BALANCED ORDER | %s | %s",
            _family_from_text(row["text"]),
            row["chunk_id"],
        )

    return [
        RetrievalResult(
            chunk_id=r["chunk_id"],
            text=r["text"],
            metadata=r["metadata"],
        )
        for r in candidates[:k]
    ]

def filter_rows_for_resource(rows, entity: str, hard_deps: list[str]):

#30 May
    logger.info("FILTER INPUT entity=%s rows=%s", entity, len(rows))
     
    allowed = set([entity] + hard_deps)

    logger.info("ALLOWED ENTITIES=%s", sorted(allowed))

    filtered = []

    for row in rows:

        row_entity = (row.metadata.get("entity"))

        if row_entity in allowed:

            filtered.append(row)

    logger.info("FILTER OUTPUT entity=%s rows=%s", entity, len(filtered))
    return filtered

def _get_corrector() -> QueryCorrector:

    global _corrector, _known_entities
    
    if _corrector is None:
        bm25 = _get_bm25()
        _corrector = QueryCorrector(bm25._metadata)
        _known_entities = {
            row["metadata"].get("entity")
            for row in bm25._metadata
            if row["metadata"].get("entity")
            and row["metadata"].get("doc_type") == "resource"
        }
    return _corrector

def _get_known_entities() -> set[str]:
    _get_corrector()
    return _known_entities

def remove_conflicting_entities(entities: list[str], query: str) -> list[str]:

    q = query.lower()

    ecs_present = (
        "aws_ecs_service" in entities
        or
        "aws_ecs_cluster" in entities
    )

    ec2_intent = any(
        signal in q
        for signal in (
            "ec2",
            "capacity provider",
            "managed instance",
            "managed instances",
            "launch template",
            "autoscaling group",
            "asg",
        )
    )

    if ecs_present and not ec2_intent:

        forbidden = {
            "aws_ecs_capacity_provider",
            "aws_launch_template",
            "aws_autoscaling_group",
            "aws_autoscaling_attachment",
            "aws_autoscaling_policy",
            "aws_iam_instance_profile",
        }

        removed = forbidden & set(entities)

        entities = [e for e in entities if e not in forbidden]

        if removed:
            logger.info("REMOVED ECS/EC2 CONFLICT ENTITIES=%s", sorted(removed))

    ec2_autoscaling_present = (
            "aws_autoscaling_group" in entities
            or
            "aws_launch_template" in entities
        )

    ecs_intent = any(
            signal in q
            for signal in (
                "ecs",
                "fargate",
                "capacity provider",
                "ecs service",
                "ecs cluster",
            )
        )
    
    scaling_policy_intent = any(
        s in q
        for s in (
            "scaling policy",
            "scale out",
            "scale in",
            "scale up",
            "scale down",
            "target tracking",
            "step scaling",
            "cpu utilization",
            "scaling adjustment",
        )
    )

    if ec2_autoscaling_present and not ecs_intent:

            forbidden = {
                "aws_appautoscaling_target",
                "aws_appautoscaling_policy",
            }

            removed = forbidden & set(entities)

            entities = [e for e in entities if e not in forbidden]

            if removed:
                logger.info(
                    "REMOVED EC2/ECS AUTOSCALING CONFLICT ENTITIES=%s",
                    sorted(removed)
                )      

    if ec2_autoscaling_present and not scaling_policy_intent:

        forbidden = {
            "aws_autoscaling_policy",
            "aws_autoscaling_attachment",
        }

        removed = forbidden & set(entities)

        entities = [e for e in entities if e not in forbidden]

        if removed:
            logger.info(
                "REMOVED UNREQUESTED AUTOSCALING POLICY=%s",
                sorted(removed)
            )  
    
    if "aws_dynamodb_table" in entities:

        if "aws_dynamodb_global_secondary_index" in entities:

            entities = [
                e
                for e in entities
                if e != "aws_dynamodb_global_secondary_index"
            ]

            logger.info(
                "REMOVED DYNAMODB INLINE/STANDALONE CONFLICT=%s",
                ["aws_dynamodb_global_secondary_index"]
            )
        
    return entities

def _get_client() -> OpenAI:

    global _client

    if _client is None:

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError("OPENAI_API_KEY missing")

        _client = OpenAI(api_key=api_key)

    return _client

def get_generation_deps(resource: str) -> list[str]:
    """
    Dependencies used for generation ordering.

    Terraform optional dependencies often become required
    when generating a complete architecture because later
    resources should reference earlier resources.

    Generation dependencies = hard + optional.
    """

    deps = RESOURCE_DEPENDENCIES.get(resource, {})

    hard = deps.get("hard", [])
    optional = deps.get("optional", [])

    return list(dict.fromkeys(hard + optional))

def _is_argument_assignment(stripped: str, arg: str) -> bool:
    """
    True when a stripped HCL line assigns `arg`, e.g. 'arg = value'.

    Tolerant of the alignment padding Terraform/LLMs emit:
        volume                   = var.volume

    The trailing '\\s*=' guarantees the name is terminated by '=' (HCL
    identifiers contain neither spaces nor '='), so 'volume' will NOT match
    'volume_configuration =' and 'cidr_block' will NOT match 'cidr_blocks ='.
    """
    return re.match(rf"{re.escape(arg)}\s*=", stripped) is not None


# ======================================================
# TOPOLOGICAL SORT
# ======================================================

def _topo_sort(entities: list[str]) -> list[str]:
    """
    Kahn's algorithm. Returns entities ordered so that every
    dependency comes before the entity that requires it.
    Entities absent from RESOURCE_DEPENDENCIES are placed first.
    """
    entity_set = set(entities)

    # Build adjacency: node → list of nodes it depends on (within entity_set)
    deps_within: dict[str, list[str]] = {}
    for e in entities:
        #known = RESOURCE_DEPENDENCIES.get(e, {})
        #deps_within[e] = [d for d in known.get("hard", []) if d in entity_set]
        logger.info("GEN DEPS %s -> %s", e, get_generation_deps(e))
        deps_within[e] = [d for d in get_generation_deps(e) if d in entity_set]

    # In-degree = number of dependencies within the set
    in_degree = {e: len(deps_within[e]) for e in entities}

    # Reverse map: who depends on me?
    dependents: dict[str, list[str]] = defaultdict(list)
    for e, deps in deps_within.items():
        for dep in deps:
            dependents[dep].append(e)

    # Start with nodes that have no dependencies
    queue = deque(e for e in entities if in_degree[e] == 0)
    result: list[str] = []

    while queue:
        node = queue.popleft()
        result.append(node)
        for dependent in dependents[node]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)

    # Handle cycles (shouldn't occur in Terraform deps, but be safe)
    remaining = [e for e in entities if e not in result]
    if remaining:
        logger.warning("Cycle detected or unresolved deps for: %s", remaining)
        result.extend(remaining)

    return result

def _normalize_rds_parameter_blocks(entity: str, hcl: str) -> str:

    if entity != "aws_rds_cluster_parameter_group":
        return hcl

    lines = hcl.splitlines()

    output = []

    skip = False
    depth = 0
    skip_depth = 0

    for line in lines:

        stripped = line.strip()

        if (
            not skip
            and stripped.startswith("parameter {")
        ):
            logger.info(
                "REMOVED invalid parameter block"
            )

            skip = True
            skip_depth = depth

            depth += line.count("{")
            depth -= line.count("}")

            continue

        if skip:

            depth += line.count("{")
            depth -= line.count("}")

            if depth <= skip_depth:
                skip = False

            continue

        output.append(line)

        depth += line.count("{")
        depth -= line.count("}")

    return "\n".join(output)

def _normalize_cloudfront_required_blocks(entity: str, hcl: str) -> str:

    if entity != "aws_cloudfront_distribution":
        return hcl

    if "viewer_certificate {" in hcl:
        return hcl

    logger.info(
        "INJECTED viewer_certificate block"
    )

    block = """

    viewer_certificate {
        cloudfront_default_certificate = true
    }
    """

    pos = hcl.rfind("}")

    if pos == -1:
        return hcl

    return hcl[:pos] + block + "\n}" + hcl[pos + 1:]

def _normalize_malformed_var_refs(terraform: str) -> str:

    def repl(m):
        old = f"var_{m.group(2)}"
        new = f"var.{m.group(2)}"

        logger.info(
            "NORMALIZED MALFORMED VAR REF %s -> %s",
            old,
            new,
        )

        return f"{m.group(1)}{new}"

    return re.sub(
        r'(?m)^(\s*[A-Za-z0-9_]+\s*=\s*)var_([a-z][a-z0-9_]*)\s*$',
        repl,
        terraform,
    )

# ======================================================
# PLAN BUILDING
# ======================================================

def build_plan(query: str) -> GenerationPlan:
    """
    Extract root entities from the query, expand to full dependency
    closure, topologically sort, and return a GenerationPlan.
    """
    corrector = _get_corrector()
    known = _get_known_entities()

    # Step 1: Normalize query and extract entity hints from INFRA_PHRASES
    clean = corrector.correct(query)
    logger.info("Normalized query: %s", clean)

    # Step 2: Use architecture expander for multi-resource architectural queries
    arch_entities = extract_architecture(clean)

    arch_entities = [PLANNER_NAME_ALIASES.get(e, e) for e in arch_entities]

    arch_entities = [RESOURCE_ALIASES.get(e, e) for e in arch_entities]

    logger.info("PRE VALIDATION=%s", arch_entities)

    valid = validate_entities(arch_entities, known)

    valid = [e for e in valid if schema_index.is_known(e)]

    dropped = set(arch_entities) - set(valid)

    if dropped:
        logger.warning("INVALID ENTITIES DROPPED=%s", sorted(dropped))

    arch_entities = valid

    arch_entities = validate_entities(arch_entities, known)

    logger.info("PRE VALIDATION=%s", arch_entities)

    # Step 3: Also extract entity names directly from the corrected query
    # (any aws_xxx tokens in clean_query are valid entity hints)
    query_entities = [
        tok for tok in re.findall(r"aws_[a-z0-9_]+", clean)
        if tok in known
    ]

    # Combine, deduplicate, keep insertion order
    seen: set[str] = set()
    root_entities: list[str] = []

    for e in arch_entities + query_entities:
        if e not in seen:
            seen.add(e)
            root_entities.append(e)

    logger.info("ROOT BEFORE COMPLETION=%s", root_entities)

    root_entities = complete_architecture(root_entities)

    root_entities = [RESOURCE_ALIASES.get(e, e) for e in root_entities]

    root_entities = validate_entities(root_entities, known)

    root_entities = [e for e in root_entities if schema_index.is_known(e)]

    root_entities = remove_conflicting_entities(root_entities, clean)

    logger.info("ROOT AFTER COMPLETION=%s", root_entities)

    if not root_entities:
        logger.warning("Could not extract any root entities from query: %s", query)
        return GenerationPlan(
            query=query,
            root_entities=[],
            ordered_nodes=[]
        )

    logger.info("Root entities: %s", root_entities)

    # Step 4: Expand to full dependency closure (hard deps only)
    all_entities = expand_entities(root_entities, depth=2, hard_only=True)

    all_entities = [e for e in all_entities if schema_index.is_known(e)]

    all_entities = remove_conflicting_entities(all_entities, clean)

    logger.info("Full entity set after expansion: %s", all_entities)

    # Step 5: Topological sort — dependencies come before dependents
    ordered = _topo_sort(all_entities)
    logger.info("TOPO ORDER=%s", ordered)

    # Step 6: Build ResourceNode list
    used_labels = set()
    root_set = set(root_entities)
    nodes = []

    for e in ordered:

        label = generate_label(e, used_labels)

        used_labels.add(label)

        nodes.append(

            ResourceNode(

                entity=e,

                label=label,

                is_root=(e in root_set),

                #hard_deps=[d for d in RESOURCE_DEPENDENCIES.get(e, {}).get("hard", []) if d in set(all_entities)]

                hard_deps = [d for d in get_generation_deps(e) if d in set(all_entities)]
            )
        )
    
    for node in nodes:
        logger.info("NODE=%s HARD_DEPS=%s", node.entity, node.hard_deps)

    return GenerationPlan(query=query, root_entities=root_entities, ordered_nodes=nodes)

# ======================================================
# DEPENDENCY REFERENCE CONTEXT
# ======================================================

def build_dependency_reference_context(node, symbol_table: dict[str, str],) -> str:

    if not node.hard_deps:
        return ""

    lines = [
        "DEPENDENCY REFERENCES",
        "",
        "Use these generated Terraform resources instead of variables whenever appropriate.",
        "",
    ]

    for dep in node.hard_deps:

        label = symbol_table.get(dep)

        if not label:
            continue

        if dep == "aws_vpc":
            lines.append(f"{dep}.{label}.id")

        elif dep == "aws_subnet":
            lines.append(f"{dep}.{label}.id")

        elif dep == "aws_security_group":
            lines.append(f"{dep}.{label}.id")

        elif dep == "aws_db_subnet_group":
            lines.append(f"{dep}.{label}.name")

        elif dep == "aws_iam_role":
            lines.append(f"{dep}.{label}.arn")

        else:
            lines.append(f"{dep}.{label}")

    logger.info("REFERENCE CONTEXT FOR %s:\n%s", node.entity, "\n".join(lines))
    return "\n".join(lines)

# ======================================================
# CONTEXT ASSEMBLY
# ======================================================

def assemble_context(query: str, node: ResourceNode, symbol_table: dict[str, str], global_rows):
    #30 May

    filtered_rows = filter_rows_for_resource(
        rows=global_rows,
        entity=node.entity,
        hard_deps=node.hard_deps,
    )

    logger.info("Context rows for %s = %s", node.entity, len(filtered_rows))
    argref_chunks = [
        r.chunk_id
        for r in filtered_rows
        if r.metadata.get("section", "").lower() == "argument reference"
    ]

    logger.info(
        "ARGREF CHUNKS FOR %s = %s",
        node.entity,
        argref_chunks,
    )

    #30 May
    logger.info("GLOBAL ROWS FOR %s", node.entity)

    for row in global_rows:

        if row.metadata.get("entity") == node.entity:

            logger.info("GLOBAL | %s | %s", row.chunk_id, row.metadata.get("section"))

    entity_rows = [r for r in filtered_rows if r.metadata.get("entity") == node.entity]
    
    #30 May
    logger.info("%s AFTER XYZ FILTER=%s", node.entity, len(filtered_rows))

    logger.info("%s entity_rows=%s dep_rows=%s", node.entity, len(entity_rows), len(filtered_rows) - len(entity_rows))

    # P1 FIX: guarantee an argument-reference floor for the TARGET entity.
    #
    # Previously this top-up only fired when the entity had ZERO rows
    # ("if not entity_rows"). That created an inversion: resources the main
    # retriever MISSED were rescued with deterministic, argument-reference-first
    # context, while resources it PARTIALLY found were frozen with whatever
    # scraps survived the global k-cap (sometimes a single argument-reference
    # chunk). Those partially-covered resources then failed `terraform validate`
    # because their schema was incomplete.
    #
    # We now top every target entity up to ARGREF_FLOOR argument-reference
    # chunks using the deterministic, SECTION_PRIORITY-ordered scan, merging
    # only chunks not already present (dedup by chunk_id). The fetched rows are
    # left untagged so build_xml_context treats them as primary documentation.
    existing_ids = {r.chunk_id for r in filtered_rows}

    existing_argref = sum(
        1 for r in entity_rows
        if r.metadata.get("section", "").lower() == "argument reference"
    )

    if existing_argref < ARGREF_FLOOR:

        if not entity_rows:
            logger.warning("Global retrieval missed %s", node.entity)
        else:
            logger.info(
                "Topping up %s: argument_reference=%s < floor=%s",
                node.entity, existing_argref, ARGREF_FLOOR,
            )

        bm25 = _get_bm25()

        # Priority-ordered candidate scan (argument reference first). Fetch a
        # generous set so we can reach the floor even after skipping duplicates.
        candidates = retrieve_entity_rows(node.entity, bm25, k=ARGREF_FLOOR * 2)

        added = 0
        for cand in candidates:

            if cand.metadata.get("section", "").lower() != "argument reference":
                continue

            if cand.chunk_id in existing_ids:
                continue

            filtered_rows.append(cand)
            entity_rows.append(cand)
            existing_ids.add(cand.chunk_id)
            added += 1
            
            existing_argref += 1

            logger.info("FLOOR TOPUP %s | %s", cand.chunk_id, cand.metadata.get("section"))

            if existing_argref >= ARGREF_FLOOR:
                break

        logger.info(
            "%s floor top-up added=%s argument_reference_now=%s",
            node.entity, added, existing_argref,
        )

    logger.info("%s -> rows=%s", node.entity, len(filtered_rows))

    if node.entity == "aws_appautoscaling_policy":

        logger.info("FINAL CHUNKS USED:")

        for row in filtered_rows:

            logger.info(
                "%s | %s | %s",
                row.chunk_id,
                row.metadata.get("section"),
                row.metadata.get("header_h3"),
            )

    for row in filtered_rows:

        logger.info("%s | %s", row.metadata.get("entity"), row.chunk_id)

    section_counts = {}

    for row in filtered_rows:
        section = row.metadata.get("section", "unknown")
        section_counts[section] = (
            section_counts.get(section, 0) + 1
        )

    logger.info(
        "%s sections=%s",
        node.entity,
        section_counts
    )

    #1 June
    for row in filtered_rows:
        logger.info("%s | %s", row.chunk_id, row.metadata.get("section"))

    xml_context = build_xml_context(filtered_rows)

    logger.info(
        "XML CONTEXT HEAD FOR %s:\n%s",
        node.entity,
        xml_context[:1000],
    )

    logger.info(
        "CONTEXT CHARS FOR %s = %s",
        node.entity,
        len(xml_context),
    )

    if "db_name" in xml_context:
        logger.info("DB_NAME FOUND IN FINAL CONTEXT")
    else:
        logger.warning("DB_NAME MISSING FROM FINAL CONTEXT")

    reference_context = build_dependency_reference_context(node, symbol_table)

    if node.entity == "aws_appautoscaling_policy":
        logger.info(
            "FULL CONTEXT FOR APPAUTOSCALING POLICY:\n%s",
            xml_context
        )

    if node.entity in {"aws_eks_node_group", "aws_appautoscaling_policy"}:

        logger.info("\n%s XML CONTEXT\n%s\n", node.entity, xml_context[:10000])

    if node.entity == "aws_instance":
        logger.info("\nAWS_INSTANCE XML\n%s\n", xml_context[:10000])

    references = []

    for entity, label in symbol_table.items():

        references.append(f"{entity} = {label}")

    ref_block = ""

    if references:

        ref_block = (
            "\n\n"
            "AVAILABLE TERRAFORM REFERENCES:\n"
            + "\n".join(references)
        )

    final_context = xml_context + ref_block + reference_context

    if node.entity == "aws_appautoscaling_policy":
        logger.info(
            "\n===== FINAL CONTEXT FOR %s =====\n%s\n=====================\n",
            node.entity,
            final_context,
        )

    logger.info("Context chars for %s = %s", node.entity, len(final_context))

    logger.info("\n%s FINAL CONTEXT\n%s\n", node.entity, final_context[:20000])

    return final_context

# ======================================================
# SYSTEM PROMPT
# ======================================================

SYSTEM_PROMPT = """You are a Terraform infrastructure engineer specialising in AWS.

Your task is to generate valid HCL for a SINGLE Terraform resource block.

Rules:
1. Output ONLY the resource block — no other blocks, no commentary, no markdown fences.
2. Use references from the symbol table verbatim (e.g. aws_iam_role.main.arn).
3. Use var.xxx for all configurable values: names, CIDR blocks, instance sizes, counts, regions, tags.
4. Include all required arguments and all required nested blocks. When a nested block is required by the Terraform schema, it must be generated even if default values are needed.
5. Resource label MUST exactly match the provided resource label.
6. Follow snake_case for all argument values you invent.
7. Do NOT generate depends_on unless there is a genuine timing dependency not expressed by a reference.
8. Do NOT output variables, outputs, providers, or locals — only the resource block.
9. If you are unsure of an argument value, use a descriptive var.xxx reference.
10. Prefer references over hardcoded values.
11. Prefer production-safe defaults.
12. Avoid deprecated Terraform arguments.
13. Use interpolation references instead of duplicated values.
14. Reuse previously generated resources when possible.
15. Do not invent unsupported arguments.
16. When AVAILABLE TERRAFORM REFERENCES are provided, prefer using those references instead of creating new standalone resources.
17. If a referenced resource satisfies a dependency, attach it rather than creating alternative configuration.
18. Generate Terraform compatible with hashicorp/aws provider version 5.x. Never use deprecated arguments.

19. Include required arguments.

    Optional arguments should only be emitted when:
    - explicitly requested by the user
    - required by another emitted argument
    - necessary for a minimal deployable configuration

    Do not emit advanced optional arguments merely because they appear in documentation.

20. The user query identifies the feature of interest, not a partial resource definition.
21. Always include required arguments.
22. Never iterate over a resource unless count or for_each exists.
23. When referencing a Terraform resource: resource "aws_subnet" "subnet" use: [aws_subnet.subnet.id]
24. Do not use Terraform for-expressions unless the referenced resource uses count or for_each.

***EXAMPLE***

    Use:

    aws_subnet.subnet.id or [aws_subnet.subnet.id]

    Do not generate Terraform for-expressions such as:

    [for x in aws_subnet.subnet : x.id]

    unless the referenced resource explicitly uses count or for_each.

25. Output format example:

    resource "aws_instance" "example" {
    ...
    }

    Use the exact Terraform Resource Type and Terraform Resource Label provided above.
    
    CRITICAL:

26. When multiple Argument Reference chunks are present, treat them as the source of truth and ignore any conflicting prior knowledge. The provided documentation always takes precedence over your pretrained Terraform knowledge.

27. Only use arguments explicitly present in the Argument Reference sections of the provided context. Do not invent deprecated or legacy Terraform arguments.
"""


# ======================================================
# RESOURCE GENERATION
# ======================================================

def _extract_var_refs(hcl: str) -> list[str]:
    return sorted(set(re.findall(r"var\.([a-z0-9_]+)", hcl)))

_DYNAMIC_OPEN = re.compile(r'^dynamic\s+"([A-Za-z0-9_]+)"')
_FOR_EACH     = re.compile(r'^for_each\s*=\s*var\.([A-Za-z0-9_]+)')
_VAR_ASSIGN   = re.compile(r'^([A-Za-z0-9_]+)\s*=\s*var\.([A-Za-z0-9_]+)')

def _extract_var_sources(entity: str, hcl: str):
    """
    Map var.NAME -> (entity, schema_path).

    Dynamic blocks are unwrapped so provenance points at the REAL nested block:
      dynamic "metric_dimension" {        -> path segment 'metric_dimension'
        for_each = var.metric_dimensions  -> recorded against the BLOCK path
                                             with a '[]' marker => collection
        content {                         -> transparent (no path segment)
          name = var.x                    -> '<...>.metric_dimension.name'
        }
      }
    """
    result = defaultdict(list)

    stack = []

    def path_names():
        return [n for (n, _dyn) in stack if n]

    for line in hcl.splitlines():

        stripped = line.strip()

        code = re.sub(
            r'"(?:\\.|[^"\\])*"',
            "",
            stripped
        )

        opens = code.count("{")
        closes = code.count("}")

        fe = _FOR_EACH.match(stripped)
        if fe:
            var_name = fe.group(1)
            path = ".".join(path_names())          # tail is the dynamic block label
            if path:
                result[var_name].append((entity, path + "[]"))   # '[]' => list(object)
                logger.info(
                    "VAR SOURCE var=%s entity=%s path=%s (for_each)",
                    var_name,
                    entity,
                    path + "[]",
                )
        elif opens == 0:
            m = _VAR_ASSIGN.match(stripped)
            if m:
                arg_name = m.group(1)
                var_name = m.group(2)
                path = ".".join(path_names() + [arg_name])
                result[var_name].append((entity, path))
                logger.info(
                    "VAR SOURCE var=%s entity=%s path=%s",
                    var_name,
                    entity,
                    path,
                )

        if (opens > closes and code.endswith("{") and "=" not in code):
            d = _DYNAMIC_OPEN.match(stripped)
            if d:
                stack.append((d.group(1), True))              # dynamic "X" -> push X
            else:
                head = code[:-1].strip()
                name = head.split()[0] if head else ""
                if not name or name.startswith("resource"):
                    stack.append((None, False))
                elif name == "content" and any(is_dyn for (_n, is_dyn) in stack):
                    stack.append((None, False))               # content -> transparent
                else:
                    stack.append((name, False))
        else:
            net = opens - closes
            if net > 0:
                stack.extend([(None, False)] * net)
            elif net < 0:
                for _ in range(-net):
                    if stack:
                        stack.pop()

    return dict(result)

def generate_resource(query: str, node: ResourceNode, context: str, symbol_table: dict[str, str], generated_types) -> GeneratedBlock:
  
    client = _get_client()

    user_message = (

        f"USER ARCHITECTURE GOAL:\n"
        f"{query}\n\n"

        f"GENERATION CONTEXT:\n"
        f"{context}\n\n"

        f"Terraform Resource Type:\n"
        f"{node.entity}\n\n"

        f"Terraform Resource Label:\n"
        f"{node.label}\n\n"

        f"Generate ONLY the Terraform resource block.\n"
        f"No markdown.\n"
        f"No explanation.\n"
    )

    logger.info("Generating: %s", node.entity)
    logger.info("CONTEXT CHARS=%s", len(context))

    try:
        logger.info("\n%s USER MESSAGE SENT TO LLM\n%s\n", node.entity, user_message[:30000])
        if node.entity == "aws_appautoscaling_policy":

            logger.info("\nAPPAUTOSCALING FINAL USER MESSAGE\n%s\n", user_message)

        response = client.chat.completions.create(
            
            model=OPENAI_MODEL, 

            max_completion_tokens=MAX_TOKENS,

            temperature=0,

            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": user_message,
                },
            ],
        )

        raw = (response.choices[0].message.content.strip())
        logger.info("RAW RESPONSE %s:\n%s", node.entity, raw[:2000])
        logger.info("HCL HASH %s = %s", node.entity, hashlib.md5(raw.encode()).hexdigest())

    except Exception as exc:
        logger.error("Generation failed for %s: %s", node.entity, exc)
        raw = f'# ERROR generating {node.entity}: {exc}'

    # Strip accidental markdown fences
    raw = re.sub(r"^```[a-z]*\n?", "", raw)
    raw = re.sub(r"\n?```$", "", raw)
    raw = raw.strip()

    raw = _normalize_argument_aliases(node.entity, raw)
    raw = _normalize_ecr_scan_on_push(node.entity, raw)
    raw = _normalize_ecs_service_connect(node.entity, raw)
    raw = _normalize_ecs_task_definition_blocks(node.entity, raw)
    raw = _normalize_ecs_deployment_configuration(node.entity, raw)
    raw = _normalize_ecs_capacity_provider(node.entity, raw)
    raw = _normalize_rds_parameter_blocks(node.entity, raw)
    raw = _normalize_cloudfront_required_blocks(node.entity, raw)
    raw = _normalize_lb_listener_forward(node.entity, raw)
    raw = _normalize_list_references(raw)
    raw = _normalize_subnet_optional_arguments(raw)
    raw = _normalize_vpc_optional_arguments(node.entity, raw)
    raw = _normalize_ecs_cluster_arguments(node.entity, raw)
    raw = _normalize_cidr_block_lists(raw)
    raw = _remove_fake_reference_segments(raw)
    raw = _normalize_attribute_aliases(raw)
    raw = _normalize_malformed_var_refs(raw)
    raw = _remove_invalid_resource_types(raw)
    raw = normalize_block_vs_argument(node.entity, raw)

    #11 June
    logger.info("RUNNING VALIDATOR FOR %s", node.entity)
    #findings = validate_resource(entity=node.entity, hcl=raw)

    findings = validate_resource(entity=node.entity, hcl=raw, generated_types=generated_types)

    logger.info("VALIDATOR RETURNED %s FINDINGS FOR %s", len(findings), node.entity)

    for finding in findings:
        logger.info(
            "SCHEMA FINDING "
            "kind=%s "
            "entity=%s "
            "field=%s",
            finding.kind,
            finding.entity,
            finding.field
        )

        SCHEMA_FINDING_COUNTS[finding.kind] += 1

    var_refs = _extract_var_refs(raw)
    var_sources = _extract_var_sources(node.entity, raw)

    symbol_table[node.entity] = node.label
    logger.info("SYMBOL TABLE NOW=%s", symbol_table)

    logger.info("Generated %s — vars: %s", node.entity, var_refs)

    logger.info("\n===== RAW MODEL OUTPUT =====\n%s\n============================", raw)
    logger.info("OUTPUT LENGTH=%s", len(raw))

    return GeneratedBlock(entity=node.entity, label=node.label, hcl=raw, var_refs=var_refs, var_sources=var_sources)

def generate_label(entity: str, existing: set[str]):

    base = (entity.replace("aws_", "").replace("_", "-"))

    candidate = base

    index = 1

    while candidate in existing:

        candidate = f"{base}-{index}"

        index += 1
    
    candidate = re.sub(r'^[^a-zA-Z_]+', '', candidate)
    if not candidate:
        candidate = "resource"
    return candidate.replace("-", "_")

def _remove_fake_reference_segments(terraform: str) -> str:

    return re.sub(
        r'(aws_[a-zA-Z0-9_]+\.[a-zA-Z0-9_]+)\.references(?:\[[^\]]+\])?\.',
        r'\1.',
        terraform,
    )

def _normalize_argument_aliases(entity: str, hcl: str) -> str:

    aliases = ARGUMENT_ALIASES.get(entity)

    if not aliases:
        return hcl

    lines = []
    depth = 0

    for line in hcl.splitlines():

        stripped = line.strip()

        depth += line.count("{")
        depth -= line.count("}")

        if depth == 1:

            for old_arg, new_arg in aliases.items():

                pattern = rf"^(\s*){re.escape(old_arg)}\s*="

                if re.match(pattern, line):

                    line = re.sub(
                        pattern,
                        rf"\1{new_arg} =",
                        line,
                    )

        lines.append(line)

    return "\n".join(lines)

def _normalize_attribute_aliases(terraform: str) -> str:

    for (resource_type, old_attr), new_attr in ATTRIBUTE_ALIASES.items():

        pattern = (
            rf'({re.escape(resource_type)}'
            rf'\.[a-zA-Z0-9_]+)\.'
            rf'{re.escape(old_attr)}\b'
        )

        terraform = re.sub(
            pattern,
            rf'\1.{new_attr}',
            terraform,
        )

    return terraform

def _normalize_subnet_optional_arguments(terraform: str) -> str:

    logger.info("RUNNING SUBNET SANITIZER")

    DENYLIST = {
        "map_customer_owned_ip_on_launch",
        "customer_owned_ipv4_pool",
        "outpost_arn",
        "enable_lni_at_device_index",
        "ipv4_ipam_pool_id",
        "ipv6_ipam_pool_id",
        "ipv4_netmask_length",
        "ipv6_netmask_length",
    }

    lines = []

    for line in terraform.splitlines():

        stripped = line.strip()

        remove = False

        for arg in DENYLIST:

            if _is_argument_assignment(stripped, arg):
                logger.info("REMOVED SUBNET ARG: %s", arg)
                remove = True
                break

        if not remove:
            lines.append(line)

    return "\n".join(lines)

def _normalize_vpc_optional_arguments(entity:str, terraform: str) -> str:
    
    logger.info("VPC SANITIZER CALLED FOR %s", entity)

    if entity != "aws_vpc":
        return terraform
    
    DENYLIST = {
        "ipv6_cidr_block",
        "ipv6_cidr_block_network_border_group",
        "ipv6_ipam_pool_id",
        "assign_generated_ipv6_cidr_block",
    }

    lines = []

    for line in terraform.splitlines():

        stripped = line.strip()

        remove = False

        for arg in DENYLIST:

            if _is_argument_assignment(stripped, arg):
                logger.info("REMOVED VPC ARG: %s", arg)
                remove = True
                break

        if not remove:
            lines.append(line)

    return "\n".join(lines)

def _normalize_cidr_block_lists(terraform: str) -> str:

    patterns = [
        r'(\bcidr_blocks\s*=\s*)\[var\.([a-zA-Z0-9_]+)\]',
        r'(\bipv6_cidr_blocks\s*=\s*)\[var\.([a-zA-Z0-9_]+)\]',
    ]

    for pattern in patterns:

        terraform = re.sub(
            pattern,
            r'\1var.\2',
            terraform,
        )

    return terraform

def _normalize_ecs_service_connect(entity: str, hcl: str) -> str:
    if entity != "aws_ecs_service":
        return hcl

    lines = hcl.splitlines()

    output = []
    skip = False
    depth = 0
    skip_depth = 0

    for line in lines:
        stripped = line.strip()

        if not skip and stripped.startswith("service_connect_configuration"):
            logger.info("REMOVED service_connect_configuration")
            skip = True
            skip_depth = depth
            depth += line.count("{")
            depth -= line.count("}")
            continue

        if skip:
            depth += line.count("{")
            depth -= line.count("}")

            if depth <= skip_depth:
                skip = False

            continue

        output.append(line)

        depth += line.count("{")
        depth -= line.count("}")

    return "\n".join(output)

def _normalize_ecs_task_definition_blocks(entity: str, hcl: str) -> str:
    if entity != "aws_ecs_task_definition":
        return hcl

    lines = []

    for line in hcl.splitlines():
        stripped = line.strip()

        if _is_argument_assignment(stripped, "placement_constraints"):
            logger.info("REMOVED ecs_task_definition placement_constraints arg")
            continue

        if _is_argument_assignment(stripped, "volume"):
            logger.info("REMOVED ecs_task_definition volume arg")
            continue

        lines.append(line)

    return "\n".join(lines)

def _normalize_ecs_deployment_configuration(entity: str, hcl: str) -> str:
    if entity != "aws_ecs_service":
        return hcl

    lines = hcl.splitlines()

    output = []
    skip = False
    depth = 0
    skip_depth = 0

    for line in lines:
        stripped = line.strip()

        if not skip and stripped.startswith("deployment_configuration"):
            logger.info("REMOVED deployment_configuration")
            skip = True
            skip_depth = depth
            depth += line.count("{")
            depth -= line.count("}")
            continue

        if skip:
            depth += line.count("{")
            depth -= line.count("}")

            if depth <= skip_depth:
                skip = False

            continue

        output.append(line)

        depth += line.count("{")
        depth -= line.count("}")

    return "\n".join(output)

def _normalize_ecs_capacity_provider(entity: str, hcl: str) -> str:

    if entity != "aws_ecs_capacity_provider":
        return hcl

    lines = hcl.splitlines()

    output = []

    skip = False
    depth = 0
    skip_depth = 0

    for line in lines:

        stripped = line.strip()

        if (
            not skip
            and
            stripped.startswith("network_configuration")
        ):
            logger.info(
                "REMOVED ecs_capacity_provider network_configuration"
            )

            skip = True
            skip_depth = depth

            depth += line.count("{")
            depth -= line.count("}")

            continue

        if skip:

            depth += line.count("{")
            depth -= line.count("}")

            if depth <= skip_depth:
                skip = False

            continue

        output.append(line)

        depth += line.count("{")
        depth -= line.count("}")

    return "\n".join(output)
# ======================================================
# STITCHING
# ======================================================

# Common variable definitions with sensible defaults and descriptions
_KNOWN_VARS: dict[str, tuple[str, str, str]] = {
    # name: (type, default, description)
    "region":           ("string", '"us-east-1"',    "AWS region"),
    "environment":      ("string", '"dev"',           "Deployment environment"),
    "project":          ("string", '"myproject"',     "Project name"),
    "name":             ("string", '"main"',          "Resource name prefix"),
    "vpc_cidr":         ("string", '"10.0.0.0/16"',   "VPC CIDR block"),
    "subnet_cidr":      ("string", '"10.0.1.0/24"',   "Subnet CIDR block"),
    "private_cidr":     ("string", '"10.0.2.0/24"',   "Private subnet CIDR"),
    "instance_type":    ("string", '"t3.micro"',      "EC2 instance type"),
    "instance_class":   ("string", '"db.t3.micro"',   "RDS instance class"),
    "desired_count":    ("number", "1",               "Desired task/instance count"),
    "min_size":         ("number", "1",               "Minimum autoscaling size"),
    "max_size":         ("number", "3",               "Maximum autoscaling size"),
    "retention_days":   ("number", "30",              "Log retention in days"),
    "tags":             (
        'map(string)',
        '{\n    Environment = "dev"\n    Project     = "myproject"\n  }',
        "Resource tags",
    ),
    "allowed_ssh_cidr_blocks": (
    "list(string)",
    '["0.0.0.0/0"]',
    "Allowed SSH CIDR blocks",
    ),

    "environment_variables": (
        "map(string)",
        '{}',
        "Lambda environment variables",
    ),

    "vpc_tags": (
        "map(string)",
        '{ Environment = "dev" }',
        "VPC tags",
    ),

    "cidr_blocks": (
        "list(string)",
        '["0.0.0.0/0"]',
        "CIDR blocks",
    ),

    "subnet_ids": (
    "list(string)",
    '[]',
    "Subnet IDs",
    ),

    "security_group_ids": (
        "list(string)",
        '[]',
        "Security group IDs",
    ),

    "public_access_cidrs": (
        "list(string)",
        '["0.0.0.0/0"]',
        "Allowed CIDRs",
    ),

    "ingress_cidr_blocks": (
    "list(string)",
    '["0.0.0.0/0"]',
    "Ingress CIDRs",
    ),

    "private_subnet_ids": (
        "list(string)",
        '[]',
        "Private subnet IDs",
    ),

    "availability_zones": (
        "list(string)",
        '["us-east-1a","us-east-1b"]',
        "AZs",
    ),

    "node_group_desired_size": (
    "number",
    "2",
    "Desired node count",
    ),

    "node_group_min_size": (
        "number",
        "1",
        "Minimum node count",
    ),

    "node_group_max_size": (
        "number",
        "5",
        "Maximum node count",
    ),

    "node_group_disk_size": (
        "number",
        "20",
        "Node disk size",
    ),

    "node_group_instance_types": (
        "list(string)",
        '["t3.medium"]',
        "Node instance types",
    ),

    "endpoint_private_access": (
        "bool",
        "true",
        "Private endpoint access",
    ),

    "endpoint_public_access": (
        "bool",
        "true",
        "Public endpoint access",
    ),

    "policy_json": (
        "string",
        '"{}"',
        "IAM policy JSON"
    ),

    "sqs_dead_letter_queue_arn": (
        "string",
        '"arn:aws:sqs:us-east-1:123456789012:dlq"',
        "Dead letter queue ARN",
    ),
}

def infer_variable_type_from_schema(sources):

    _FIELD_TYPE_OVERRIDES = {
        "cidr_blocks": "list(string)",
        "ipv6_cidr_blocks": "list(string)",
        "prefix_list_ids": "list(string)",
        "security_groups": "list(string)",
        "subnet_ids": "list(string)",
        "availability_zones": "list(string)",
    }

    candidate_types = []

    for entity, path in sources:

        if path.endswith("[]"):
            block_path = path[:-2]
            hcl_type = block_object_type(entity, block_path)
            logger.info("SCHEMA LOOKUP entity=%s block=%s type=%s",
                        entity, block_path, hcl_type)
        else:
            field = path.split(".")[-1]

            # 1) precise path lookup
            raw_type = find_argument_type_by_path(entity, path)

            # 2) fallback: global search by leaf field name
            if raw_type is None:
                raw_type = find_argument_type(entity, field)

            hcl_type = terraform_type_to_hcl(raw_type)

            # 3) fallback: deterministic field-name override (already HCL strings)
            if hcl_type is None:
                hcl_type = _FIELD_TYPE_OVERRIDES.get(field)

            logger.info("SCHEMA LOOKUP entity=%s path=%s type=%s",
                        entity, path, hcl_type)

        if hcl_type:
            candidate_types.append(hcl_type)

    if not candidate_types:
        return None

    unique = set(candidate_types)
    if len(unique) > 1:
        logger.warning("VAR TYPE CONFLICT=%s", candidate_types)
        return None

    return candidate_types[0]

def infer_variable_type(var_name: str) -> tuple[str, str | None]:

    logger.info("DISCOVERED VAR=%s", var_name)

    var = var_name.lower()

    EXACT_TYPE_OVERRIDES = {
        # Security Group Rules
        "security_group_ingress_rules": "list(any)",
        "security_group_egress_rules": "list(any)",
        "sg_ingress_rules": "list(any)",
        "sg_egress_rules": "list(any)",

        # AutoScaling
        "vpc_zone_identifier": "list(string)",

        # ECS
        "requires_compatibilities": "list(string)",

        # CloudFront
        "aliases": "set(string)",
        "allowed_methods": "set(string)",
        "cached_methods": "set(string)",
        "locations": "set(string)",

        # API Gateway
        "stage_variables": "map(string)",

        # ECS Service
        "enable_ecs_managed_tags": "bool",

        # RDS
        "rds_cluster_parameters": "list(any)",

        # ECS
        "propagate_tags": "string",

        "volumes": "list(any)",

        "proxy_configuration_properties": "map(string)",

        "client_id_list": "set(string)",

        "oidc_client_id_list": "set(string)",
    }

    BOOLEAN_OVERRIDES = {
        "multi_az",
        "publicly_accessible",
        "deletion_protection",
        "skip_final_snapshot",
        "apply_immediately",
        "apply_immediately",
        "enable_dns_support",
        "enable_dns_hostnames",
        "enable_network_address_usage_metrics",
        "copy_tags_to_snapshot",
        "enable_tls_version_and_cipher_suite_headers"
    }

    NUMBER_OVERRIDES = {
        "allocated_storage",
        "retention_period",
        "enable_lni_at_device_index"
    }

    MAP_ANY_OVERRIDES = {
        "lb_target_group_health_check",
        "lb_target_group_stickiness",
        "scaling_configuration",
        "route_settings",
    }

    LIST_ANY_SUFFIXES = (
        "_ingress_rules",
        "_egress_rules",
        "_parameters",
    )

    NUMBER_SUFFIXES = (
        "_size",
        "_count",
        "_port",
        "_interval",
        "_timeout",
        "_duration",
        "_threshold",
        "_retention_period",
    )

    LIST_STRING_SUFFIXES = (
        "_ids",
        "_arns",
        "_cidr_blocks",
        "_availability_zones",
        "_subnets",
        "_security_groups",
        "_cidrs",
        "_cache_keys",
        "_list"
    )

    SET_STRING_SUFFIXES = (
        "_allowed_methods",
        "_cached_methods",
        "_locations",
        "_headers",
        "_whitelisted_names",
    )

    MAP_STRING_HINTS = (
        "tags",
        "environment_variables",
        "environment_vars",
        "labels",
        "metadata",
        "annotations",
    )

    LIST_STRING_NAMES = {
        "subnets",
        "security_groups",
        "headers",
    }

    STRING_OVERRIDES = {
        "ecs_service_propagate_tags",
    }

    #
    # Exact overrides first
    #
    if var in EXACT_TYPE_OVERRIDES:
        return (EXACT_TYPE_OVERRIDES[var], None)

    if var in BOOLEAN_OVERRIDES:
        return ("bool", None)

    if var in NUMBER_OVERRIDES:
        return ("number", None)

    if var in MAP_ANY_OVERRIDES:
        return ("map(any)", None)

    if var.endswith("_configuration"):
        return ("map(any)", None)
    
    if var == "parameters":
        return ("map(any)", None)
    
    #
    # Boolean naming conventions
    #
    if ("enable_" in var or "associate_" in var):
        return ("bool", None)

    if var.endswith(("_enabled", "_encrypted")):
        return ("bool", None)
    
    if var.endswith("enable_xff_client_port"):
        return ("bool", None)

    if any(
        x in var
        for x in (
            "private_access",
            "public_access",
            "force_detach",
        )
    ):
        return ("bool", None)
    
    # Explicit suffix-based rules

    if var in STRING_OVERRIDES:
        return ("string", None)

    if var in LIST_STRING_NAMES:
        return ("list(string)", None)
    
    if var.endswith(LIST_ANY_SUFFIXES):
        return ("list(any)", None)

    if var.endswith(NUMBER_SUFFIXES):
        return ("number", None)

    if var.endswith(SET_STRING_SUFFIXES):
        return ("set(string)", None)

    if var.endswith(LIST_STRING_SUFFIXES):
        return ("list(string)", None)

    #
    # Generic numeric hints
    #
    if any(
        x in var
        for x in (
            "desired_size",
            "min_size",
            "max_size",
            "disk_size",
            "retention_days",
        )
    ):
        return ("number", None)

    #
    # Misc list(string) variables that don't follow suffix patterns
    #
    if var in (
        "instance_types",
        "managed_policy_arns",
        "api_gateway_endpoint_types",
        "security_groups",
    ):
        return ("list(string)", None)

    #
    # map(string)
    #
    if any(hint in var for hint in MAP_STRING_HINTS):
        return ("map(string)", None)

    #
    # Default
    #
    return ("string", None)

def _normalize_lb_listener_forward(entity: str, hcl: str) -> str:
    if entity != "aws_lb_listener":
        return hcl
    
    if not ("forward {" in hcl and "target_group_arn =" in hcl):
        return hcl                     

    pattern = r'forward\s*\{\s*target_group_arn\s*=\s*([^}]+?)\s*\}'

    return re.sub(pattern, r'target_group_arn = \1', hcl, flags=re.DOTALL)


def _normalize_list_references(terraform: str) -> str:

    LIST_REFERENCE_ARGS = {
        "subnet_ids",
        "security_group_ids",
        "vpc_zone_identifier",
        "public_access_cidrs"
    }

    for arg in LIST_REFERENCE_ARGS:

        pattern = (rf'({arg}\s*=\s*)(aws_[a-z0-9_]+\.[a-z0-9_]+\.id)(?!\])')

        before = terraform

        terraform = re.sub(
            pattern,
            r'\1[\2]',
            terraform
        )

        if before != terraform:
            logger.info("List Normalized: %s", arg)

    return terraform

def _normalize_ecr_scan_on_push(entity: str, hcl: str) -> str:
    if entity != "aws_ecr_repository":
        return hcl

    lines = []
    depth = 0

    for line in hcl.splitlines():
        stripped = line.strip()

        # Only remove top-level scan_on_push
        if (
            depth == 1
            and stripped.startswith("scan_on_push")
            and "=" in stripped
        ):
            logger.info("REMOVED TOP LEVEL ECR scan_on_push")
            continue

        lines.append(line)

        depth += line.count("{")
        depth -= line.count("}")

    return "\n".join(lines)

def _normalize_ecs_cluster_arguments(entity: str, hcl: str) -> str:

    if entity != "aws_ecs_cluster":
        return hcl

    denylist = {
        "s3_encryption_enabled",
    }

    out = []

    for line in hcl.splitlines():

        stripped = line.strip()

        if any(
            _is_argument_assignment(stripped, arg)
            for arg in denylist
        ):
            logger.info(
                "REMOVED ECS CLUSTER ARG=%s",
                stripped,
            )
            continue

        out.append(line)

    return "\n".join(out)

def _remove_invalid_resource_types(terraform: str) -> str:

    #known = _get_known_entities()

    known = {entity for entity in _get_known_entities() if schema_index.is_known(entity)}

    lines = terraform.splitlines()

    output = []

    i = 0

    while i < len(lines):

        line = lines[i]

        match = re.match(
            r'^\s*resource\s+"([^"]+)"\s+"([^"]+)"\s*\{', line)

        if not match:
            output.append(line)
            i += 1
            continue

        resource_type = match.group(1)

        if resource_type in known:
            output.append(line)
            i += 1
            continue

        logger.warning("REMOVING INVALID RESOURCE TYPE: %s", resource_type)

        depth = line.count("{") - line.count("}")

        i += 1

        while i < len(lines) and depth > 0:
            depth += lines[i].count("{")
            depth -= lines[i].count("}")
            i += 1

    return "\n".join(output)

def _fix_resource_labels(terraform: str) -> str:

    labels_by_type = defaultdict(set)

    for match in re.finditer(
        r'resource\s+"([^"]+)"\s+"([^"]+)"',
        terraform
    ):
        labels_by_type[
            match.group(1)
        ].add(
            match.group(2)
        )

    def replace(match):

        resource_type = match.group(1)
        found_label = match.group(2)

        valid_labels = labels_by_type.get(
            resource_type,
            set(),
        )

        #
        # already valid
        #
        if found_label in valid_labels:
            return match.group(0)

        #
        # ambiguous -> leave untouched
        #
        if len(valid_labels) != 1:
            return match.group(0)

        actual_label = next(iter(valid_labels))

        logger.info(
            "LABEL FIX %s.%s -> %s.%s",
            resource_type,
            found_label,
            resource_type,
            actual_label,
        )

        return (
            f"{resource_type}."
            f"{actual_label}"
            f"{match.group(3)}"
        )

    pattern = (
        r'\b'
        r'(aws_[a-z0-9_]+)'
        r'\.([a-zA-Z0-9_]+)'
        r'(\.[a-zA-Z0-9_]+)'
    )

    return re.sub(
        pattern,
        replace,
        terraform,
    )

def _fix_invalid_sqs_attributes(terraform: str) -> str:

    terraform = re.sub(
        r'aws_sqs_queue\.[^.]+\.dead_letter_target_arn',
        'var.sqs_dead_letter_queue_arn',
        terraform,
    )

    terraform = re.sub(
        r'aws_sqs_queue_redrive_policy\.[^.]+\.arn',
        'var.sqs_dead_letter_queue_arn',
        terraform,
    )

    return terraform

def _fix_undeclared_data_references(terraform: str) -> str:

    terraform = re.sub(
        r'data\.aws_iam_policy_document\.[^.]+\.json',
        'var.policy_json',
        terraform,
    )

    return terraform

def _generate_variables_tf(all_var_refs: list[str], all_var_sources) -> str:

    logger.info("Entered _generate_variables_tf")
    logger.info("All_VAR_SOURCES=%s", all_var_sources)

    schema_hits = 0
    heuristic_hits = 0

    blocks: list[str] = []

    for var_name in sorted(set(all_var_refs)):

        source = all_var_sources.get(var_name)

        schema_type = None

        if source:
            schema_type = infer_variable_type_from_schema(source)

        if schema_type:
            schema_hits += 1

            logger.info("SCHEMA TYPE %s -> %s", var_name, schema_type)

            inferred_type = schema_type
            default = None
            
        else:
            heuristic_hits += 1

            inferred_type, default = infer_variable_type(var_name)

            logger.info("HEURISTIC TYPE %s -> %s", var_name, inferred_type)

        block = (
            f'variable "{var_name}" {{\n'
            f'  description = "TODO: describe {var_name}"\n'
            f'  type        = {inferred_type}\n'
        )

        if default is not None:
            block += f'  default     = {default}\n'

        block += "}"

        blocks.append(block)
    
    total = schema_hits + heuristic_hits
    pct = (schema_hits*100/total if total else 0)
    logger.info("TYPE COVERAGE schema=%s heuristic=%s pct=%.1f%%", schema_hits, heuristic_hits, pct)
    return "\n\n".join(blocks) + "\n" if blocks else "# No variables required\n"


def _generate_outputs_tf(blocks: list[GeneratedBlock]) -> str:
    outputs: list[str] = []

    # Common output patterns per entity type
    OUTPUT_ATTRS: dict[str, list[tuple[str, str]]] = {
        "aws_vpc":                   [("vpc_id", "id")],
        "aws_subnet":                [("subnet_id", "id")],
        "aws_security_group":        [("security_group_id", "id")],
        "aws_instance":              [("instance_id", "id"), ("instance_public_ip", "public_ip")],
        "aws_iam_role":              [("iam_role_arn", "arn"), ("iam_role_name", "name")],
        "aws_iam_instance_profile":  [("instance_profile_arn", "arn")],
        "aws_lb":                    [("alb_arn", "arn"), ("alb_dns_name", "dns_name")],
        "aws_lb_target_group":       [("target_group_arn", "arn")],
        "aws_ecs_cluster":           [("ecs_cluster_arn", "arn"), ("ecs_cluster_id", "id")],
        "aws_ecs_service":           [("ecs_service_name", "name")],
        "aws_eks_cluster":           [("eks_cluster_endpoint", "endpoint"), ("eks_cluster_name", "name")],
        "aws_rds_cluster":           [("rds_endpoint", "endpoint"), ("rds_cluster_id", "cluster_identifier")],
        "aws_db_instance":           [("db_endpoint", "endpoint"), ("db_identifier", "identifier")],
        "aws_lambda_function":       [("lambda_arn", "arn"), ("lambda_invoke_arn", "invoke_arn")],
        "aws_s3_bucket":             [("s3_bucket_name", "id"), ("s3_bucket_arn", "arn")],
        "aws_cloudwatch_log_group":  [("log_group_name", "name"), ("log_group_arn", "arn")],
        "aws_api_gateway_rest_api":  [("api_gateway_id", "id"), ("api_gateway_invoke_url", "execution_arn")],
        "aws_kms_key":               [("kms_key_arn", "arn"), ("kms_key_id", "key_id")],
        "aws_nat_gateway":           [("nat_gateway_id", "id")],
    }

    for block in blocks:
        attrs = OUTPUT_ATTRS.get(block.entity, [])
        for output_name, attr in attrs:
            outputs.append(
                f'output "{output_name}" {{\n'
                f'  description = "{block.entity} {attr}"\n'
                f'  value       = {block.entity}.{block.label}.{attr}\n'
                f'}}'
            )

    return "\n\n".join(outputs) + "\n" if outputs else "# No outputs defined\n"


def _generate_providers_tf() -> str:
    return textwrap.dedent(
        '''\
terraform {
  required_version = ">= 1.5"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = var.region

  default_tags {
    tags = var.tags
  }
}
'''
    )

def stitch(blocks: list[GeneratedBlock], plan: GenerationPlan) -> dict[str, str]:
    """
    Combine generated blocks into a set of .tf files.
    Returns: {"main.tf": ..., "variables.tf": ..., "outputs.tf": ..., "providers.tf": ...}
    """
    # Collect all variable references across all blocks
    all_vars: list[str] = []
    all_var_sources = defaultdict(list)

    for block in blocks:

        all_vars.extend(block.var_refs)

        for var_name, sources in block.var_sources.items():
            all_var_sources[var_name].extend(sources)

    all_var_sources = dict(all_var_sources)
    logger.info("ALL VAR SOURCES=%s", all_var_sources)

    # Always include region and tags for providers.tf
    for essential in ("region", "tags", "environment", "project"):
        if essential not in all_vars:
            all_vars.append(essential)

    # main.tf: resource blocks separated by blank lines with entity comments
    main_parts: list[str] = []

    for block in blocks:
        comment = f"# {block.entity}"
        if block.entity not in plan.root_entities:
            comment += "  (dependency)"
        main_parts.append(f"{comment}\n{block.hcl}")

    main_tf = "\n\n".join(main_parts) + "\n"

    return {
        "providers.tf":  _generate_providers_tf(),
        "variables.tf":  _generate_variables_tf(all_vars, all_var_sources),
        "main.tf":       main_tf,
        "outputs.tf":    _generate_outputs_tf(blocks),
    }


# ======================================================
# VALIDATION
# ======================================================

def validate(files: dict[str, str]) -> list[str]:
    """
    Post-generation validation. Returns a list of warning strings.
    Checks:
    - All hard dependencies of generated resources are also present
    - Resource labels are consistent (every reference X.Y has a definition)
    """
    warnings: list[str] = []
    main_tf = files.get("main.tf", "")

    # Extract generated resource types
    generated_types = set(re.findall(r'^resource\s+"(aws_[a-z0-9_]+)"', main_tf, re.MULTILINE))

    # Extract all references: resource_type.label.attribute
    referenced = re.findall(

            r'\b'
            r'(aws_[a-z0-9_]+)'
            r'\.([a-z0-9_]+)'
            r'\.([a-z0-9_]+)',

            main_tf
        )

    # Check every referenced type is also defined
    for ref_type, ref_label, ref_attr in referenced:
        if ref_type not in generated_types:
            warnings.append(f"Reference to {ref_type} found but not defined in main.tf")

    # Check hard dependencies are satisfied
    for rtype in generated_types:
        hard_deps = RESOURCE_DEPENDENCIES.get(rtype, {}).get("hard", [])
        for dep in hard_deps:
            if dep not in generated_types:
                warnings.append(
                    f"{rtype} requires {dep} (hard dependency) but it is not generated"
                )

    return warnings


# ======================================================
# MAIN PIPELINE
# ======================================================

def generate(query: str) -> GenerationResult:

    plan = build_plan(query)
    
    #30 MAY
    global_rows = retrieve_generation_context(query)

    planned_entities = {node.entity for node in plan.ordered_nodes}

    retrieved_entities = {
        row.metadata.get("entity")
        for row in global_rows
        if row.metadata.get("entity")
    }
    
    logger.info("POST BACKFILL COVERAGE=%s/%s", len(planned_entities & retrieved_entities), len(planned_entities))

    missing_entities = (planned_entities - retrieved_entities)

    bm25 = _get_bm25()

    for entity in missing_entities:

        logger.info("BACKFILL ENTITY=%s", entity)

        global_rows.extend(retrieve_entity_rows(entity, bm25, k=4))
    
    retrieved_entities = {row.metadata.get("entity") for row in global_rows if row.metadata.get("entity")}

    coverage = len(planned_entities & retrieved_entities)

    logger.info(
        "POST BACKFILL COVERAGE=%s/%s",
        coverage,
        len(planned_entities),
    )

    #30 MAY
    logger.info("GLOBAL ENTITIES=%s", sorted({r.metadata.get("entity") for r in global_rows}))

    planned_entities = {node.entity for node in plan.ordered_nodes}
    #30 May
    logger.info("PLANNED ENTITIES=%s", sorted(planned_entities))
    retrieved_entities = {
        row.metadata.get("entity")
        for row in global_rows
        if row.metadata.get("entity")
    }

    coverage = len(planned_entities & retrieved_entities)

    logger.info(
        "PLANNER COVERAGE=%s/%s (%.1f%%)",
        coverage,
        len(planned_entities),
        (
            coverage * 100 / len(planned_entities)
            if planned_entities else 0
        )
    )

    logger.info("MISSING ENTITIES=%s", sorted(planned_entities - retrieved_entities))

    if not plan.ordered_nodes:
        return GenerationResult(
            query=query,
            plan=plan,
            files={"error.tf": f"# Could not extract resources from query: {query}\n"},
            warnings=["No resources identified from query"],
        )

    logger.info(
        "Plan: %d resources in order: %s",
        len(plan.ordered_nodes),
        [n.entity for n in plan.ordered_nodes],
    )

    # 2. Generate each resource in topo order
    symbol_table: dict[str, str] = {}
    blocks: list[GeneratedBlock] = []

    generated_types = {node.entity for node in plan.ordered_nodes}
    for node in plan.ordered_nodes:
        context = assemble_context(query=query, node=node, symbol_table=symbol_table, global_rows=global_rows)
        block = generate_resource(query, node, context, symbol_table, generated_types=generated_types)
        blocks.append(block)

    # 3. Stitch into files
    files = stitch(blocks, plan)

    main_tf = files["main.tf"]

    main_tf = _fix_resource_labels(main_tf)

    main_tf = _fix_invalid_sqs_attributes(main_tf)

    main_tf = _fix_undeclared_data_references(main_tf)

    files["main.tf"] = main_tf

    existing_vars = set(re.findall(r'variable\s+"([^"]+)"', files["variables.tf"]))

    logger.info("EXISTING VARS=%s", sorted(existing_vars))

    current_refs = set(re.findall(r'var\.([A-Za-z0-9_]+)', files["main.tf"]))
    
    logger.info("CURRENT REFS=%s", sorted(current_refs))

    missing = current_refs - existing_vars

    logger.info("MISSING VARS=%s", sorted(missing))

    if missing:

        logger.warning("MISSING VARIABLE DECLARATIONS=%s", sorted(missing))

        for var_name in sorted(missing):

            var_type, default = infer_variable_type(var_name)

            block = (
                f'variable "{var_name}" {{\n'
                f'  type = {var_type}\n'
            )

            if default is not None:
                block += f'  default = {default}\n'

            block += '}\n\n'

            files["variables.tf"] += block

    # 4. Validate
    warnings = validate(files)
    if warnings:
        for w in warnings:
            logger.warning("Validation: %s", w)

    print_conflict_summary()
    return GenerationResult(query=query, plan=plan, files=files, warnings=warnings)


def print_result(result: GenerationResult) -> None:
    """Pretty-print a GenerationResult to stdout."""

    print("\n" + "=" * 72)
    print(f"Query:     {result.query}")
    print(f"Resources: {[n.entity for n in result.plan.ordered_nodes]}")

    if result.warnings:
        print("\nWarnings:")
        for w in result.warnings:
            print(f"  ⚠  {w}")

    print("=" * 72)

    logger.info("=" * 60)
    logger.info("SCHEMA FINDING SUMMARY")
    logger.info("=" * 60)

    for k, v in SCHEMA_FINDING_COUNTS.items():
        logger.info("%s = %s", k, v)

    for filename, content in result.files.items():
        print(f"\n{'-' * 30} {filename} {'-' * 30}\n")
        print(content)


# ======================================================
# ENTRY POINT
# ======================================================

if __name__ == "__main__":
    import sys

    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "create EKS cluster with node group"
    result = generate(query)
    print_result(result)
