"""
regenerate_map.py  (V3)

- Builds V3 map from schema/resource_schema.json
- Cycles on FULL (hard+optional) AND HARD-ONLY graphs (hard-only is what
  expand_entities(hard_only=True) traverses -> the one that matters for safety)
- Field provenance for every cycle edge: "A -> B via field X"
- Per focus resource: resolved edges (with field) + unresolved ref-args
- Diffs vs V1, writes candidate.
"""
from __future__ import annotations

import json, sys
from collections import defaultdict
from pathlib import Path

from build_resource_dependencies import build_with_provenance

try:
    from auto_dependency_map import RESOURCE_DEPENDENCIES as V1
except Exception as exc:
    print("WARN: could not import V1:", exc); V1 = {}

SCHEMA = Path("schema/resource_schema.json")
if not SCHEMA.exists():
    print(f"ERROR: {SCHEMA} not found. Run generate_dependency_map.py first."); sys.exit(1)

sys.setrecursionlimit(100000)
V2, PROV = build_with_provenance(json.loads(SCHEMA.read_text(encoding="utf-8")))
print(f"V1 resources: {len(V1)}   V2 resources: {len(V2)}")

def graph(dmap, kinds):
    g = defaultdict(set)
    for e in dmap:
        _ = g[e]
    for e, d in dmap.items():
        deps = (d.get("hard", []) if "hard" in kinds else []) + \
               (d.get("optional", []) if "optional" in kinds else [])
        for dep in deps:
            if dep in dmap and dep != e:
                g[e].add(dep)
    return g

def tarjan(g):
    idx, low, on, st, cnt, out = {}, {}, {}, [], [0], []
    def sc(v):
        idx[v] = low[v] = cnt[0]; cnt[0] += 1; st.append(v); on[v] = True
        for w in g[v]:
            if w not in idx:
                sc(w); low[v] = min(low[v], low[w])
            elif on.get(w):
                low[v] = min(low[v], idx[w])
        if low[v] == idx[v]:
            comp = []
            while True:
                w = st.pop(); on[w] = False; comp.append(w)
                if w == v: break
            if len(comp) > 1:
                out.append(sorted(comp))
    for v in list(g):
        if v not in idx:
            sc(v)
    return out

def edges(dmap):
    s = set()
    for e, d in dmap.items():
        for dep in d.get("hard", []) + d.get("optional", []):
            s.add((e, dep))
    return s

g_full, g_hard = graph(V2, {"hard", "optional"}), graph(V2, {"hard"})
scc_full, scc_hard = tarjan(g_full), tarjan(g_hard)
e1, e2 = edges(V1), edges(V2)
dropped, added = e1 - e2, e2 - e1
inverted = {(a, b) for (a, b) in dropped if (b, a) in e2}

print("" + "=" * 70)
print(f"V1 edges {len(e1)} | V2 edges {len(e2)}")
print(f"FULL cycles (hard+optional): {len(scc_full)}")
print(f"HARD-ONLY cycles (closure):  {len(scc_hard)}   <-- the one that matters")
print(f"DROPPED {len(dropped)} | ADDED {len(added)} | INVERTED {len(inverted)}")
print("=" * 70)

def fields_for(a, b):
    return [f for (t, _k, f) in PROV.get(a, []) if t == b]

def show(title, sccs):
    print(f"{title}: {len(sccs)}")
    for scc in sccs:
        print(f"  SCC {scc}")
        s = set(scc)
        for a in scc:
            for b in g_full[a] & s:
                print(f"    {a} -> {b}  via {fields_for(a, b) or ['?']}")

show("FULL-GRAPH CYCLES", scc_full)
if scc_hard:
    show("HARD-ONLY CYCLES", scc_hard)
else:
    print("HARD-ONLY CYCLES: NONE  (closure is acyclic)")

FOCUS = ["aws_vpc", "aws_subnet", "aws_route_table", "aws_db_instance",
         "aws_lb", "aws_lb_listener", "aws_ecs_service", "aws_eks_cluster"]
print("" + "=" * 70)
print("FOCUS: resolved edges (with field) + unresolved ref-args")
print("=" * 70)
for r in FOCUS:
    d = V2.get(r, {})
    print(f"{r}  hard={d.get('hard', [])} optional={d.get('optional', [])}")
    for t, k, f in PROV.get(r, []):
        print(f"    {f} -> {t} [{k}]" if k != "unresolved" else f"    UNRESOLVED ref-arg: {f}")

out = Path("auto_dependency_map.candidate.py")
with open(out, "w") as f:
    f.write("# AUTO-GENERATED (V3 precision) - DO NOT EDIT MANUALLY RESOURCE_DEPENDENCIES = ")
    json.dump(V2, f, indent=4, sort_keys=True)
    f.write("")

print(f"Candidate written: {out} Done.")
