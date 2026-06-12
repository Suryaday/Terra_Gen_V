"""
schema_normalizer_v2.py — Schema-driven normalizer (production).

normalize_block_vs_argument():
  Uses schema_index to detect top-level fields emitted as `arg = value` that
  are actually nested blocks, and DROPS them. Replaces ALL per-resource
  BLOCK_ONLY tables:
    - _normalize_ecs_task_definition_blocks (volume, placement_constraints)
    - _normalize_ecs_capacity_provider (network_configuration)
    - SCHEMA_RULES block_only sets
    - any future block-vs-argument fix

Wire AFTER existing normalizers in generate_resource() so it catches anything
they miss, then progressively DELETE the hand tables as the schema proves stable.

Also: infer_variable_type_from_schema():
  Ground-truth variable typing from schema argument types. Falls back to the
  existing heuristic when schema doesn't know.
"""
from __future__ import annotations

import re
import logging

import schema_index

logger = logging.getLogger(__name__)

_ASSIGN = re.compile(r"^([a-z][a-z0-9_]*)\s*=")

def normalize_block_vs_argument(entity: str, hcl: str) -> str:
    """
    Drop any top-level `field = value` line where schema says `field` is a
    nested block (not an argument). Whitespace-tolerant, depth-aware.

    Only acts at brace-depth 1 (top level of the resource block).
    Only drops lines WITHOUT `{` (so actual block openers aren't touched).
    """
    if not schema_index.available():
        return hcl

    if not schema_index.get_resource_schema(entity):
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
                    logger.info("SCHEMA: dropped block-as-arg %s.%s", entity, field)
                    drop = True

        if not drop:
            out.append(line)

        depth += line.count("{") - line.count("}")

    return "\n".join(out)

def infer_variable_type_from_schema(entity: str, arg_name: str, var_name: str) -> str | None:
    """
    Given that `arg_name = var.var_name` was emitted for `entity`, look up the
    schema-declared type and convert to HCL type string.

    Returns None if schema doesn't know (caller falls back to heuristic).

    Usage in _generate_variables_tf:
        schema_type = infer_variable_type_from_schema(entity, arg, var_name)
        if schema_type:
            return (schema_type, None)
        # else fall back to infer_variable_type(var_name)
    """
    tf_type = schema_index.get_argument_type(entity, arg_name)
    if tf_type is None:
        return None
    return schema_index.tf_type_to_hcl(tf_type)
