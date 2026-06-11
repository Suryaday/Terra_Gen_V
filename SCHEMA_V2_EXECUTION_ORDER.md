# Execution Order Documentation

## Part A — Live Pipeline (current `generation_eval.py` flow)

```
generation_eval.py
│
├─ generator.generate(query)
│   │
│   ├─ PHASE 1: PLAN  [generator.build_plan]
│   │   ├─ query_corrector.py          → phrase expansion + fuzzy correction
│   │   ├─ architecture_expander.py    → extract_architecture()
│   │   │   ├─ architecture_cache.py   → get_cached(v6:...) / save_cached()
│   │   │   └─ [on miss] call_llm()   → Ollama/qwen3 → complete_architecture()
│   │   ├─ architecture_validator.py   → validate_entities()
│   │   ├─ generator.py               → PLANNER_NAME_ALIASES / RESOURCE_ALIASES
│   │   ├─ generator.py               → merge query entities → complete_architecture()
│   │   ├─ generator.py               → remove_conflicting_entities()
│   │   ├─ dependency_expander.py      → expand_entities(hard_only=True)
│   │   │   └─ auto_dependency_map.py  → RESOURCE_DEPENDENCIES (edges)
│   │   ├─ generator.py               → _topo_sort() / get_generation_deps()
│   │   │   └─ auto_dependency_map.py  → RESOURCE_DEPENDENCIES (edges)
│   │   └─ → ResourceNode list with hard_deps
│   │
│   ├─ PHASE 2: RETRIEVE  [generator.retrieve_generation_context]
│   │   ├─ hybrid_retriever.py         → hybrid_retrieve()
│   │   │   ├─ query_router.py        → intent classification
│   │   │   ├─ query_corrector.py     → correct query
│   │   │   ├─ retriever.py           → dense: HyDE (Ollama) + OpenAI embeddings
│   │   │   ├─ bm25_search.py         → sparse: BM25 → RRF merge
│   │   │   ├─ reranker.py            → cross-encoder re-rank
│   │   │   └─ dependency_retriever.py → inject_dependencies()
│   │   │       └─ auto_dependency_map.py → RESOURCE_DEPENDENCIES
│   │   └─ → global retrieval rows
│   │
│   ├─ PHASE 3: BACKFILL
│   │   └─ retrieve_entity_rows() for planned entities missing from retrieval
│   │
│   ├─ PHASE 4: GENERATE (loop per node, topo order)
│   │   ├─ assemble_context()
│   │   │   ├─ filter_rows_for_resource()  (uses node.hard_deps ← RESOURCE_DEPS)
│   │   │   ├─ ARGREF floor top-up (BM25)
│   │   │   ├─ context_builder.py → build_xml_context()
│   │   │   └─ build_dependency_reference_context()
│   │   ├─ generate_resource() → OpenAI chat (temperature=0)
│   │   └─ normalizer chain (all in generator.py)
│   │
│   └─ PHASE 5: STITCH & VALIDATE
│       ├─ stitch() → main.tf / variables.tf / outputs.tf / providers.tf
│       └─ validate() → reference + dependency warnings
│
└─ terraform init + terraform validate → PASS/FAIL
```

---

## Part B — Schema V2 Toolchain (prototype, NOT wired into live pipeline)

### Execution order to generate V2 and verify:

```
Step 1:  generate_dependency_map.py        [OFFLINE, requires terraform CLI]
         ├─ fetches: terraform providers schema -json
         ├─ builds: RESOURCE_DEPENDENCIES (V1 - current)  → auto_dependency_map.py
         └─ NEW: extract_resource_schema()                 → schema/resource_schema.json

Step 2:  regenerate_map.py                 [VERIFICATION, reads schema + V1]
         ├─ reads: schema/resource_schema.json
         ├─ calls: build_resource_dependencies.build_dependencies()
         │          (arguments-only, required→hard/optional→optional)
         ├─ compares: V1 vs V2
         │   ├─ cycle count (Tarjan SCC)
         │   ├─ edge count
         │   ├─ DROPPED edges (regression risk)
         │   ├─ ADDED edges
         │   ├─ INVERTED edges
         │   └─ per-resource focus comparison
         └─ writes: auto_dependency_map.candidate.py (V2)

Step 3:  dependency_diff_demo.py           [DEMO, uses sample data]
         ├─ reads: schema/dependency_sample.json (small VPC/RDS sample)
         ├─ calls: build_resource_dependencies.build_dependencies()
         ├─ imports: auto_dependency_map.RESOURCE_DEPENDENCIES (V1)
         └─ prints: side-by-side + cycle check for focus nodes
```

### File purposes:

| File | Role | When to run |
|------|------|-------------|
| `generate_dependency_map.py` | Offline: fetches real Terraform schema, produces `auto_dependency_map.py` + `schema/resource_schema.json` | Once (on a machine with `terraform` + AWS provider) |
| `build_resource_dependencies.py` | Library: `build_dependencies(schema_dict)` → V2 map from arguments-only logic | Called by `regenerate_map.py` |
| `regenerate_map.py` | Verification: V1-vs-V2 diff + cycles + edge analysis + writes candidate | After Step 1 |
| `dependency_diff_demo.py` | Quick demo: cycle/topo comparison on small sample (no terraform needed) | Anytime |
| `schema_index.py` | Runtime API: read-only queries over `resource_schema.json` (safe no-op if absent) | Future: wired into normalizers |
| `schema_normalizers.py` | PoC normalizers: block-as-arg, required blocks, invalid attrs, var types | Future: wired behind existing chain |
| `schema_layer_demo.py` | Standalone demo of the 4 normalizer capabilities | Anytime |

### Data files:

| File | Purpose |
|------|---------|
| `schema/resource_schema.json` | FULL provider schema (all ~1500 resources) — produced by Step 1 |
| `schema/resource_schema.sample.json` | 8-resource subset for `schema_layer_demo.py` (no terraform needed) |
| `schema/dependency_sample.json` | VPC/RDS subset for `dependency_diff_demo.py` (no terraform needed) |

---

## Part C — Integration path (AFTER verification proves V2 is clean)

```
1. Confirm V2 has 0 cycles and no critical dropped edges
2. Replace auto_dependency_map.py with auto_dependency_map.candidate.py
3. Re-run 20/20 benchmark
4. If green: demote ARCHITECTURE_COMPLETIONS to intent-only
5. Wire schema_normalizers behind existing chain (additive)
6. Progressively retire hand-maintained normalizer tables
```
