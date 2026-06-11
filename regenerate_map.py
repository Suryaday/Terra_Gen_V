"""
regenerate_map.py  (VERIFICATION HARNESS - does NOT touch the runtime)

Purpose:
  1. Reads schema/resource_schema.json (produced by generate_dependency_map.py)
  2. Builds RESOURCE_DEPENDENCIES_V2 using arguments-only + required-flag logic
  3. Diffs V1 (current auto_dependency_map.py) vs V2:
       - Cycle count (Tarjan)
       - Total edge count
       - DROPPED edges (in V1 but not V2)  ← regression risk check
       - ADDED edges (in V2 but not V1)
       - INVERTED edges (A→B in V1, B→A in V2)
  4. Writes auto_dependency_map.candidate.py (V2) for inspection

Run:
  python regenerate_map.py

Requires:
  - schema/resource_schema.json (run generate_dependency_map.py first)
  - auto_dependency_map.py (current V1 - already in repo)
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

from build_resource_dependencies import build_dependencies

try:
    from auto_dependency_map import RESOURCE_DEPENDENCIES as V1
except ImportError:
    print("ERROR: cannot import auto_dependency_map.RESOURCE_DEPENDENCIES (V1)")
    sys.exit(1)

SCHEMA_FILE = Path("schema/resource_schema.json")

if not SCHEMA_FILE.exists():
    print(f"ERROR: {SCHEMA_FILE} not found.")
    print("Run:  cd 'Terrafrom Dependency Mapping' && python generate_dependency_map.py")
    print("Then copy schema/resource_schema.json to the project root schema/ dir.")
    sys.exit(1)


# ======================================================
# BUILD V2
# ======================================================

schema = json.loads(SCHEMA_FILE.read_text(encoding="utf-8"))
V2 = build_dependencies(schema)

print(f"V1 resources: {len(V1)}")
print(f"V2 resources: {len(V2)}")


# ======================================================
# CYCLE DETECTION (Tarjan's SCC)
# ======================================================

def _build_graph(dmap: dict) -> dict[str, set[str]]:
    g: dict[str, set[str]] = defaultdict(set)
    for entity, d in dmap.items():
        for dep in list(d.get("hard", [])) + list(d.get("optional", [])):
            if dep in dmap:
                g[entity].add(dep)
    return g


def _tarjan_sccs(g: dict[str, set[str]]) -> list[list[str]]:
    index_counter = [0]
    stack = []
    lowlink = {}
    index = {}
    on_stack = {}
    sccs = []

    def strongconnect(v):
        index[v] = index_counter[0]
        lowlink[v] = index_counter[0]
        index_counter[0] += 1
        stack.append(v)
        on_stack[v] = True

        for w in sorted(g.get(v, [])):
            if w not in index:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif on_stack.get(w, False):
                lowlink[v] = min(lowlink[v], index[w])

        if lowlink[v] == index[v]:
            scc = []
            while True:
                w = stack.pop()
                on_stack[w] = False
                scc.append(w)
                if w == v:
                    break
            if len(scc) > 1:
                sccs.append(sorted(scc))

    for v in sorted(g):
        if v not in index:
            strongconnect(v)

    return sccs


def _edge_set(dmap: dict) -> set[tuple[str, str]]:
    edges = set()
    for entity, d in dmap.items():
        for dep in list(d.get("hard", [])) + list(d.get("optional", [])):
            edges.add((entity, dep))
    return edges


# ======================================================
# ANALYSIS
# ======================================================

g1 = _build_graph(V1)
g2 = _build_graph(V2)

sccs1 = _tarjan_sccs(g1)
sccs2 = _tarjan_sccs(g2)

e1 = _edge_set(V1)
e2 = _edge_set(V2)

dropped = e1 - e2
added = e2 - e1
inverted = {(a, b) for (a, b) in dropped if (b, a) in e2}

print(f"\n{'='*70}")
print(f"V1 edges: {len(e1)}   cycles (SCCs > 1): {len(sccs1)}")
print(f"V2 edges: {len(e2)}   cycles (SCCs > 1): {len(sccs2)}")
print(f"{'='*70}")

print(f"\nDROPPED (in V1 not V2): {len(dropped)}")
print(f"ADDED   (in V2 not V1): {len(added)}")
print(f"INVERTED (A→B became B→A): {len(inverted)}")

if sccs1:
    print(f"\nV1 CYCLES ({len(sccs1)} SCCs):")
    for scc in sccs1[:10]:
        print(f"  {scc}")
    if len(sccs1) > 10:
        print(f"  ... and {len(sccs1) - 10} more")

if sccs2:
    print(f"\nV2 CYCLES ({len(sccs2)} SCCs):")
    for scc in sccs2[:10]:
        print(f"  {scc}")
else:
    print("\nV2 CYCLES: NONE ✓")

# Focus resources
FOCUS = [
    "aws_vpc", "aws_subnet", "aws_route_table", "aws_route_table_association",
    "aws_internet_gateway", "aws_security_group", "aws_db_subnet_group",
    "aws_db_instance", "aws_iam_role", "aws_lb_listener", "aws_ecs_service",
    "aws_eks_cluster", "aws_lb",
]

print(f"\n{'='*70}")
print("FOCUS RESOURCE COMPARISON (V1 vs V2)")
print(f"{'='*70}")
for r in FOCUS:
    d1 = V1.get(r, {})
    d2 = V2.get(r, {})
    h1 = sorted(d1.get("hard", []))
    o1 = sorted(d1.get("optional", []))
    h2 = sorted(d2.get("hard", []))
    o2 = sorted(d2.get("optional", []))
    if h1 != h2 or o1 != o2:
        print(f"\n  {r}")
        print(f"    V1 hard={h1}")
        print(f"    V2 hard={h2}")
        print(f"    V1 optional={o1}")
        print(f"    V2 optional={o2}")

# Dropped edges for focus resources (regression risk)
focus_dropped = [(a, b) for (a, b) in dropped if a in FOCUS or b in FOCUS]
if focus_dropped:
    print(f"\n{'='*70}")
    print(f"DROPPED EDGES involving focus resources ({len(focus_dropped)}):")
    print(f"{'='*70}")
    for a, b in sorted(focus_dropped)[:30]:
        print(f"  {a} -> {b}")
    if len(focus_dropped) > 30:
        print(f"  ... and {len(focus_dropped) - 30} more")


# ======================================================
# WRITE CANDIDATE
# ======================================================

out_file = Path("auto_dependency_map.candidate.py")
with open(out_file, "w") as f:
    f.write("# AUTO-GENERATED TERRAFORM DEPENDENCY MAP (V2 - arguments only, required-aware)\n")
    f.write("# DO NOT EDIT MANUALLY\n\n")
    f.write("RESOURCE_DEPENDENCIES = ")
    json.dump(V2, f, indent=4, sort_keys=True)
    f.write("\n")

print(f"\nCandidate map written to: {out_file}")
print("Done.")
