"""
schema_index.py

Runtime, read-only index over the Terraform AWS provider schema produced by
`Terrafrom Dependency Mapping/generate_dependency_map.py` (-> schema/resource_schema.json).

This is the ground-truth source that lets correction be deterministic instead of
hand-maintained. It is intentionally SAFE: if the schema file is absent, every
query degrades to "unknown" (None / empty / False) so callers no-op and the
existing pipeline behaves exactly as before.

Schema entry shape (per resource):
    {
      "arguments":  {name: {"type": <tf_type>, "required": bool}},
      "blocks":     {name: {"required": bool, "min_items": int, "max_items": int,
                            "arguments": {...}, "blocks": {...}, "attributes": [...]}},
      "attributes": [name, ...]   # every readable/exported attribute
    }
"""
from __future__ import annotations

import functools
import json
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

# Primary path (generated). Falls back to the committed sample so the layer is
# demonstrable without running terraform.
_CANDIDATES = [
    Path(os.getenv("RESOURCE_SCHEMA_FILE", "schema/resource_schema.json")),
    Path("schema/resource_schema.sample.json"),
]


@functools.lru_cache(maxsize=1)
def _load() -> dict:
    for path in _CANDIDATES:
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                logger.info("schema_index loaded %s resources from %s", len(data), path)
                return data
            except Exception:
                logger.exception("schema_index failed to load %s", path)
    logger.warning("schema_index: no schema file found; all lookups will no-op")
    return {}


def available() -> bool:
    return bool(_load())


def resource(entity: str) -> dict | None:
    return _load().get(entity)


def is_known(entity: str) -> bool:
    return entity in _load()


def is_block(entity: str, field: str) -> bool:
    r = resource(entity)
    return bool(r and field in r.get("blocks", {}))


def is_argument(entity: str, field: str) -> bool:
    r = resource(entity)
    return bool(r and field in r.get("arguments", {}))


def required_blocks(entity: str) -> list[str]:
    r = resource(entity) or {}
    return [name for name, b in r.get("blocks", {}).items() if b.get("required")]


def valid_attributes(entity: str) -> set[str]:
    r = resource(entity)
    return set(r.get("attributes", [])) if r else set()


def argument_type(entity: str, name: str) -> object | None:
    r = resource(entity)
    if not r:
        return None
    arg = r.get("arguments", {}).get(name)
    return arg.get("type") if arg else None


def tf_type_to_hcl(tf_type) -> str | None:
    """
    Convert a Terraform JSON type into the HCL type string this project uses.
      "string"            -> "string"
      ["set","string"]    -> "set(string)"
      ["list","string"]   -> "list(string)"
      ["map","string"]    -> "map(string)"
      ["list",[...obj...]] -> "list(any)"
    """
    if tf_type is None:
        return None
    if isinstance(tf_type, str):
        return tf_type
    if isinstance(tf_type, list) and tf_type:
        kind = tf_type[0]
        inner = tf_type[1] if len(tf_type) > 1 else "string"
        inner_hcl = inner if isinstance(inner, str) else "any"
        if kind in ("list", "set", "map"):
            return f"{kind}({inner_hcl})"
    return "any"
