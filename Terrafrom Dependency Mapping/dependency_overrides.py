"""
dependency_overrides.py

The ONE curated layer on top of the schema-derived map. Holds only what the
Terraform schema genuinely cannot express:
  - ADD_EDGES   : planner-required intent (schema marks them optional/ambiguous)
  - REMOVE_EDGES: break genuine semantic cycles (mutual references)
  - REVERSE_EDGES: sugar for REMOVE(a->b)+ADD(b->a) (rarely needed)

NOT for builder bugs (fix those in build_resource_dependencies.py).
Keep this SMALL and benchmark-scoped — every entry is hand-maintained debt.

This REPLACES the ordering-relevant parts of ARCHITECTURE_COMPLETIONS:
edges here affect closure + topo ordering + reference_context, which
completions never did.
"""
from __future__ import annotations

# src -> [(dst, kind)]  kind in {"hard", "optional"}
ADD_EDGES = {
    # ECS: cluster/task_definition are string-typed, ambiguous bare names ->
    # unresolvable structurally, but hard planner deps (must exist + ordered first).
    "aws_ecs_service": [
        ("aws_ecs_cluster", "hard"),
        ("aws_ecs_task_definition", "hard"),
    ],
    # LB: schema says subnets/subnet_mapping optional, but no ALB exists without
    # networking. hard => expand_entities pulls subnet (and transitively vpc).
    "aws_lb": [
        ("aws_subnet", "hard"),
        ("aws_security_group", "optional"),
    ],
    # RDS: subnet group is schema-optional but architecturally expected.
    "aws_db_instance": [
        ("aws_db_subnet_group", "optional"),
    ],
    # Recall casualty from dropping the endswith resolver (certificate_authority_arn).
    "aws_acm_certificate": [
        ("aws_acmpca_certificate_authority", "optional"),
    ],
}

# src -> [dst, ...]   remove these edges entirely
REMOVE_EDGES = {
    # Break the genuine instance<->network_interface mutual reference.
    # Keep instance -> network_interface; drop the attachment.instance back-edge.
    "aws_network_interface": ["aws_instance"],
    # Belt-and-suspenders if the builder route-skip isn't applied:
    "aws_route_table": ["aws_route"],
}

# src -> [dst, ...]   flip a->b into b->a (optional). Usually unnecessary.
REVERSE_EDGES = {}

def apply_overrides(deps: dict) -> dict:
    """Return a NEW dependency map with overrides applied (build-time)."""
    out = {
        k: {"hard": list(v.get("hard", [])), "optional": list(v.get("optional", []))}
        for k, v in deps.items()
    }

    def _node(name):
        return out.setdefault(name, {"hard": [], "optional": []})

    def _drop(src, dst):
        n = out.get(src)
        if not n:
            return
        for bucket in ("hard", "optional"):
            if dst in n[bucket]:
                n[bucket].remove(dst)

    # REMOVE
    for src, targets in REMOVE_EDGES.items():
        for dst in targets:
            _drop(src, dst)

    # REVERSE
    for src, targets in REVERSE_EDGES.items():
        for dst in targets:
            _drop(src, dst)
            n = _node(dst)
            if src not in n["hard"] and src not in n["optional"]:
                n["optional"].append(src)

    # ADD
    for src, items in ADD_EDGES.items():
        n = _node(src)
        for dst, kind in items:
            other = "optional" if kind == "hard" else "hard"
            if dst in n[other]:
                n[other].remove(dst)
            if dst not in n[kind]:
                n[kind].append(dst)

    # normalize: dedup, hard wins over optional, sort
    for v in out.values():
        v["hard"] = sorted(dict.fromkeys(v["hard"]))
        hard_set = set(v["hard"])
        v["optional"] = sorted(d for d in dict.fromkeys(v["optional"]) if d not in hard_set)

    return out
