# Retrieval Baseline (Locked State)

## Retrieval Configuration

```python
MAX_DISTANCE = 1.2

RERANK_POOL = 24

SIMILARITY_FUNCTION = "1 - distance / 2"

ENTITY_DIVERSITY_LIMIT_ARGUMENT_REFERENCE = 2

DENSE_QUERY = "original_query"

BM25_QUERY = "clean_query"
```

---

## Enabled Features

* Metadata-aware reranking
* HyDE query generation
* Hybrid retrieval (Dense + BM25 + RRF)
* Protected phrase correction
* Reranker semantic alias enrichment
* Entity diversity for argument reference chunks
* Architecture dependency injection

---

## Current Retrieval Philosophy

Dense:

* semantic understanding
* natural language intent

Sparse:

* lexical/entity recovery
* Terraform terminology rescue

Reranker:

* semantic grounding
* metadata-aware ranking

---

## Evaluation Rules

* No retrieval tuning without benchmark evidence
* All changes validated using:

  * golden_quick.json
  * golden_full.json
* Failures categorized manually
* No optimization for single-query overfitting
