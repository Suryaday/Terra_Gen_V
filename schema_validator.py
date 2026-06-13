"""
schema_validator.py — Pre-validate generated HCL against RESOURCE_SCHEMA.

Detects issues that would fail terraform validate, BEFORE running terraform:
  - BLOCK_AS_ARGUMENT: field emitted as `x = var.y` but schema says it's a block
  - MISSING_REQUIRED_BLOCK: a min_items>0 block not present in HCL
  - INVALID_ATTRIBUTE_REF: reference to aws_X.label.attr where attr isn't exported

Returns structured findings so the normalizer layer can act on them.
"""
from __future__ import annotations

import re
import logging
from dataclasses import dataclass
import schema_index
from schema_index import (is_block_at_path, is_argument_at_path)

logger = logging.getLogger(__name__)

_ASSIGN = re.compile(r"^([a-z][a-z0-9_]*)\s*=")

@dataclass
class Finding:
    kind: str           # BLOCK_AS_ARGUMENT | MISSING_REQUIRED_BLOCK | INVALID_ATTRIBUTE_REF
    entity: str
    field: str
    detail: str = ""

def validate_resource(entity: str, hcl: str, generated_types: set[str] | None = None) -> list[Finding]:
    """
    Validate a single resource block's HCL against schema.
    Returns list of Findings (empty = clean).
    """
    findings: list[Finding] = []

    if not schema_index.available():
        return findings

    block_stack = []

    for line in hcl.splitlines():

        stripped = line.strip()

        code = re.sub(
            r'"(?:\\.|[^"\\])*"',
            "",
            stripped
        )

        opens = code.count("{")
        closes = code.count("}")

        m = _ASSIGN.match(stripped)

        if m and "{" not in stripped:

            field = m.group(1)

            block_path = ".".join(block_stack)

            logger.info("VALIDATOR CHECK path=%s field=%s", block_path, field)

            if field in ("metric_data_queries", "metric_dimension", "metrics"):
                logger.info("BLOCK CHECK path=%s field=%s is_block=%s is_arg=%s",
                    block_path,
                    field,
                    is_block_at_path(entity, block_path, field),
                    is_argument_at_path(entity, block_path, field),
                )

            logger.info("IS_BLOCK? entity=%s path=%s field=%s result=%s", entity, block_path, field, schema_index.is_block_at_path(entity, block_path, field))

            if (schema_index.is_block_at_path(entity, block_path, field)
                and
                not schema_index.is_argument_at_path(entity, block_path, field)):

                findings.append(
                    Finding(
                        kind="BLOCK_AS_ARGUMENT",
                        entity=entity,
                        field=(
                            f"{block_path}.{field}"
                            if block_path
                            else field
                        ),
                        detail=(
                            f"{field} is a nested block, "
                            f"not a scalar argument"
                        ),
                    )
                )

        if (opens > closes and code.endswith("{") and "=" not in code):

            block_name = code[:-1].strip()

            if (block_name and not block_name.startswith("resource")):
                block_stack.append(block_name)

        net_closes = closes - opens

        for _ in range(max(0, net_closes)):
            if block_stack:
                block_stack.pop()

    # 2. MISSING_REQUIRED_BLOCK
    for block_name in schema_index.required_blocks(entity):
        if not re.search(rf"\b{re.escape(block_name)}\s*\{{", hcl):
            findings.append(Finding(
                kind="MISSING_REQUIRED_BLOCK",
                entity=entity,
                field=block_name,
                detail=f"required block '{block_name}' (min_items>0) not found in HCL",
            ))

    # 3. INVALID_ATTRIBUTE_REF (only if generated_types provided)
    if generated_types:

        logger.info("VALIDATING ATTR REFS entity=%s generated_types=%s", entity, len(generated_types))

        for rtype, label, attr in re.findall(r"\b(aws_[a-z0-9_]+)\.([a-z0-9_]+)\.([a-z0-9_]+)", hcl):
            
            logger.info("ATTR REF %s.%s.%s", rtype, label, attr)

            if rtype not in generated_types:
                continue
            valid = schema_index.valid_attributes(rtype)

            logger.info("VALID ATTRS FOR %s = %s", rtype, sorted(list(valid))[:15])
            
            if valid and attr not in valid:
                findings.append(Finding(
                    kind="INVALID_ATTRIBUTE_REF",
                    entity=entity,
                    field=f"{rtype}.{label}.{attr}",
                    detail=f"'{attr}' not in valid attributes: {sorted(valid)[:10]}...",
                ))

    return findings
