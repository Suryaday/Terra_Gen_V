from __future__ import annotations

import logging
import concurrent.futures
import time
import threading
import re

from collections import defaultdict
from dataclasses import replace
from pathlib import Path
from typing import Optional
from collections import Counter

from query_corrector import QueryCorrector
from query_router import (classify, QueryIntent)

from hyde import generate_hyde

from bm25_search import BM25Engine

from retriever import retrieve as dense_retrieve

from retrieval_types import RetrievalResult

from reranker import rerank

from reranker import load_model as load_reranker

from dependency_retriever import inject_dependencies

from architecture_expander import (extract_architecture)

from architecture_validator import (validate_entities)



logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger=logging.getLogger(__name__)

INDEX_FILE = Path("vectorstore/bm25.pkl").resolve()
bm25_engine = BM25Engine(index_path = INDEX_FILE)

_init_lock = threading.Lock()

_corrector = None

_known_entities = None


def initialize():

    global _corrector
    global _known_entities

    if _corrector is not None:

        return (_corrector, _known_entities)

    with _init_lock:

        if _corrector is not None:

            return (_corrector, _known_entities)

        bm25_engine._load()

        load_reranker()

        _corrector = (QueryCorrector(bm25_engine._metadata))

        _known_entities = {row["metadata"].get("entity") for row in bm25_engine._metadata if row["metadata"].get("entity")}

    return (_corrector, _known_entities)

#30 May 8 to 12
TOP_K = 12
RRF_K = 60
POOL_MULTIPLIER = 3
MIN_POOL = 24
RERANK_POOL = 72
#30 May - added tiemouts 70
SECTION_PRIORITY={"argument reference":0, "example usage":1, "basic usage":2, "overview":50, "import":60, "timeouts": 70, "attribute reference":100, "required":101, "optional":102, "identity schema":103}
BAD_RERANK_SECTIONS = { "required", "optional", "identity schema", "timeouts"}
BAD_RERANK_PATTERNS = { "_required_", "_optional_", "_attribute_reference_", "_identity_schema_"}
HYDE_SKIP_TERMS = {"timeout", "timeouts", "argument", "arguments", "parameter", "parameters", "rotation", "ssh", "ttl", "ingress", "egress"}
BAD_ENTITY_CONTAMINATION={"aws_lambda_alias", "aws_ecr_lifecycle_policy_document", "aws_batch_compute_environment", "aws_transfer_ssh_key", "aws_ec2_host", "aws_datasync_location_efs", "aws_appautoscaling_scheduled_action", "aws_s3tables_table_bucket"}

#RRF(d)=∑r∈R 1 / (​k+r(d))

def rrf_score(rank:int):

    return 1/(RRF_K + rank)


