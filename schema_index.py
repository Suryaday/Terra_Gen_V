"""
schema_index.py — Runtime read-only index over RESOURCE_SCHEMA.

Single source of truth for:
  - is this a block or an argument?
  - what type is this argument?
  - what are the required blocks?
  - what are the valid exported attributes?

Safe by design: if schema file is absent, every query returns None/empty/False
-> existing pipeline runs unchanged. No-op degradation.
"""
from __future__ import annotations

import functools
import json
import logging
import os
from pathlib import Path
from collections import defaultdict

logger = logging.getLogger(__name__)

SCHEMA_CONFLICTS = defaultdict(set)

_SCHEMA_PATH = Path(os.getenv("RESOURCE_SCHEMA_FILE", "schema/resource_schema.json"))

@functools.lru_cache(maxsize=1)
def _load() -> dict:
    if _SCHEMA_PATH.exists():
        try:
            data = json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))
            logger.info("schema_index: loaded %d resources from %s", len(data), _SCHEMA_PATH)
            return data
        except Exception:
            logger.exception("schema_index: failed to load %s", _SCHEMA_PATH)
    return {}

def available() -> bool:
    return bool(_load())

def get_resource_schema(entity: str) -> dict | None:
    return _load().get(entity)

def is_block(entity: str, field: str) -> bool:
    """True if `field` is a nested block (at top level) for this resource."""
    r = get_resource_schema(entity)
    return bool(r and field in r.get("blocks", {}))

def is_argument(entity: str, field: str) -> bool:
    """True if `field` is a configurable scalar/collection argument (top level)."""
    r = get_resource_schema(entity)
    return bool(r and field in r.get("arguments", {}))

def is_valid_argument(entity: str, field: str) -> bool:
    """True if field exists as EITHER argument or block (i.e. won't be 'unsupported')."""
    r = get_resource_schema(entity)
    if not r:
        return True  # unknown resource -> don't interfere
    return field in r.get("arguments", {}) or field in r.get("blocks", {})

def get_argument_type(entity: str, field: str):
    """Return the Terraform JSON type for a top-level argument, or None."""
    r = get_resource_schema(entity)
    if not r:
        return None
    arg = r.get("arguments", {}).get(field)
    return arg.get("type") if arg else None

def find_argument_type(resource: str, arg_name: str):

    schema = get_resource_schema(resource)

    if not schema:
        return None

    matches = []

    def search(node):

        arguments = node.get("arguments", {})

        if arg_name in arguments:

            arg_type = (arguments[arg_name].get("type"))

            matches.append(arg_type)

        for block in (node.get("blocks", {}).values()):
            search(block)

    search(schema)

    if not matches:
        return None

    unique = {json.dumps(x, sort_keys=True) for x in matches}

    if len(unique) > 1:

        SCHEMA_CONFLICTS[resource].add(arg_name)

        logger.warning(
            "SCHEMA TYPE CONFLICT "
            "resource=%s arg=%s "
            "matches=%s",
            resource,
            arg_name,
            matches,
        )

        return None

    return matches[0]

def get_nested_argument_type(entity: str, block_path: str, field: str):
    """
    Get type for a nested argument: block_path = "vpc_config" or "default_action.forward".
    Walks into blocks recursively.
    """
    r = get_resource_schema(entity)
    if not r:
        return None
    node = r
    for part in block_path.split("."):
        node = node.get("blocks", {}).get(part)
        if not node:
            return None
    arg = node.get("arguments", {}).get(field)
    return arg.get("type") if arg else None

def find_argument_type_by_path(entity: str, path: str):

    if "." not in path:
        return get_argument_type(entity, path)

    block_path, _, field = path.rpartition(".")

    return get_nested_argument_type(entity, block_path, field)

def required_blocks(entity: str) -> list[str]:
    """Return names of top-level blocks where min_items > 0."""
    r = get_resource_schema(entity) or {}
    return [name for name, b in r.get("blocks", {}).items() if b.get("min_items", 0) > 0]

def valid_attributes(entity: str) -> set[str]:
    """Return the set of valid exported attribute names for reference validation."""
    r = get_resource_schema(entity)
    return set(r.get("attributes", [])) if r else set()

def tf_type_to_hcl(tf_type) -> str | None:
    """
    Convert Terraform JSON type to HCL type string:
      "string"           -> "string"
      "number"           -> "number"
      "bool"             -> "bool"
      ["set","string"]   -> "set(string)"
      ["list","string"]  -> "list(string)"
      ["map","string"]   -> "map(string)"
      ["list",[...obj...]] -> "list(any)"
      ["object",{...}]   -> "map(any)"
    """
    if tf_type is None:
        return None
    if isinstance(tf_type, str):
        return tf_type
    if isinstance(tf_type, list) and tf_type:
        kind = tf_type[0]
        inner = tf_type[1] if len(tf_type) > 1 else "string"
        if kind in ("list", "set", "map"):
            inner_hcl = inner if isinstance(inner, str) else "any"
            return f"{kind}({inner_hcl})"
        if kind == "object":
            return "map(any)"
    return "any"

def print_conflict_summary():

    if not SCHEMA_CONFLICTS:
        logger.info("SCHEMA CONFLICT SUMMARY={} ")
        return

    logger.info(
        "SCHEMA CONFLICT SUMMARY=%s",
        {
            k: sorted(v)
            for k, v in SCHEMA_CONFLICTS.items()
        }
    )
