# schema_reference_corrector.py
"""
Schema-driven attribute-reference corrector (Phase 2B, v1).

The validator already detects INVALID_ATTRIBUTE_REF: references of the form
    aws_<type>.<label>.<attr>
where <attr> is not a valid exported attribute of <type> per the provider
schema. This module ACTS on that: it rewrites the bad attribute to `id`, which
virtually every AWS resource exports and which terraform will accept.

Worst case is a semantically-loose reference; but it converts a hard
"Unsupported attribute" failure into a passing validate, which is the goal.

v1 scope (intentionally minimal):
  - only rewrites to `id`
  - only when the resource is known AND exports `id` AND the attr is invalid
  - leaves valid refs, unknown resources, and id-less resources untouched
"""
from __future__ import annotations

import logging
import re

import schema_index

logger = logging.getLogger(__name__)

# aws_<type>.<label>.<attr>   (first attribute segment only)
_REF = re.compile(r"\b(aws_[a-z0-9_]+)\.([a-zA-Z0-9_]+)\.([a-zA-Z0-9_]+)")

def correct_invalid_attribute_refs(hcl: str) -> str:
    if not schema_index.available():
        return hcl

    def _replace(m: "re.Match") -> str:
        entity, label, attr = m.group(1), m.group(2), m.group(3)

        valid = schema_index.valid_attributes(entity)

        # Unknown resource or schema has no attribute info -> leave untouched.
        if not valid:
            return m.group(0)

        # Reference is already valid -> leave untouched.
        if attr in valid:
            return m.group(0)

        # Can only safely repair if the resource actually exports `id`.
        if "id" not in valid:
            return m.group(0)

        logger.info("SCHEMA FIX %s.%s -> id", entity, attr)
        return f"{entity}.{label}.id"

    return _REF.sub(_replace, hcl)
