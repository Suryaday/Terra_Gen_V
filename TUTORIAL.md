# Terra_Gen_V — A Deep-Dive Tutorial

> How to turn plain English into valid, deployable Terraform — and how to run the whole thing on your own machine.

This tutorial is longer and more hands-on than the [README](README.md). It has two halves:

- **Part A — The concepts.** What problem this solves, why naive RAG fails at it, and how every piece of the pipeline works. Read this if you want to *understand* the topic.
- **Part B — Run it yourself.** A step-by-step setup guide, including the gotchas, with troubleshooting.

You do not need to be an ML expert. If you know a little Python and have touched Terraform once, you'll be fine.

---

## Table of contents

**Part A — Concepts**
1. [The problem: from a sketch to a `.tf` file](#1-the-problem)
2. [Why "just ask ChatGPT for Terraform" breaks](#2-why-naive-rag-breaks)
3. [The core idea: treat it like a compiler, not a chatbot](#3-the-compiler-idea)
4. [Retrieval 101: dense vs sparse search](#4-retrieval-101)
5. [Fusing two searches with Reciprocal Rank Fusion (RRF)](#5-rrf)
6. [HyDE: searching with a hypothetical answer](#6-hyde)
7. [Cross-encoder reranking](#7-reranking)
8. [Budget allocation and the "U-shape" context trick](#8-context)
9. [The dependency graph and topological sort](#9-dependency-graph)
10. [Schema-grounded repair: the part that makes it valid](#10-schema-repair)
11. [Putting it all together: one request, end to end](#11-end-to-end)

**Part B — Run it yourself**
12. [What you need before you start](#12-prerequisites)
13. [Step 1 — Clone and create a virtual environment](#13-step-1)
14. [Step 2 — Install dependencies](#14-step-2)
15. [Step 3 — Configure your `.env`](#15-step-3)
16. [Step 4 — Install and start Ollama](#16-step-4)
17. [Step 5 — Build the knowledge base (vector store + BM25)](#17-step-5)
18. [Step 6 — Run the backend API](#18-step-6)
19. [Step 7 — Run the frontend](#19-step-7)
20. [Step 8 — Run the evaluations](#20-step-8)
21. [Troubleshooting](#21-troubleshooting)
22. [How to extend it](#22-extend)
23. [FAQ](#23-faq)

---

# Part A — Concepts

## 1. The problem

Cloud infrastructure usually starts as a picture or a sentence: *"a highly available web app with autoscaling behind a load balancer and a managed database."* Turning that into real, working [Terraform](https://developer.hashicorp.com/terraform) is slow and fiddly. You have to:

- Pick the right AWS resources (`aws_vpc`, `aws_subnet`, `aws_lb`, `aws_autoscaling_group`, `aws_db_instance`, ...).
- Create them in the right order, because some resources reference others (a subnet needs a VPC id first).
- Get every argument and nested block exactly right, or `terraform validate` rejects it.

Terra_Gen_V automates that translation. You give it a description; it gives you back a deployable module that passes validation.

> **Today it takes a natural-language description.** Accepting an architecture *diagram/image* as input is on the roadmap, not yet implemented.

---

## 2. Why naive RAG breaks

**RAG** (Retrieval-Augmented Generation) means: before asking the LLM to answer, you *retrieve* relevant documents and stuff them into the prompt so the model has facts to work from. The textbook version is about 50 lines:

```python
# The "RAG in an afternoon" version
loader = DirectoryLoader("docs/", glob="**/*.md")
splitter = RecursiveCharacterTextSplitter(chunk_size=700)
store = Chroma.from_documents(splitter.split_documents(loader.load()), OpenAIEmbeddings())
chain = RetrievalQA.from_chain_type(llm=ChatOpenAI(model="gpt-4"), retriever=store.as_retriever())
print(chain.invoke("Build me an EKS cluster with Fargate"))
```

This produces *something*. But for infrastructure code it fails in predictable ways:

| Failure | Why it happens |
|---|---|
| Resources in random order | The LLM emits everything in one pass with no notion of dependencies. |
| Invented references | It writes `subnet_id = aws_subnet.main.id` for a subnet it never created. |
| Half the dependencies missing | Asked for a load balancer, it forgets the target group, listener, or security group. |
| Wrong syntax | It writes `lifecycle = {...}` as an argument when Terraform requires a `lifecycle { }` *block*. |
| Fails `terraform validate` | All of the above compound. |

The gap between *"looks like Terraform"* and *"is valid Terraform"* is where the real work lives. Closing it requires structure the naive chain doesn't have.

---

## 3. The compiler idea

The mental model that makes this tractable: **treat generation like a compiler, not a chatbot.**

A compiler doesn't translate your whole program in one blob. It parses structure, resolves symbols, orders things by dependency, and validates against a grammar. Terra_Gen_V does the same for infrastructure:

```
PLAN      -> figure out which resources, and their dependency order
RETRIEVE  -> pull the exact docs for each resource
GENERATE  -> emit one resource block at a time, in order
REPAIR    -> validate/fix each block against the real provider schema
STITCH    -> assemble files, declare variables, final validation
```

Each stage is deterministic where it can be, and uses an LLM only where judgment is genuinely needed. The rest of Part A walks through the interesting pieces.

---

## 4. Retrieval 101

To give the generator the right documentation, the system searches a corpus of the entire Terraform AWS provider docs. It uses **two complementary kinds of search**.

**Dense (semantic) search** — `retriever.py`
Every chunk of documentation is converted into a vector (a list of numbers) using an embedding model (`text-embedding-3-small`). Your query is embedded too, and the system finds chunks whose vectors are closest. This captures *meaning*: "serverless function" can match "lambda" even without the exact word. Vectors live in [ChromaDB](https://www.trychroma.com/).

**Sparse (keyword) search** — `bm25_search.py` / `bm25_retriever.py`
This is classic keyword matching using the [BM25](https://en.wikipedia.org/wiki/Okapi_BM25) algorithm. It's exact and literal — great for things dense search fumbles, like the precise token `aws_security_group_rule` or `t3.micro`. The tokenizer is infrastructure-aware: it deliberately keeps `aws_security_group_rule`, `us-east-1`, and `10.0.0.0/16` as single tokens instead of splitting them.

Why both? Dense search understands intent but can be fuzzy; sparse search is precise but literal. Each covers the other's blind spots. Combining them is the next step.

---

## 5. RRF

Now you have two ranked lists — one from dense, one from sparse — and you need a single merged ranking. The system uses **Reciprocal Rank Fusion**, which is elegantly simple. Each document gets a score based on its *rank* (not its raw similarity, which isn't comparable across the two systems):

```
RRF(doc) = sum over each list of   1 / (k + rank_in_that_list)
```

In the code (`hybrid_retriever.py`), `k = 60`:

```python
RRF_K = 60
def rrf_score(rank: int):
    return 1 / (RRF_K + rank)
```

A document ranked #1 in a list contributes `1/61`; ranked #2 contributes `1/62`; and so on. A document that appears high in *both* lists accumulates the most score and rises to the top. The constant `k=60` is a well-known default that softens the influence of tiny rank differences. The two searches run **in parallel threads** so fusion adds little latency.

---

## 6. HyDE

**HyDE** stands for *Hypothetical Document Embeddings* (`hyde.py`). The trick: a short user query and a long documentation chunk don't look very similar as vectors, which hurts dense search. So instead of embedding the bare query, you first ask a cheap **local** LLM (via [Ollama](https://ollama.com/), model `qwen3`) to *write a fake answer* — a plausible paragraph of Terraform documentation for the query — and embed *that*. The hypothetical answer "looks like" the real docs you're trying to find, so recall improves.

HyDE isn't always worth it. The pipeline **skips** HyDE when the query is very short (3 tokens or fewer) or contains precise lookup terms like `timeout`, `ingress`, `ttl` — cases where literal keyword search is already better. Running HyDE locally keeps it free.

---

## 7. Reranking

RRF gives a good candidate pool, but it's still based on ranks, not deep relevance. A **cross-encoder reranker** (`reranker.py`, model `BAAI/bge-reranker-v2-m3`) then re-scores the pool. Unlike the bi-encoder used for dense search (which embeds query and doc separately), a cross-encoder reads the query and each candidate *together* and outputs a precise relevance score. It's slower, so it's only run on the shortlist — not the whole corpus. The model is loaded once and cached.

---

## 8. Context

After reranking you still can't just dump everything into the prompt. Two refinements:

**Two-phase budget allocation** (`hybrid_retriever.py`).
A request like "ECS service with a VPC, subnets, security groups, and a load balancer" plans ~10 resources. If you naively take the top-k chunks, a few "loud" resources (like `aws_ecs_service`) can eat the entire budget, leaving `aws_subnet`, `aws_security_group`, etc. with *zero* documentation. So selection happens in two passes:
- **Phase 1 (breadth):** give every distinct resource up to 2 chunks first, so all planned resources are represented.
- **Phase 2 (depth):** spend the remaining budget deepening coverage (argument-reference sections get a higher cap).

**U-shape ordering** (`context_builder.py`).
LLMs suffer from "lost in the middle" — they pay most attention to the *start* and *end* of a long prompt and least to the middle. So the most important docs are placed at the two ends and the least important in the middle:

```python
# rank 1 -> bottom, rank 2 -> top, rank 3 -> second from bottom, ...
```

The final context is emitted as structured XML with three sections — `<supporting_architecture>`, `<primary_documentation>`, and `<terraform_examples>` — and the noisy per-chunk metadata headers are stripped out.

---

## 9. Dependency graph

This is what fixes the "wrong order / missing dependencies" failures.

The file `auto_dependency_map.py` contains a generated map of **788 AWS resource relationships**, shaped like:

```python
RESOURCE_DEPENDENCIES = {
    "aws_subnet": {"hard": ["aws_vpc"], "optional": []},
    "aws_instance": {"hard": [], "optional": ["aws_subnet", "aws_security_group"]},
    ...
}
```

- **hard** = a true requirement (a subnet cannot exist without a VPC).
- **optional** = commonly associated but not strictly required.

Two things use this map:
- `dependency_expander.py` — *graph closure*: if you ask for a subnet, it pulls in the VPC automatically.
- `_topo_sort()` in `generator.py` — orders resources so dependencies are generated first.

The ordering uses **Kahn's algorithm**, a standard topological-sort technique: repeatedly take the resources with no remaining unmet dependencies, emit them, remove them from the graph, and repeat. The result is an order where, by the time you generate `aws_subnet`, the `aws_vpc` it references already exists — so the generator can wire up `vpc_id = aws_vpc.main.id` correctly using a **symbol table** of already-generated resources.

> The map itself is built offline by `Terrafrom Dependency Mapping/generate_dependency_map.py`, which runs `terraform providers schema -json` and resolves which resource each attribute reference points to, with manual overrides for edges the schema can't express and to break cycles.

---

## 10. Schema repair

Even with perfect context, an LLM still makes structural mistakes — the classic one being writing a *nested block* as an *argument*:

```hcl
# WRONG (what the LLM sometimes emits)
resource "aws_instance" "main" {
  lifecycle = { create_before_destroy = true }
}

# RIGHT (what the schema requires)
resource "aws_instance" "main" {
  lifecycle {
    create_before_destroy = true
  }
}
```

The schema layer catches and fixes these *before you ever see the output*, using the real provider schema stored in `schema/resource_schema.json`:

- `schema_index.py` — a read-only index: is this a known resource? is this path a block or an argument? what type is this field?
- `schema_normalizer.py` — rewrites `field = value` into a `field { }` block when the schema says it should be nested (and vice versa).
- `schema_validator.py` — reports structural findings: block-used-as-argument, missing required block, invalid attribute reference.
- `schema_reference_corrector.py` — rewrites bad attribute references (e.g. an invalid `.foo` to a valid `.id`).

On top of this, `generator.py` runs ~18 targeted normalization passes, each one written to fix a *specific* failure pattern observed across many test generations. That accumulated, empirical repair logic is the bulk of why the output actually validates.

---

## 11. End to end

Here's a single request flowing through the whole system:

```
Query: "a highly available web app with autoscaling and a managed database"
  |
  v
PLAN (generator.build_plan)
  - correct/normalize the query                       (query_corrector)
  - LLM proposes resources, cached                    (architecture_expander + Ollama)
  - drop unknown resources                            (architecture_validator + schema_index)
  - close the dependency graph                        (dependency_expander + auto_dependency_map)
  - topologically sort (Kahn's algorithm)             (_topo_sort)
  => ordered list: aws_vpc, aws_subnet, aws_security_group, aws_lb, aws_autoscaling_group, aws_db_instance, ...
  |
  v
RETRIEVE (hybrid_retriever.hybrid_retrieve)
  - classify intent, maybe HyDE-expand                (query_router, hyde)
  - dense + sparse search in parallel                 (retriever, bm25_search)
  - fuse with RRF                                      (rrf_score)
  - cross-encoder rerank                               (reranker)
  - breadth-then-depth budget across resources
  - inject dependency docs                             (dependency_retriever)
  |
  v
GENERATE (per resource, in order)
  - build U-shaped XML context                         (context_builder)
  - LLM emits ONE resource block, given a symbol table of earlier resources (OpenAI gpt-4.1-mini)
  - run ~18 normalize passes + schema normalize/validate (schema_*)
  |
  v
STITCH (generator.stitch)
  - assemble main.tf
  - auto-declare any referenced-but-missing var.x into variables.tf
  - final validation pass -> warnings
  |
  v
Response: { architecture[], terraform, warnings, generation_time_seconds }
```

The web UI (`frontend/`) calls `POST /generate` and renders the resource list, the Terraform, a validation indicator, and the timing.

---

# Part B — Run it yourself

> **Time budget:** ~20–30 minutes, most of it spent installing dependencies and pulling the Ollama model. You will need your own OpenAI API key (embeddings + generation cost a few cents per run).

## 12. Prerequisites

| Tool | Version | Why |
|---|---|---|
| Python | 3.10+ | Backend + pipeline |
| Node.js | 18+ | Frontend |
| [Ollama](https://ollama.com/) | latest | Local LLM for planning + HyDE |
| OpenAI API key | — | Embeddings + final generation |
| Terraform CLI | 1.x | Only needed to run the generation eval / deploy output |
| Git | — | Cloning |

Check what you have:

```bash
python --version
node --version
ollama --version
terraform version
```

---

## 13. Step 1 — Clone and create a virtual environment

```bash
git clone https://github.com/Suryaday/Terra_Gen_V.git
cd Terra_Gen_V

python -m venv .venv
# macOS / Linux:
source .venv/bin/activate
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
```

A virtual environment keeps this project's packages isolated from the rest of your system.

---

## 14. Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

`requirements.txt` includes the runtime packages (`fastapi`, `uvicorn`, `openai`, `chromadb`, `rank-bm25`, `sentence-transformers`, `ollama`, `tenacity`, `python-dotenv`, `rapidfuzz`, ...).

> **Note:** `sentence-transformers` will download the reranker model (`BAAI/bge-reranker-v2-m3`, a few hundred MB) the first time the retriever runs. This is normal and only happens once.

---

## 15. Step 3 — Configure your `.env`

Create a file named `.env` in the repo root:

```bash
OPENAI_API_KEY=sk-your-key-here

# Optional — defaults shown
OPENAI_MODEL=gpt-4.1-mini
ARCH_MODEL=qwen3:latest
OLLAMA_HOST=http://localhost:11434
OLLAMA_TIMEOUT=120
```

The OpenAI key is **required** — the code raises an error on startup if it's missing.

---

## 16. Step 4 — Install and start Ollama

Ollama runs the local models used for architecture planning and HyDE, so you don't pay for those calls.

```bash
# Install from https://ollama.com/download, then:
ollama pull qwen3:latest
ollama serve     # if it isn't already running as a service
```

Verify it responds:

```bash
curl http://localhost:11434/api/tags
```

---

## 17. Step 5 — Build the knowledge base

The retrieval index (`vectorstore/`) is **generated**, not committed. There are two paths depending on what's already in your clone.

### The pipeline

```
extract.py  ->  data/processed/terraform_aws_corpus.json   (parse provider docs)
chunker.py  ->  data/chunks/terraform_chunks.json          (split into chunks)
embed.py    ->  vectorstore/chroma/                         (dense vectors in ChromaDB)
bm25_retriever.py -> vectorstore/bm25.pkl                   (sparse BM25 index)
```

### Fast path (recommended)

The repo already ships `data/chunks/terraform_chunks.json`. If it's present, **skip extraction and chunking** and just build the two indexes:

```bash
python embed.py             # builds vectorstore/chroma + artifacts/embedding_manifest.json
python bm25_retriever.py    # builds vectorstore/bm25.pkl
```

`embed.py` calls the OpenAI embeddings API in parallel batches (with a semaphore to respect rate limits and exponential backoff on failures). It writes a manifest and a `failed_batches.json` if anything fails, so re-running only retries what's missing.

### Full path (only if you want to rebuild the corpus from scratch)

> **Gotcha you must know about:** `extract.py` currently has a **hardcoded local path** at the top:
>
> ```python
> PROJECT_ROOT = Path("C:/Users/Suryaday Nath/Downloads/Projects/RAG")
> ```
>
> It also expects the AWS provider docs at `terraform-provider-aws/website/docs/{r,d}`. To run the full extraction you must (a) clone the [`terraform-provider-aws`](https://github.com/hashicorp/terraform-provider-aws) repo, and (b) edit `PROJECT_ROOT` to point at your own location. Then:
>
> ```bash
> python extract.py     # -> data/processed/terraform_aws_corpus.json
> python chunker.py     # -> data/chunks/terraform_chunks.json
> python embed.py
> python bm25_retriever.py
> ```

For most people, the **fast path** is all you need.

### Sanity-check retrieval

You can poke the retriever interactively before touching the API:

```bash
python hybrid_retriever.py
# then type, e.g.:  how to trigger lambda from s3 upload
```

---

## 18. Step 6 — Run the backend API

```bash
uvicorn app:app --reload --port 8000
```

Test it:

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"query": "a highly available web app with autoscaling and a managed database"}'
```

You'll get JSON like:

```json
{
  "query": "...",
  "architecture": ["aws_vpc", "aws_subnet", "aws_security_group", "..."],
  "terraform": "resource \"aws_vpc\" \"main\" { ... }",
  "warnings": [],
  "generation_time_seconds": 12.3
}
```

> The first request is slower: it lazily loads the BM25 index and the reranker model. Subsequent requests are faster.

---

## 19. Step 7 — Run the frontend

```bash
cd frontend
npm install
npm run dev
```

Open the printed Vite URL (typically `http://localhost:5173`). The SPA posts to `http://localhost:8000/generate`, so keep the backend running. Enter a description and you'll see the planned resources, the generated Terraform, a validation indicator, and the timing.

---

## 20. Step 8 — Run the evaluations

Two harnesses let you reproduce the quality numbers.

**Retrieval quality** (Recall@k, MRR, Success@1, nDCG):

```bash
python golden_evaluation.py
```

This scores the retriever against labeled queries in `evaluation/golden_queries.json` (43 queries; `golden_quick.json` is a 20-query subset).

**End-to-end generation** (runs *real* `terraform fmt / init / validate`):

```bash
python generation_eval.py
```

This generates Terraform for each case in `evaluation/generation_eval.json` (40 cases), writes files to a temp directory, and runs the Terraform CLI against them. Failures are written to `generation_failures.txt`. (Requires the Terraform CLI installed.)

**Numbers recorded in this repo:**

| Benchmark | Result | Dataset |
|---|---|---|
| Generation passing `terraform validate` | 40 / 40 | `generation_eval.json` (latest run: no failures) |
| Retrieval Recall@8 | 0.95 | `golden_quick.json` (20-query subset) |
| Retrieval MRR | 0.76 | `golden_quick.json` (20-query subset) |
| Retrieval Success@1 | 0.65 | `golden_quick.json` (20-query subset) |

The retrieval figures are from the 20-query quick subset; expanding to the full 43-query set is in progress. Your numbers may differ slightly depending on model versions.

---

## 21. Troubleshooting

| Symptom | Likely cause / fix |
|---|---|
| `RuntimeError: OPENAI_API_KEY missing` | No `.env`, or the key isn't named `OPENAI_API_KEY`. |
| `Missing Chroma path vectorstore/chroma` | You skipped `python embed.py`. Build the indexes (Step 5). |
| `Missing chunks file: .../terraform_chunks.json` | The chunks file isn't present; run the full path or restore it. |
| First request hangs ~30s | Normal cold start — the reranker model and BM25 index load lazily on first use. |
| Architecture expansion times out / empty plan | Ollama isn't running or `qwen3:latest` isn't pulled. Check `curl http://localhost:11434/api/tags`. |
| `extract.py` can't find files | The hardcoded `PROJECT_ROOT` path and the `terraform-provider-aws` docs aren't set up. Use the **fast path** instead. |
| Frontend shows network error | Backend isn't running on `:8000`, or CORS — make sure `uvicorn` is up first. |
| Embedding step reports failed batches | Transient OpenAI rate limits; just re-run `python embed.py` — it retries only the missing batches. |
| Reranker download is slow | One-time `sentence-transformers` model download; let it finish. |

---

## 22. Extend it

Some good entry points if you want to build on it:

- **Add resources to the dependency map.** Edit the override rules in `Terrafrom Dependency Mapping/dependency_overrides.py` and regenerate `auto_dependency_map.py`.
- **Tune retrieval.** The constants at the top of `hybrid_retriever.py` (`TOP_K`, `RRF_K`, `FIRST_PASS_PER_ENTITY`, `RERANK_POOL`, section priorities) control the whole retrieval shape. Change one, re-run `golden_evaluation.py`, and watch the metrics move.
- **Add a normalization pass.** If you observe a recurring generation mistake, add a targeted `_normalize_*`/`_fix_*` pass in `generator.py` and add a case to `evaluation/generation_eval.json`.
- **Swap models.** `OPENAI_MODEL` and `ARCH_MODEL` are environment variables; try different generation/planning models.

---

## 23. FAQ

**Is this just a LangChain wrapper?**
No. The retrieval pipeline (hybrid + RRF + reranking), the dependency-graph planner with topological sort, and the schema-grounded repair layer are the bulk of the work, and none of that comes "for free" from a basic RAG chain.

**Does it really cost only ~$20?**
Development to date has been under $20 because most of the pipeline runs locally on Ollama (planning, HyDE) and a local cross-encoder (reranking). OpenAI is used only for embeddings (one-time index build) and final generation. Your ongoing cost is a few cents of OpenAI usage per generation.

**Can it take an architecture diagram as input?**
Not yet — that's on the roadmap. Today the input is a natural-language description.

**Is the output production-ready?**
It's designed to pass `terraform validate` and to be a strong first draft. Like any generated IaC, review it before you run `terraform apply` against real infrastructure. Known weak spots: complex IAM policies, lifecycle rules, multi-subnet chains, and deprecated argument names.

**Why both dense and sparse search?**
Dense search understands meaning but is fuzzy; sparse (BM25) is literal and exact. Each covers the other's blind spots, and RRF fuses them.

---

*Found this useful, or hit a snag? Open an issue on the repo. Contributions and corrections welcome.*
