"""
dependency_diff_demo.py  (PROTOTYPE)

Shows O1+O2: builds a corrected RESOURCE_DEPENDENCIES from the schema and diffs
it against the CURRENT auto_dependency_map.py, then runs a cycle check + topo
sort on a VPC/RDS node set for BOTH maps.

Run:  python dependency_diff_demo.py
"""
import json
from pathlib import Path

from build_resource_dependencies import build_dependencies

try:
    from auto_dependency_map import RESOURCE_DEPENDENCIES as CURRENT
except Exception as exc:  # pragma: no cover
    print("WARN: could not import current map:", exc)
    CURRENT = {}

SCHEMA = json.loads(Path("schema/dependency_sample.json").read_text())
CORRECTED = build_dependencies(SCHEMA)

NODES = [
    "aws_vpc", "aws_subnet", "aws_route_table", "aws_route_table_association",
    "aws_internet_gateway", "aws_security_group", "aws_db_subnet_group",
    "aws_db_instance", "aws_iam_role",
]


def edges(dmap, nodes):
    """n -> set(deps): 'n depends on dep' (hard+optional), restricted to nodes."""
    nodeset = set(nodes)
    g = {n: set() for n in nodes}
    for n in nodes:
        d = dmap.get(n, {}) or {}
        for dep in list(d.get("hard", [])) + list(d.get("optional", [])):
            if dep in nodeset and dep != n:
                g[n].add(dep)
    return g


def find_cycle(g):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {n: WHITE for n in g}

    def dfs(n, stack):
        color[n] = GRAY
        for m in sorted(g[n]):
            if color[m] == GRAY:
                return stack + [n, m]
            if color[m] == WHITE:
                r = dfs(m, stack + [n])
                if r:
                    return r
        color[n] = BLACK
        return None

    for n in sorted(g):
        if color[n] == WHITE:
            r = dfs(n, [])
            if r:
                return r
    return None


def topo(g):
    # dependencies first
    indeg = {n: len(g[n]) for n in g}
    order, queue = [], sorted([n for n in g if indeg[n] == 0])
    dependents = {n: [m for m in g if n in g[m]] for n in g}
    while queue:
        n = queue.pop(0)
        order.append(n)
        for m in dependents[n]:
            indeg[m] -= 1
            if indeg[m] == 0:
                queue.append(m)
        queue.sort()
    return order if len(order) == len(g) else None


def show_map(name, dmap):
    print(f"\n{name}")
    for n in ["aws_vpc", "aws_subnet", "aws_route_table", "aws_db_instance"]:
        d = dmap.get(n, {}) or {}
        print(f"  {n:30s} hard={d.get('hard', [])}  optional={d.get('optional', [])}")
    g = edges(dmap, NODES)
    cyc = find_cycle(g)
    if cyc:
        print(f"  CYCLE: {' -> '.join(cyc)}")
    else:
        print(f"  NO CYCLE. topo order = {topo(g)}")


show_map("=== CURRENT (auto_dependency_map.py) ===", CURRENT)
show_map("=== CORRECTED (schema, arguments-only + required) ===", CORRECTED)
