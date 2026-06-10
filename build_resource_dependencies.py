"""
build_resource_dependencies.py  (PROTOTYPE - O1 + O2)

Builds a *corrected* RESOURCE_DEPENDENCIES from the per-resource schema
(schema/resource_schema.json produced by extract_resource_schema()).

Two corrections vs the current auto_dependency_map.py:

  O1 (direction):  only CONFIGURABLE ARGUMENTS create edges. Computed/exported
                   attributes (aws_vpc.default_route_table_id, ...) are NOT
                   arguments, so they can never produce a (reversed) edge.
                   => "X depends on Y" iff X has an input argument that takes
                      Y's id/arn/name. No more vpc -> route_table inversions,
                      no more cycles.

  O2 (hard/opt):   classification comes from the schema's `required` flag, not
                   a heuristic. required ref-arg -> hard; optional -> optional.

Pure/deterministic, no terraform dependency; feed it the schema dict.
"""
from __future__ import annotations

# Order matters: try plural/longer suffixes first.
REFERENCE_SUFFIXES = ("_ids", "_arns", "_names", "_id", "_arn", "_name")

# Stems whose `aws_<stem>` form isn't the real resource name.
STEM_ALIASES = {
    "role": "aws_iam_role",
    "execution_role": "aws_iam_role",
    "node_role": "aws_iam_role",
    "task_role": "aws_iam_role",
    "service_role": "aws_iam_role",
    "security_group": "aws_security_group",
    "vpc_security_group": "aws_security_group",
    "db_subnet_group": "aws_db_subnet_group",
}


def _resolve(arg_name: str, known: set) -> str | None:
    """Resolve a reference-style argument name to the resource it targets."""
    for suf in REFERENCE_SUFFIXES:
        if arg_name.endswith(suf):
            stem = arg_name[: -len(suf)]
            direct = "aws_" + stem
            if direct in known:
                return direct
            alias = STEM_ALIASES.get(stem)
            if alias and alias in known:
                return alias
            return None
    return None


def build_dependencies(resource_schema: dict) -> dict:
    known = set(resource_schema)
    deps: dict = {}

    for entity, schema in resource_schema.items():
        hard: list = []
        optional: list = []

        # ARGUMENTS ONLY - extract_resource_schema() already excluded
        # computed-only attributes, so reversed edges are impossible.
        for arg, meta in schema.get("arguments", {}).items():
            target = _resolve(arg, known)
            if not target or target == entity:
                continue
            if meta.get("required"):
                hard.append(target)
            else:
                optional.append(target)

        deps[entity] = {
            "hard": sorted(dict.fromkeys(hard)),
            "optional": sorted(dict.fromkeys(optional)),
        }

    return deps
