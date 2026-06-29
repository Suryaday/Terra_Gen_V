# Terra_Gen_V — Architecture

A one-page view of how a natural-language request becomes valid, deployable Terraform.

**Legend:** 🟩 runs **locally / free** (Ollama + local cross-encoder) · 🟧 **OpenAI API (paid)** · 🟦 **data stores / ground truth**. Only two components are paid — embeddings and final generation — which is why the project runs lean.

```mermaid
flowchart TB
    subgraph CLIENT[" "]
        UI["React + Vite SPA<br/>(frontend/)"]
    end

    UI -->|"POST /generate {query}"| API["FastAPI · app.py<br/>generator.generate(query)"]

    subgraph ONLINE["ONLINE PIPELINE — per request (generator.py)"]
        direction TB

        subgraph PLAN["1 · PLAN — build_plan()"]
            P1["query_corrector<br/>fuzzy correct + expand"]
            P2["architecture_expander<br/>LLM resource proposal"]
            P3["validate + de-conflict<br/>ECS vs EC2, aliases"]
            P4["dependency_expander<br/>graph closure"]
            P5["_topo_sort<br/>Kahn's algorithm"]
            P1 --> P2 --> P3 --> P4 --> P5
        end

        subgraph RETR["2 · RETRIEVE — hybrid_retrieve()"]
            R0["query_router · hyde<br/>intent + HyDE expand"]
            R1["dense (ChromaDB)"]
            R2["sparse (BM25)"]
            R3["RRF fusion<br/>1/(60+rank)"]
            R4["cross-encoder rerank"]
            R5["budget alloc<br/>breadth→depth · ARGREF_FLOOR"]
            R6["dependency_retriever<br/>inject dep docs"]
            R0 --> R1 & R2
            R1 --> R3
            R2 --> R3
            R3 --> R4 --> R5 --> R6
        end

        subgraph GEN["3 · GENERATE — per resource, in order"]
            G1["context_builder<br/>U-shape XML context"]
            G2["LLM emits ONE block<br/>+ symbol table of prior resources"]
            G1 --> G2
        end

        subgraph REP["4 · REPAIR — schema layer"]
            X1["~18 _normalize_/_fix_ passes"]
            X2["schema_normalizer<br/>block vs argument"]
            X3["schema_validator<br/>findings"]
            X4["reference_corrector<br/>fix bad refs"]
            X1 --> X2 --> X3 --> X4
        end

        subgraph STITCH["5 · STITCH — stitch() + validate()"]
            S1["assemble main.tf"]
            S2["infer + declare variables.tf"]
            S3["final validation → warnings"]
            S1 --> S2 --> S3
        end

        PLAN --> RETR --> GEN --> REP --> STITCH
    end

    API --> ONLINE
    STITCH -->|"{architecture[], terraform, warnings, time}"| UI

    subgraph STORES["DATA / GROUND TRUTH"]
        DB1[("ChromaDB<br/>terraform_docs")]
        DB2[("bm25.pkl")]
        DB3[("resource_schema.json")]
        DB4[("auto_dependency_map.py<br/>788 resources")]
    end

    subgraph MODELS["MODELS"]
        M1["Ollama qwen3<br/>LOCAL · free"]
        M2["bge-reranker-v2-m3<br/>LOCAL · free"]
        M3["OpenAI embeddings<br/>text-embedding-3-small"]
        M4["OpenAI gpt-4.1-mini<br/>generation"]
    end

    subgraph OFFLINE["OFFLINE DATA PREP (build-time)"]
        direction LR
        O1["extract.py<br/>parse AWS docs"]
        O2["chunker.py<br/>split + tag"]
        O3["embed.py<br/>embed batches"]
        O4["bm25_retriever.py<br/>build index"]
        O5["generate_dependency_map.py<br/>terraform schema -json"]
        O1 --> O2 --> O3
        O2 --> O4
    end

    O3 --> DB1
    O4 --> DB2
    O5 --> DB3
    O5 --> DB4

    P2 -.-> M1
    R0 -.-> M1
    R1 -.-> M3
    R1 -.-> DB1
    R2 -.-> DB2
    R4 -.-> M2
    G2 -.-> M4
    P4 -.-> DB4
    REP -.-> DB3

    classDef local fill:#d4f5d4,stroke:#2d8a2d,color:#000;
    classDef api fill:#ffe0cc,stroke:#cc5500,color:#000;
    classDef store fill:#e0e8ff,stroke:#3355cc,color:#000;
    class M1,M2 local;
    class M3,M4 api;
    class DB1,DB2,DB3,DB4 store;
```

## Reading the diagram

The system has two pipelines:

- **Online (per request):** the five numbered stages — Plan, Retrieve, Generate, Repair, Stitch — run for every `POST /generate` call.
- **Offline (build-time):** the data-prep pipeline builds the ChromaDB vector store, the BM25 index, the provider schema ground truth, and the dependency map that the online pipeline reads from.

### The five stages

1. **Plan** — correct the query, propose resources with a local LLM, drop unknowns and resolve conflicts, close the dependency graph, then topologically sort with Kahn's algorithm so dependencies come before dependents.
2. **Retrieve** — optional HyDE expansion, parallel dense + sparse search, Reciprocal Rank Fusion, cross-encoder reranking, breadth-then-depth budget allocation, and dependency-doc injection.
3. **Generate** — for each resource in dependency order, build a U-shaped XML context and emit a single HCL block, passing a symbol table of already-generated resources so references resolve.
4. **Repair** — run targeted normalization passes plus schema-grounded normalization, validation, and reference correction against the real provider schema.
5. **Stitch** — assemble `main.tf`, infer and declare any missing variables in `variables.tf`, and run a final validation pass that emits warnings.

For a full narrative walkthrough of each component, see the [TUTORIAL](TUTORIAL.md). For setup and usage, see the [README](README.md).
