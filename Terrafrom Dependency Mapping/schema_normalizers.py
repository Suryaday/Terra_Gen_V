"""
schema_normalizers.py  (PROTOTYPE / additive)

Schema-driven replacements for the hand-maintained normalizer zoo. Each function
consults schema_index (provider ground truth) instead of per-resource tables.
All functions are no-ops when the schema is unavailable or the resource/field is
unknown, so wiring them in cannot regress the current pipeline.

PoC scope: top-level fields (covers volume, capacity_provider_strategy, etc.).
Nested-block reshaping (e.g. aws_lb_listener default_action.forward) is a
follow-up once the top-level layer is validated against the passing benchmark.
"""
from __future__ import annotations

import logging
import re

import schema_index

logger = logging.getLogger(__name__)

_ASSIGN = re.compile(r"^([a-z][a-z0-9_]*)\s*=")


def drop_block_as_argument(entity: str, hcl: str) -> str:
    """
    Generalizes every BLOCK_ONLY denylist: if a TOP-LEVEL field is emitted as a
    scalar argument (`field = ...`) but the schema says it's a nested block, the
    line is invalid -> drop it. Whitespace-tolerant; only acts at brace depth 1.
    """
    if not schema_index.resource(entity):
        return hcl

    out: list[str] = []
    depth = 0
    for line in hcl.splitlines():
        stripped = line.strip()
        drop = False
        if depth == 1 and "{" not in stripped:
            m = _ASSIGN.match(stripped)
            if m:
                field = m.group(1)
                if schema_index.is_block(entity, field) and not schema_index.is_argument(entity, field):
                    logger.info("SCHEMA DROP block-as-arg: %s.%s", entity, field)
                    drop = True
        if not drop:
            out.append(line)
        depth += line.count("{") - line.count("}")
    return "\n".join(out)


def missing_required_blocks(entity: str, hcl: str) -> list[str]:
    """
    Returns required blocks (min_items>0) that are absent from the generated HCL.
    Drives required-block injection (viewer_certificate, default_action, ...)
    from schema instead of one injector per resource.
    """
    missing = []
    for block in schema_index.required_blocks(entity):
        if not re.search(rf"\b{re.escape(block)}\s*\{{", hcl):
            missing.append(block)
    return missing


def invalid_attribute_refs(hcl: str, generated_types: set[str]) -> list[tuple[str, str, str]]:
    """
    Finds references `aws_TYPE.label.attr` where TYPE is a generated resource and
    `attr` is NOT a valid exported attribute per schema. Powers attribute
    correction / dangling-ref rewrite (aws_key_pair.x.name, redrive_policy.x.arn).
    Returns (full_ref, type, attr).
    """
    bad = []
    for rtype, label, attr in re.findall(r"\b(aws_[a-z0-9_]+)\.([a-z0-9_]+)\.([a-z0-9_]+)", hcl):
        if rtype not in generated_types:
            continue
        valid = schema_index.valid_attributes(rtype)
        if valid and attr not in valid:
            bad.append((f"{rtype}.{label}.{attr}", rtype, attr))
    return bad


def infer_var_types(entity: str, hcl: str) -> dict[str, str]:
    """
    Maps `var.NAME` to a ground-truth HCL type by looking at which schema argument
    it's assigned to (`arg = var.NAME`). Replaces suffix-guessing in
    infer_variable_type for the args we can resolve.
    """
    result: dict[str, str] = {}
    for arg, var_name in re.findall(r"([a-z][a-z0-9_]*)\s*=\s*var\.([a-z0-9_]+)", hcl):
        hcl_type = schema_index.tf_type_to_hcl(schema_index.argument_type(entity, arg))
        if hcl_type:
            result[var_name] = hcl_type
    return result
