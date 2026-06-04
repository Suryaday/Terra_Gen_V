from __future__ import annotations

import logging
import os
import re
import textwrap

from collections import defaultdict, deque, Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

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

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

INDEX_FILE = Path("vectorstore/bm25.pkl").resolve()

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2048"))

_client: Optional[OpenAI] = None

RESOURCE_ALIASES = {
    "aws_alb": "aws_lb",
    "aws_alb_listener": "aws_lb_listener",
    "aws_alb_target_group": "aws_lb_target_group",
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

    candidates.sort(
        key=lambda r: SECTION_PRIORITY.get(r["metadata"].get("section", "").lower(), 50))
    
    for row in candidates:
        print("What Chunks are being generated:") 
        print(row["chunk_id"], row["metadata"].get("section"))
    
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
    logger.info("ENTITY_ROWS_FINAL=%s", [r.chunk_id for r in filtered])
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
        }
    return _corrector


def _get_known_entities() -> set[str]:
    _get_corrector()
    return _known_entities


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

    arch_entities = [RESOURCE_ALIASES.get(e, e) for e in arch_entities]

    arch_entities = validate_entities(arch_entities, known)

    logger.info("ARCH BEFORE COMPLETION: %s", arch_entities)

    arch_entities = complete_architecture(arch_entities)
    arch_entities = [RESOURCE_ALIASES.get(e, e) for e in arch_entities]
    arch_entities = validate_entities(arch_entities, known)

    logger.info("Architecture entities after completion: %s", arch_entities)

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

    root_entities = validate_entities(root_entities, known)

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
    all_entities = [e for e in all_entities if e in known]

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

    #30 May
    logger.info("GLOBAL ROWS FOR %s", node.entity)

    for row in global_rows:

        if row.metadata.get("entity") == node.entity:

            logger.info("GLOBAL | %s | %s", row.chunk_id, row.metadata.get("section"))

    entity_rows = [r for r in filtered_rows if r.metadata.get("entity") == node.entity]
    
    #30 May
    logger.info("%s AFTER XYZ FILTER=%s", node.entity, len(filtered_rows))

    logger.info("%s entity_rows=%s dep_rows=%s", node.entity, len(entity_rows), len(filtered_rows) - len(entity_rows))

    if not entity_rows:

        logger.warning("Global retrieval missed %s", node.entity,)

        bm25 = _get_bm25()

        #30 MAY
        #fallback_rows = bm25.retrieve(node.entity, filters={"entity": node.entity}, k=5)

        fallback_rows = retrieve_entity_rows(node.entity, bm25, k=4)

        filtered_rows.extend(fallback_rows)

        for r in fallback_rows:

            logger.info("FALLBACK %s metadata_id=%s", r.chunk_id, id(r.metadata))

        r.metadata["_dependency"] = True

    logger.info("%s -> rows=%s", node.entity, len(filtered_rows))

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

    reference_context = build_dependency_reference_context(node, symbol_table)

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

    logger.info("Context chars for %s = %s", node.entity, len(final_context))

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
19. Generate all required arguments. Include optional arguments only when supported by the provided context.
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

26. Only use arguments explicitly present in the Argument Reference sections of the provided context. Do not invent deprecated or legacy Terraform arguments.

