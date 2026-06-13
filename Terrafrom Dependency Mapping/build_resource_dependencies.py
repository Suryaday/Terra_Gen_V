"""
build_resource_dependencies.py  (V3: precision pass)

vs V2:
  - PRECISION RESOLVER: removed the generic "endswith-unique" rule that made
    garbage edges (ecs_service->media_store_container, db_instance->ssm_maintenance_window)
    and false cycles (transit_gateway->..._association). Resolution = strip ref
    suffix -> direct match (+singularize) -> curated alias. Nothing else.
  - INLINE-BLOCK SKIP: don't derive deps from attribute-as-block rule/target
    lists (route, ingress, egress, ...) -> kills the route/route_table/vpce cycle.
  - PROVENANCE: build_with_provenance() reports which field produced each edge,
    plus unresolved ref-suffix args (so missing edges are explainable).

Arguments-only. hard/optional from schema `required`; nested args optional unless
every ancestor block is required.

By design: bare ambiguous names (ecs_service.cluster / .task_definition) do NOT
resolve here -> they belong in the curated planner-intent layer (step 5).
"""
from __future__ import annotations

REFERENCE_SUFFIXES = ("_ids", "_arns", "_names", "_id", "_arn", "_name")

STEM_ALIASES = {
    "role": "aws_iam_role", "execution_role": "aws_iam_role",
    "node_role": "aws_iam_role", "task_role": "aws_iam_role",
    "service_role": "aws_iam_role", "iam_role": "aws_iam_role",
    "security_group": "aws_security_group",
    "vpc_security_group": "aws_security_group",
    "db_subnet_group": "aws_db_subnet_group",
    "load_balancer": "aws_lb", "lb": "aws_lb",
    "target_group": "aws_lb_target_group",
    "allocation": "aws_eip",
}

INLINE_TARGET_BLOCKS = {
    "route", "ingress", "egress", "cors_rule",
    "lifecycle_rule", "ordered_cache_behavior",
}

def _strip_ref_suffix(arg_name):
    for suf in REFERENCE_SUFFIXES:
        if arg_name.endswith(suf):
            return arg_name[: -len(suf)], True
    return arg_name, False

def _singularize(stem):
    return stem[:-1] if stem.endswith("s") and not stem.endswith("ss") else stem

def _resolve(arg_name, known):
    stem, _ = _strip_ref_suffix(arg_name)
    for cand in (stem, _singularize(stem)):
        direct = "aws_" + cand
        if direct in known:
            return direct
        alias = STEM_ALIASES.get(cand)
        if alias and alias in known:
            return alias
    return None

def _walk(node, parent_required, known, entity, edges, path):
    for arg, meta in node.get("arguments", {}).items():
        if arg in INLINE_TARGET_BLOCKS:        # <-- add this guard
            continue
        field_path = f"{path}.{arg}" if path else arg
        target = _resolve(arg, known)
        if target and target != entity:
            kind = "hard" if (parent_required and meta.get("required", False)) else "optional"
            edges.append((target, kind, field_path))
        elif target is None and _strip_ref_suffix(arg)[1]:
            edges.append((None, "unresolved", field_path))
    for bname, block in node.get("blocks", {}).items():
        if bname in INLINE_TARGET_BLOCKS:
            continue
        child = f"{path}.{bname}" if path else bname
        _walk(block, parent_required and bool(block.get("required", False)),
              known, entity, edges, child)

def build_with_provenance(resource_schema):
    known = set(resource_schema)
    deps, provenance = {}, {}
    for entity, schema in resource_schema.items():
        edges = []
        _walk(schema, True, known, entity, edges, "")
        provenance[entity] = edges
        hard = [t for (t, k, _) in edges if k == "hard"]
        optional = [t for (t, k, _) in edges if k == "optional"]
        hard_u = sorted(dict.fromkeys(hard))
        hard_set = set(hard_u)
        opt_u = sorted({d for d in optional if d not in hard_set})
        deps[entity] = {"hard": hard_u, "optional": opt_u}
    return deps, provenance

def build_dependencies(resource_schema):
    deps, _ = build_with_provenance(resource_schema)
    return deps