def hybrid_retrieve(query:str, filters: Optional[dict] = None, k:int = TOP_K) -> list[RetrievalResult]:

    corrector, known_entities = initialize()

    if not query.strip(): return []

    intent = classify(query)

    original_query = query.strip()

    logger.info("Intent=%s | Query='%s'", intent.value, query)

    clean_query=corrector.correct(query)

    logger.info("Normalized Query = %s", clean_query)

    architecture_result=[]

    def fallback_architecture(output:list)->list[str]:

        entities=[]

        seen=set()

        for row in output[:3]:

            entity=(row.metadata.get("entity"))

            if (entity and entity not in seen):

                seen.add(entity)

                entities.append(entity)

        return entities

    def _run_arch():

        try:

            architecture_result.extend(extract_architecture(clean_query))

        except Exception:

            logger.exception("Architecture expansion failed")

    arch_thread=None

    if (intent == QueryIntent.ARCHITECTURE):

        retrieval_query=clean_query

        arch_thread=threading.Thread(target=_run_arch, daemon=True)

        arch_thread.start()

    else:

        tokens = set(re.sub(r"[^a-z0-9_ ]", " ", original_query.lower()).split())

        token_skip = bool(tokens & HYDE_SKIP_TERMS)

        short_query_skip = (len(tokens)<=3)

        skip_hyde = (bool(token_skip) or short_query_skip)
        
        #27 MAY ADD
        logger.info("SkipHyDE=%s " "TokenSkip=%s " "ShortSkip=%s " "Tokens=%s", skip_hyde, bool(token_skip), short_query_skip, tokens)

        if skip_hyde: 
            
            logger.info("HyDE bypassed")

            retrieval_query=original_query

        else: 
            
            hyde_query=(generate_hyde(original_query))

            retrieval_query = (hyde_query or original_query)

    start = time.perf_counter()

    pool_size = max(MIN_POOL, k * POOL_MULTIPLIER)

    dense = []
    sparse = []

    with concurrent.futures.ThreadPoolExecutor(max_workers = 2) as executor:

        dense_future = executor.submit(
            dense_retrieve,
            retrieval_query,
            filters = filters,
            k = pool_size
            )

        sparse_future = executor.submit(
            bm25_engine.retrieve,
            clean_query,
            k = pool_size,
            filters=filters
            )

        try:

            dense = dense_future.result(timeout=30)

        except concurrent.futures.TimeoutError:
            logger.warning("Dense retriever timed out")

        except Exception as exc:

            logger.warning("Dense Failed, sparse only: %s", exc)

        try:

            sparse = sparse_future.result(timeout=30)

            for row in sparse:
                if "aws_db_instance" in row.chunk_id:
                    logger.info(
                        "SPARSE DB_INSTANCE %s | %s",
                        row.chunk_id,
                        row.metadata.get("section")
                    )

        except concurrent.futures.TimeoutError:

            logger.warning("Sparse Retriever timeout")

        except Exception as exc:

            logger.warning("Sparse Failed, dense only: %s", exc)
       
    if not dense and not sparse:
        logger.warning("Both Retrievers Failed")
        return []

    scores=defaultdict(float)

    merged={}

    for rank, row in enumerate(dense, start=1):

        scores[row.chunk_id] += rrf_score(rank)

        merged[row.chunk_id] = replace(row, rrf_score = scores[row.chunk_id])

    for rank,row in enumerate(sparse, start=1):

        scores[row.chunk_id] += rrf_score(rank)

        if row.chunk_id not in merged:

            merged[row.chunk_id] = replace(row, rrf_score = scores[row.chunk_id])

            continue

        existing = merged[row.chunk_id]

        merged[row.chunk_id] = replace(existing, sparse_score=row.sparse_score, rrf_score=scores[row.chunk_id])

    ranked = sorted(scores.items(), key=lambda x:x[1], reverse=True)[:RERANK_POOL]

    #30 May
    logger.info("POST RRF=%s", len(ranked))

    output=[]

    for chunk_id, score in ranked:

        row = merged[chunk_id]

        output.append(replace(row, rrf_score = score))

    latency = time.perf_counter() - start

    logger.info(
        "Hybrid %.3fs | Dense = %s Sparse = %s Final = %s",
        latency,
        len(dense),
        len(sparse),
        [x.chunk_id for x in output]
    )

    for row in output: logger.info("PRE RERANK %s | %s", row.chunk_id,row.metadata.get("section"))

    filtered = []

    for row in output:

        section = (row.metadata.get("section", "").lower())

        chunk = row.chunk_id.lower()

        entity=(row.metadata.get("entity", ""))

        if (section in BAD_RERANK_SECTIONS): continue

        if any (pattern in chunk for pattern in BAD_RERANK_PATTERNS): continue

        if (entity in BAD_ENTITY_CONTAMINATION): continue

        filtered.append(row)

    if intent == QueryIntent.ARGUMENTS:

        rerank_query=(

            "Target Section: "

            "argument reference "

            "| User Query: "

            f"{query}"

        )

    elif intent == QueryIntent.EXAMPLE:

        rerank_query=(

            "Target Section: "

            "example usage "

            "| User Query: "

            f"{query}"

        )

    else:

        rerank_query=query

    rerank_input=(

        filtered

        if filtered

        else output

    )

    arch_entities=[]

    if arch_thread:

        arch_thread.join(timeout=12)

        if arch_thread.is_alive():

            logger.warning(

                "Architecture expansion timeout"

            )

            architecture_result=(

                fallback_architecture(output)

            )

        arch_entities=(

            validate_entities(

                architecture_result,

                known_entities

            )

        )

    seen_chunks={

        row.chunk_id

        for row

        in rerank_input

    }

    for entity in arch_entities:

        candidate_rows=[

            row

            for row

            in bm25_engine._metadata

            if (

                row["metadata"]

                .get("entity")

                ==entity

                and

                row["metadata"]

                .get("doc_type")

                =="resource"

            )

        ]

        candidate_rows.sort(

            key=lambda row:

            SECTION_PRIORITY.get(

                row["metadata"]

                .get(

                    "section",

                    ""

                )

                .lower(),

                50

            )

        )
        #30 May - 3 to 5
        for best in candidate_rows[:5]:

            chunk=(

                RetrievalResult(

                    chunk_id=best["chunk_id"],

                    text=best["text"],

                    metadata={

                        **best["metadata"],

                        "_architecture":True

                    },

                    similarity=None,

                    sparse_score=None,

                    rrf_score=None,

                    cross_encoder_score=None

                )

            )

            if (

                chunk.chunk_id

                in

                seen_chunks

            ):

                continue

            seen_chunks.add(

                chunk.chunk_id

            )

            rerank_input.append(

                chunk

            )
    #30 May
    logger.info("RERANK QUERY=%s", rerank_query)
    reranked=(rerank(rerank_query, rerank_input, max(k*3, 24)))
    logger.info("AWS_INSTANCE RERANKED:")

    for i, row in enumerate(reranked[:30]):
        logger.info(
            "%02d | %s | %s",
            i,
            row.chunk_id,
            row.metadata.get("section")
        )

    for i, row in enumerate(reranked):
        
        if "aws_db_instance_argument_reference" in row.chunk_id:

            logger.info(
                "DB_INSTANCE RANK=%02d | %s",
                i,
                row.chunk_id,
            )

    logger.info("POST POOL CAP=%s", len(reranked))

    #27 May change
    #seen_entities = set()

    entity_counts = defaultdict(int)

    output = []

    for row in reranked:
        if row.metadata.get("entity") == "aws_instance":
            logger.info("RANKED | %s", row.chunk_id)
        if "argument_reference_011" in row.chunk_id:
            logger.info("FOUND 011 IN RERANKED")

        entity = (row.metadata.get("entity", "") or row.chunk_id) 
        
        #27 may change
        #if (entity and entity in seen_entities and not row.metadata.get("_architecture")): continue

        section = (row.metadata.get("section", "").lower())
        limit = 1
        if section == "argument reference": 
            limit = 8

        #4 June
        if "aws_db_instance_argument_reference_011" in row.chunk_id:
            logger.info(
                "011 SEEN | section=%s | entity_count=%s | limit=%s",
                section,
                entity_counts[entity],
                limit,
            )
        if (entity and entity_counts[entity] >= limit and not row.metadata.get("_architecture")): continue
        
        if entity: 
            #seen_entities.add(entity)
            entity_counts[entity] += 1
            logger.info("COUNTING %s -> %s (%s)", entity, entity_counts[entity] + 1, row.chunk_id)
        
        #4 June
        logger.info("ADDING %s", row.chunk_id)
        output.append(row)

        #May 30
        if len(output) >= k: 
            logger.info("NEXT ROW=%s | %s | %s", row.metadata.get("entity"), row.metadata.get("section"), row.chunk_id)
            logger.info("FINAL OUTPUT COUNT=%s", len(output))
            logger.info("ENTITY COUNTS=%s",Counter(r.metadata.get("entity") for r in output))
            break
    
    core_context=output

    dependency_rows=[]

    if intent in {QueryIntent.ARCHITECTURE, QueryIntent.RESOURCE, QueryIntent.DEPENDENCY}:

        raw_rows=(inject_dependencies(core_context, bm25_engine))

        for row in raw_rows:

            new_meta={**row.metadata, "_dependency":True}

            dependency_rows.append(replace(row, metadata=new_meta))

            logger.info("AWS_INSTANCE SELECTED:")

    #30 May
    for row in output:

        if row.metadata.get("entity") == "aws_instance":

            logger.info(
                "%s | %s",
                row.chunk_id,
                row.metadata.get("section")
            )

    return (core_context + dependency_rows)

