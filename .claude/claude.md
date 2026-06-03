# 🚀 Project: Autonomous Terraform AI Compiler

## The Grand Vision
We are building a God-Tier Infrastructure-as-Code (IaC) compiler. This system takes natural language architecture requests (e.g., "Build a highly available EKS cluster with a Fargate profile") and outputs perfect, production-ready, dependency-mapped Terraform HCL. 
This is not a simple RAG chatbot. This is a deterministic, graph-augmented AI compiler.

## System Architecture (Current State)
We have successfully built a mathematically flawless retrieval engine (Recall@8 = 1.000). The pipeline operates as follows:
1. **Lexical Normalization:** `query_corrector.py` (RapidFuzz).
2. **Intent Routing:** `query_router.py`.
3. **Graph-Augmented Expansion:** `architecture_expander.py` (Async LLM) + `dependency_retriever.py` (O(1) topological lookup using `auto_dependency_map.py`).
4. **Hybrid Search:** `hybrid_retriever.py` orchestrates Dense embeddings and Sparse BM25 concurrently.
5. **Cross-Encoder Reranking:** `reranker.py` (BAAI/bge-reranker-v2-m3) uses explicit intent-hijacking to perfectly sort chunks.
6. **Context Formatting:** `context_builder.py` formats chunks in a U-Shape XML structure to defeat LLM "Lost in the Middle" syndrome.

## 🛡️ The Prime Directive (What NOT to touch)
The retrieval layer is **FROZEN**. It is mathematically tuned and complete. 
Unless explicitly commanded by the user, **DO NOT** modify the logic, weighting, threading, or metadata schemas inside:
- `hybrid_retriever.py`
- `dependency_retriever.py`
- `bm25_search.py`
- `reranker.py`
- `chunker.py`

## 🎯 Current Objectives & Agent Mandate
You are authorized to architect, write, edit, and test code to achieve the following goals. Focus your efforts here:

1. **The Generation Engine (`generator.py`):** - We need to stream the U-Shaped XML context into a top-tier LLM to generate the actual HCL. 
   - Implement advanced prompt engineering, output parsing, and error-handling.
2. **Multi-File Output:** - Real Terraform isn't just one file. Help expand the generator to output modular Terraform (`main.tf`, `variables.tf`, `outputs.tf`, `providers.tf`).
3. **HCL Validation:** - Integrate the `terraform fmt` and `terraform validate` CLI commands into the generation loop. If the LLM generates invalid HCL, the system should catch it, feed the error back to the LLM, and auto-correct it before showing the user.
4. **State & Conversation Memory:** - Upgrade the CLI so users can iteratively modify their architecture (e.g., "Actually, change that RDS instance to Postgres").