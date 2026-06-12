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

    # 1. BLOCK_AS_ARGUMENT: top-level fields assigned as scalars that are actually blocks
    depth = 0
    for line in hcl.splitlines():
        stripped = line.strip()
        if depth == 1 and "{" not in stripped:
            m = _ASSIGN.match(stripped)
            if m:
                field = m.group(1)
                if schema_index.is_block(entity, field) and not schema_index.is_argument(entity, field):
                    findings.append(Finding(
                        kind="BLOCK_AS_ARGUMENT",
                        entity=entity,
                        field=field,
                        detail=f"{field} is a nested block, not a scalar argument",
                    ))
        depth += line.count("{") - line.count("}")

    logger.info("REQUIRED BLOCKS FOR %s = %s", entity, schema_index.required_blocks(entity))   

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