def display(results: list[RetrievalResult]):

    if not results:

        print("\n No Results \n")
        return
    
    primary_rank = 1
    dependency_rank = 1

    for row in results:

        dense = (
            f"{row.similarity:.2%}"
            if row.similarity is not None
            else "N/A"
        )

        sparse = (
            f"{row.sparse_score:.2f}"
            if row.sparse_score is not None
            else "N/A"
        )

        rrf = (
            f"{row.rrf_score:.5f}"
            if row.rrf_score is not None
            else "N/A"
        )

        cross = (
            f"{row.cross_encoder_score:.4f}"
            if row.cross_encoder_score is not None
            else "N/A"
        )

        text = (
            row.text[:700] + "..."
            if len(row.text) > 700
            else row.text
        )

        print("=" * 90)

        if row.metadata.get("_dependency"):

            print(f"Dependency: {dependency_rank}")

            dependency_rank += 1

        elif row.metadata.get("_architecture"):

            print("Architecture")

        else:

            print(f"Rank: {primary_rank}")

            primary_rank += 1

        print(
            f"Chunk: {row.chunk_id}"
        )

        print(
            f"Dense: {dense}"
        )

        print(
            f"Sparse: {sparse}"
        )

        print(
            f"RRF: {rrf}"
        )

        print(
            f"Cross: {cross}"
        )

        print(
            f"Service: "
            f"{row.metadata.get('service')}"
        )

        print(
            f"Entity: "
            f"{row.metadata.get('entity')}"
        )

        print(
            f"Type: "
            f"{row.metadata.get('doc_type')}"
        )

        print()
        print(text)
        print()

def main():

    logger.info("Hybrid Retriever Ready")

    while True:

        try:

            q = input("\nQuery (exit/help): ").strip()

            if not q: continue

            if q.lower() == "exit": break

            if q.lower() == "help":

                print(
                    "\nExamples:\n"
                    "aws_security_group_rule\n"
                    "kms key rotation\n"
                    "dynamodb ttl\n"
                    "how to trigger lambda from s3 upload\n"
                )

                continue

            results = hybrid_retrieve(q)

            display(results)

        except KeyboardInterrupt:

            print("\nGoodbye.")
            
            break

        except Exception as exc:

            logger.exception("Main loop failed: %s", exc)

            print(f"\nERROR: {exc}\n")

if __name__=="__main__":

    main()