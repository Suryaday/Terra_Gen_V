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
    Drop any `field = value` line where schema says `field` is a nested block
    (not an argument), at ANY depth. Whitespace-tolerant, path/depth-aware.

    How it works:
      - Tracks the enclosing block path via a brace-balanced name stack
        (quoted strings / ${...} are stripped before counting braces, so
        interpolations and inline maps like `tags = { Name = "x" }` don't
        corrupt the depth).
      - Only considers lines that do NOT open a block on the same line, so
        real block openers and inline-map arguments are never dropped.
      - Uses schema_index.is_block_at_path / is_argument_at_path, so the
        block-vs-argument decision is correct for NESTED blocks
        (e.g. customized_metric_specification.metrics), not just top level.

    Limitation: only single-line assignments (`field = value`) are dropped. A
    multi-line RHS (e.g. `metrics = [
  {...}
]`) only has its first line
    removed; whole-structure removal is out of scope here.

    Note: `dynamic "x" {` is tracked under the literal name `dynamic`, so
    lookups inside dynamic blocks resolve to nothing and are left untouched
    (safe no-op) until dynamic-block unwrapping is handled separately.
    """
    if not schema_index.available():
        return hcl

    if not schema_index.get_resource_schema(entity):
        return hcl

    out: list[str] = []
    block_stack: list[str | None] = []

    for line in hcl.splitlines():
        stripped = line.strip()
        # ignore braces inside quoted strings / ${...} interpolations
        code = re.sub(r'"(?:\\.|[^"\\])*"', "", stripped)
        opens = code.count("{")
        closes = code.count("}")

        drop = False

        # block-as-argument: `field = value` that does NOT open a block here
        if opens == 0:
            m = _ASSIGN.match(stripped)
            if m:
                field = m.group(1)
                block_path = ".".join(n for n in block_stack if n)

                logger.info("NORMALIZER path=%s field=%s", block_path, field)
                
                if (schema_index.is_block_at_path(entity, block_path, field) and not schema_index.is_argument_at_path(entity, block_path, field)):
                    logger.info("SCHEMA: dropped block-as-arg %s.%s", entity, ".".join(p for p in (block_path, field) if p))
                    logger.info("NORMALIZER DROP entity=%s path=%s field=%s", entity, block_path, field,)
                    drop = True

        if not drop:
            out.append(line)

        # maintain the path stack (brace-balanced, string-stripped)
        if "=" not in code and code.endswith("{") and opens - closes == 1:
            head = code[:-1].strip()
            name = head.split()[0] if head else ""
            block_stack.append(None if (not name or name.startswith("resource")) else name)
        else:
            net = opens - closes
            if net > 0:
                block_stack.extend([None] * net)
            elif net < 0:
                for _ in range(-net):
                    if block_stack:
                        block_stack.pop()

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
    tf_type = schema_index.find_argument_type(entity, arg_name)
    if tf_type is None:
        return None
    return schema_index.tf_type_to_hcl(tf_type)
