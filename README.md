# Terra_Gen_V

**An AI Terraform compiler.** Describe your AWS infrastructure in plain English and get back production-ready, dependency-resolved Terraform that passes `terraform validate` — not a snippet, not a template, a deployable module.

Terra_Gen_V is **not** a thin RAG wrapper around an LLM. It plans a resource dependency graph, retrieves the exact AWS provider documentation for each resource using a hybrid search pipeline, generates one HCL block at a time so cross-resource references resolve correctly, and repairs the output against the real Terraform provider schema before you ever see it.

---

## Why this exists

Turning an architecture design into working infrastructure is still one of the most tedious, error-prone steps in cloud engineering. An architect sketches the system; an engineer then spends days hand-translating it into Terraform — wiring up dependencies, getting the resource order right, and chasing `terraform validate` errors one by one.

The naive "ask an LLM for Terraform" approach falls apart in practice: it dumps every resource into one prompt, invents references that don't exist, forgets half the dependency chain, and rarely passes validation. The gap between *"looks like Terraform"* and *"is valid Terraform"* is where most of the real engineering lives — and that gap is what this project closes.

---

## Highlights

- **Local-first, cost-conscious.** Most of the pipeline runs on local models via [Ollama](https://ollama.com/) (architecture planning, HyDE query expansion) and a local cross-encoder reranker. The OpenAI API is used only where it earns its keep: embeddings and final HCL generation. Total development spend so far: under $20.
- **Graph-planned generation.** A dependency-aware DAG planner maps 788 AWS resource relationships and topologically sorts them, so dependencies are generated before the resources that reference them.
- **Schema-grounded repair.** Generated HCL is normalized and validated against the real Terraform AWS provider schema (`terraform providers schema -json`).
- **Hybrid retrieval.** Dense (embeddings) + sparse (BM25) retrieval fused with Reciprocal Rank Fusion, then reranked with a cross-encoder.

---

## Architecture

```
Natural-language request
        |
        v
   [ app.py ]  FastAPI  POST /generate
        |
        v
[ generator.generate() ]  -- orchestrator
        |
        +-- 1. PLAN      build_plan()        Which resources? (LLM + dependency graph + topo sort)
        +-- 2. RETRIEVE  hybrid_retrieve()   Pull exact AWS docs per resource
        +-- 3. GENERATE  generate_resource() One HCL block at a time (OpenAI)
        +-- 4. REPAIR    schema layer        Normalize + validate against provider schema
        +-- 5. STITCH    stitch()            Assemble main.tf + variables.tf, final validation
        |
        v
GenerateResponse { architecture[], terraform, warnings, generation_time_seconds }
        |
        v
   [ frontend/ ]  React + Vite SPA renders the result
```

There are two pipelines:

- **Online (per request):** the request flow shown above.
- **Offline (data prep):** ingest AWS provider docs, chunk, embed, and build the BM25 index plus the dependency map. See [Data preparation](#data-preparation-offline).

---

## How it works

### 1. Plan — `build_plan()` in `generator.py`
1. `query_corrector.py` — fuzzy spell-correction against the known AWS vocabulary and phrase expansion (e.g. "lambda function" -> `aws_lambda_function`).
2. `architecture_expander.py` — a local Ollama model proposes the full resource set; results are cached via `architecture_cache.py`.
3. `architecture_validator.py` + `schema_index.py` — drop entities that are not real, known resources.
4. `dependency_expander.py` — closes the dependency graph using `auto_dependency_map.py`.
5. `_topo_sort()` — Kahn's algorithm orders resources so dependencies come first.

### 2. Retrieve — `hybrid_retriever.hybrid_retrieve()`
- Intent classification (`query_router.py`) and optional HyDE expansion (`hyde.py`, local Ollama).
- Dense retrieval (`retriever.py`, ChromaDB) and sparse retrieval (`bm25_search.py`) run in parallel threads.
- Results fused via Reciprocal Rank Fusion, then reranked by a cross-encoder (`reranker.py`).
- `context_builder.py` formats the winning chunks into a U-shaped XML context to mitigate "lost in the middle."

### 3. Generate — `generate_resource()` in `generator.py`
For each node in dependency order, the assembled context plus a strict system prompt is sent to OpenAI. A symbol table of already-generated resources is passed in so later blocks reference earlier ones (e.g. `aws_iam_role.main.arn`) instead of inventing values.

### 4. Repair — schema layer
- `schema_normalizer.py` — fixes `field = value` where the schema requires a nested `block { }`.
- `schema_validator.py` — flags block-as-argument, missing required blocks, and invalid attribute references.
- `schema_index.py` / `schema_typing.py` / `schema_reference_corrector.py` — ground-truth lookups and reference correction against `schema/resource_schema.json`.

### 5. Stitch — `stitch()` in `generator.py`
Blocks are assembled into `main.tf`; any `var.x` referenced but not declared is auto-added to `variables.tf` with an inferred type. A final pass emits warnings for missing hard dependencies or dangling references.

---

## Tech stack

| Layer | Technology |
|---|---|
| API | FastAPI + Uvicorn |
| Generation | OpenAI `gpt-4.1-mini` |
| Embeddings | OpenAI `text-embedding-3-small` |
| Vector store | ChromaDB (persistent) |
| Sparse retrieval | BM25 (`rank-bm25`) |
| Reranking | `BAAI/bge-reranker-v2-m3` (sentence-transformers, local) |
| Local LLM (planning + HyDE) | Ollama (`qwen3:latest`) |
| Chunking | LangChain text splitters + tiktoken |
| Frontend | React 19 + Vite + TypeScript + Tailwind + React Flow |
| Dependency/schema ground truth | `terraform providers schema -json` |

**Notable engineering details:** Kahn's algorithm for topological sorting, multithreaded parallel retrieval (`ThreadPoolExecutor`), `threading.Semaphore` rate-limit gating, exponential backoff on external calls (`tenacity`), generators for streaming/batching chunks, frozen dataclasses for immutable data contracts, and LRU + on-disk caching.

---

## Project structure

```
Terra_Gen_V/
  app.py                       FastAPI entry point (POST /generate)
  models.py                    Pydantic request/response models
  generator.py                 Core compiler: plan -> generate -> repair -> stitch
  retrieval_types.py           Shared RetrievalResult dataclass

  # Retrieval layer
  hybrid_retriever.py          Orchestrates dense + sparse + RRF + rerank
  retriever.py                 Dense retriever (OpenAI embeddings + ChromaDB)
  bm25_search.py               Sparse retriever (loads vectorstore/bm25.pkl)
  bm25_retriever.py            BM25 index builder
  reranker.py                  Cross-encoder reranker
  hyde.py                      HyDE query expansion (local Ollama)
  query_corrector.py           Fuzzy query correction
  query_router.py              Intent classification
  architecture_expander.py     LLM architecture planner (local Ollama)
  architecture_cache.py        On-disk cache for planner output
  architecture_validator.py    Known-entity filtering
  dependency_expander.py       Dependency-graph closure
  dependency_retriever.py      Dependency-aware chunk injection
  context_builder.py           Prompt context assembler

  # Schema layer
  schema_index.py              Read-only index over the provider schema
  schema_normalizer.py         Block-vs-argument normalization
  schema_validator.py          Structural validation findings
  schema_typing.py             Terraform type -> HCL type
  schema_reference_corrector.py  Invalid reference rewriting
  auto_dependency_map.py       Generated RESOURCE_DEPENDENCIES map

  # Data prep (offline)
  extract.py                   Parse AWS provider docs -> corpus
  chunker.py                   Chunk corpus -> data/chunks/terraform_chunks.json
  embed.py                     Embed chunks -> ChromaDB

  # Evaluation
  golden_evaluation.py         Retrieval metrics (Recall@k, MRR, Success@1, nDCG)
  generation_eval.py           End-to-end generation eval (runs real terraform validate)
  evaluation/                  Datasets + recorded results

  # Schema / dependency-map build tooling
  "Terrafrom Dependency Mapping/"
    generate_dependency_map.py  Builds auto_dependency_map.py + schema/resource_schema.json

  frontend/                    React + Vite SPA

  data/
    processed/terraform_aws_corpus.json
    chunks/terraform_chunks.json
  schema/resource_schema.json  Provider schema ground truth
  vectorstore/                 chroma/ + bm25.pkl   (generated; see Data preparation)
```

---

## Prerequisites

- **Python 3.10+**
- **Node.js 18+** (for the frontend)
- **[Ollama](https://ollama.com/)** running locally, with the planning/HyDE model pulled:
  ```bash
  ollama pull qwen3:latest
  ```
- **An OpenAI API key** (used for embeddings and generation).
- **Terraform CLI** on your PATH (required to run the generation evaluation, which calls `terraform fmt/init/validate`, and to deploy generated output).

---

## Setup and installation

### 1. Clone and install Python dependencies

```bash
git clone https://github.com/Suryaday/Terra_Gen_V.git
cd Terra_Gen_V

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
# The runtime also uses these (install if not already present):
pip install ollama tenacity python-dotenv rapidfuzz
```

### 2. Configure environment

Create a `.env` file in the repo root:

```bash
OPENAI_API_KEY=sk-...

# Optional overrides (defaults shown)
OPENAI_MODEL=gpt-4.1-mini
ARCH_MODEL=qwen3:latest
OLLAMA_HOST=http://localhost:11434
```

### 3. Build the knowledge base (vector store + BM25 index)

The `vectorstore/` directory (ChromaDB + `bm25.pkl`) is generated, not committed. If `data/chunks/terraform_chunks.json` is present you can skip straight to embedding; otherwise run the full pipeline. See [Data preparation](#data-preparation-offline) for details.

```bash
python embed.py             # chunks -> ChromaDB (vectorstore/chroma) + artifacts/
python bm25_retriever.py    # chunks -> vectorstore/bm25.pkl
```

### 4. Run the backend

```bash
uvicorn app:app --reload --port 8000
```

The API is now available at `http://localhost:8000`.

### 5. Run the frontend

```bash
cd frontend
npm install
npm run dev
```

The SPA runs on the Vite dev server (default `http://localhost:5173`) and calls the backend at `http://localhost:8000/generate`.

---

## Usage

### Via the API

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"query": "a highly available web app with autoscaling and a managed database"}'
```

Response shape:

```json
{
  "query": "...",
  "architecture": ["aws_vpc", "aws_subnet", "..."],
  "terraform": "resource \"aws_vpc\" \"main\" { ... }",
  "warnings": [],
  "generation_time_seconds": 12.34
}
```

### Via the frontend

Open the SPA, enter an architecture description, and view the planned resource list, the generated Terraform, a validation indicator, and generation time.

---

## Data preparation (offline)

The retrieval knowledge base is built from the Terraform AWS provider documentation:

1. **Extract** — `extract.py` parses the provider markdown docs into `data/processed/terraform_aws_corpus.json`.
2. **Chunk** — `chunker.py` splits the corpus (header + token splitting, ~700 tokens / 80 overlap) into `data/chunks/terraform_chunks.json`.
3. **Embed** — `embed.py` batches chunks through OpenAI embeddings into the ChromaDB collection `terraform_docs` at `vectorstore/chroma`.
4. **Index** — `bm25_retriever.py` builds the sparse index at `vectorstore/bm25.pkl`.

The dependency map and schema ground truth are produced separately by `Terrafrom Dependency Mapping/generate_dependency_map.py`, which runs `terraform providers schema -json` and writes both `auto_dependency_map.py` and `schema/resource_schema.json`.

---

## Evaluation and benchmarks

Two harnesses measure quality against datasets in `evaluation/`:

- **Retrieval** — `golden_evaluation.py` computes Recall@k, MRR, Success@1, and nDCG over labeled queries (`evaluation/golden_queries.json`, 43 queries; `golden_quick.json`, 20-query subset).
- **Generation** — `generation_eval.py` runs the full pipeline over `evaluation/generation_eval.json` (40 cases), writes the output to a temp directory, and runs real `terraform fmt / init / validate`.

**Recorded results (reproduce with the commands below):**

| Benchmark | Result | Dataset |
|---|---|---|
| Generation passing `terraform validate` | 40 / 40 | `generation_eval.json` (latest run: no failures) |
| Retrieval Recall@8 | 0.95 | `golden_quick.json` (20-query subset) |
| Retrieval MRR | 0.76 | `golden_quick.json` (20-query subset) |
| Retrieval Success@1 | 0.65 | `golden_quick.json` (20-query subset) |

```bash
python golden_evaluation.py     # retrieval metrics
python generation_eval.py       # end-to-end generation + terraform validate
```

> Numbers above reflect the results recorded in the repo. The retrieval figures are from the 20-query quick subset; expanding to the full 43-query set is in progress.

---

## Known limitations

- **Generation is not perfect (~weak spots remain).** Complex resource chains, IAM policies, lifecycle rules, multi-subnet topologies, and deprecated argument names can still produce issues.
- **Image input is not implemented yet.** Today the system accepts a natural-language architecture specification; diagram-to-code (uploading an architecture image) is on the roadmap.
- **There is duplicated/scratch code.** The `evaluation/scripts/` directory contains a frozen snapshot copy of the backend, and the root has assorted debug/test scripts. A refactor to leaner shared modules is planned.
- **The knowledge base must be built locally.** `vectorstore/` is generated and not committed.

---

## Roadmap

- Diagram-to-code: accept an architecture image as input.
- Expand the retrieval benchmark to the full 43-query set and publish results.
- Harden generation on IAM, lifecycle, and multi-subnet chains.
- Refactor for ~30% less code via shared abstractions and removal of scratch/duplicate files.
- Broader provider coverage beyond AWS.

---

## License

Released under the [MIT License](LICENSE).