Use the exact Terraform Resource Type and Terraform Resource Label provided above."""


# ======================================================
# RESOURCE GENERATION
# ======================================================

def _extract_var_refs(hcl: str) -> list[str]:
    return sorted(set(re.findall(r"var\.([a-z0-9_]+)", hcl)))


def generate_resource(query: str, node: ResourceNode, context: str, symbol_table: dict[str, str]) -> GeneratedBlock:
  
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
        response = client.chat.completions.create(
            
            model=OPENAI_MODEL, 

            max_completion_tokens=MAX_TOKENS,

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

    except Exception as exc:
        logger.error("Generation failed for %s: %s", node.entity, exc)
        raw = f'# ERROR generating {node.entity}: {exc}'

    # Strip accidental markdown fences
    raw = re.sub(r"^```[a-z]*\n?", "", raw)
    raw = re.sub(r"\n?```$", "", raw)
    raw = raw.strip()

    var_refs = _extract_var_refs(raw)
    #symbol_table[node.entity] = (f"{node.entity}.{node.label}")
    symbol_table[node.entity] = node.label
    logger.info("SYMBOL TABLE NOW=%s", symbol_table)

    logger.info("Generated %s — vars: %s", node.entity, var_refs)

    logger.info("\n===== RAW MODEL OUTPUT =====\n%s\n============================", raw)
    logger.info("OUTPUT LENGTH=%s", len(raw))

    return GeneratedBlock(
        entity=node.entity,
        label=node.label,
        hcl=raw,
        var_refs=var_refs,
    )

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
}

def infer_variable_type(var_name: str) -> tuple[str, str | None]:

    var = var_name.lower()

    EXACT_TYPE_OVERRIDES = {
        "enable_ecs_managed_tags": "bool",
        "enable_xff_client_port": "bool",
        "requires_compatibilities": "list(string)",
        "aliases": "set(string)",
        "allowed_methods": "set(string)",
        "cached_methods": "set(string)",
        "locations": "set(string)",
        "stage_variables": "map(string)",
        "multi_az": "bool",
        "publicly_accessible": "bool",
        "enable_dns_support": "bool",
        "enable_dns_hostnames": "bool",
        "assign_generated_ipv6_cidr_block": "bool",
        "copy_tags_to_snapshot": "bool",
    }

    for key, tf_type in EXACT_TYPE_OVERRIDES.items():

        if key in var:

            return (tf_type, None)

    if any(x in var for x in (
        "desired_size",
        "min_size",
        "max_size",
        "disk_size",
        "retention_days",
        "count",
    )):
        return ("number", None)

    if any(x in var for x in (
        "enabled",
        "enable_",
        "private_access",
        "public_access",
        "publicly_accessible",
        "multi_az",
        "encrypted",
        "force_detach"
    )):
        return ("bool", None)

    if any(x in var for x in (
        "instance_types",
        "subnet_ids",
        "security_group_ids",
        "availability_zones",
        "managed_policy_arns",
    )):
        return ("list(string)", None)
    
    #30 May
    if var_name.endswith(("_enabled", "_encrypted")):
        return ("bool", None)

    if var_name.endswith(("_size", "_count", "_port")):
        return ("number", None)

    if var_name.startswith("associate_"):
        return ("bool", None)
    
    if var == "propagate_tags":
        return ("string", None)

    LIST_HINTS = (
        "_ids",
        "_arns",
        "_cidr_blocks",
        "_subnet_ids",
        "_security_group_ids",
        "_availability_zones",
        "_subnets",
        "_security_groups",
        "_cidrs",
    )

    MAP_HINTS = (
        "tags",
        "environment_variables",
        "environment_vars",
        "labels",
        "metadata",
        "annotations",
    )

    if any(
        hint in var 
        for hint in (
            "requires_compatibilities",
            "allowed_methods",
            "cached_methods",
            "locations",
            "security_groups",
            "api_gateway_endpoint_types",
        )
    ):
        return ("list(string)", None)

    if "stage_variables" in var:
        return ("map(string)", None)

    if "copy_tags_to_snapshot" in var:
        return ("bool", None)
    
    if var.endswith("_security_group_ids"):
        return ("list(string)", None)

    if var.endswith("_subnet_ids"):
        return ("list(string)", None)

    if var.endswith("_cidrs"):
        return ("list(string)", None)
    
    if var.endswith("_arns"):
        return ("list(string)", None)
    
    if var.endswith("_health_check"):
        return ("map(string)", None)

    if any(var.endswith(hint) for hint in LIST_HINTS):

        return ("list(string)", None)

    if any(hint in var for hint in MAP_HINTS):

        return ("map(string)", None)

    return ("string", None)

def _generate_variables_tf(all_var_refs: list[str]) -> str:
    blocks: list[str] = []

    for var_name in sorted(set(all_var_refs)):
        known = _KNOWN_VARS.get(var_name)

        if known:
            vtype, default, description = known
            block = (
                f'variable "{var_name}" {{\n'
                f'  description = "{description}"\n'
                f'  type        = {vtype}\n'
                f'  default     = {default}\n'
                f'}}'
            )
        else:
            # Generic fallback for unknown variables
            inferred_type, default = infer_variable_type(var_name)

            block = (
                f'variable "{var_name}" {{\n'
                f'  description = "TODO: describe {var_name}"\n'
                f'  type        = {inferred_type}\n'
            )

            if default is not None:
                 block += (f'  default     = {default}\n')

            block += "}"

        blocks.append(block)

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
      version = "~> 5.0"
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
    for block in blocks:
        all_vars.extend(block.var_refs)

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
        "variables.tf":  _generate_variables_tf(all_vars),
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

    for node in plan.ordered_nodes:
        context = assemble_context(query=query, node=node, symbol_table=symbol_table, global_rows=global_rows)
        block = generate_resource(query, node, context, symbol_table)
        blocks.append(block)

    # 3. Stitch into files
    files = stitch(blocks, plan)

    # 4. Validate
    warnings = validate(files)
    if warnings:
        for w in warnings:
            logger.warning("Validation: %s", w)

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

    for filename, content in result.files.items():
        print(f"\n{'─' * 30} {filename} {'─' * 30}\n")
        print(content)


# ======================================================
# ENTRY POINT
# ======================================================

if __name__ == "__main__":
    import sys

    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "create EKS cluster with node group"
    result = generate(query)
    print_result(result)
