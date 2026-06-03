from __future__ import annotations

import logging
import os
import time
from functools import lru_cache
from pathlib import Path
from typing import Optional

from retrieval_types import RetrievalResult

import chromadb
import tiktoken

from dotenv import load_dotenv

from openai import (
    OpenAI,
    RateLimitError,
    APITimeoutError,
    APIConnectionError,
    InternalServerError
)

from tenacity import (
    retry,
    wait_exponential,
    stop_after_attempt,
    retry_if_exception_type
)


# ======================================================
# CONFIG
# ======================================================

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY missing")

CHROMA_PATH = Path("vectorstore/chroma").resolve()

COLLECTION_NAME = "terraform_docs"
EMBED_MODEL = "text-embedding-3-small"

TOP_K = 8
#MAX_DISTANCE = 0.8
#27 MAY 1.2 to 1.45
MAX_DISTANCE = 1.2
MAX_QUERY_TOKENS = 8191
OPENAI_TIMEOUT = 30


# ======================================================
# LOGGING
# ======================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# ======================================================
# CLIENTS
# ======================================================

openai_client = OpenAI(api_key=OPENAI_API_KEY, timeout=OPENAI_TIMEOUT)

tokenizer = tiktoken.encoding_for_model(EMBED_MODEL)

if not CHROMA_PATH.exists():
    raise RuntimeError(f"Missing Chroma path {CHROMA_PATH}")

chroma_client = chromadb.PersistentClient(path=str(CHROMA_PATH))

collection = chroma_client.get_collection(COLLECTION_NAME)


# ======================================================
# TELEMETRY
# ======================================================

telemetry = {
    "queries_total": 0,
    "api_calls": 0,
    "results_total": 0,
    "cache_hits": 0,
    "cache_misses": 0,
    "validation_errors": 0,
    "retrieval_errors": 0,
    "empty_results": 0,
    "avg_embedding_latency": 0.0,
    "avg_retrieval_latency": 0.0,
    "avg_similarity": 0.0
}


# ======================================================
# HELPERS
# ======================================================

def update_average(metric: str, counter_key: str, value: float):

    total = telemetry[counter_key]

    if total <= 0:
        return

    prev = telemetry[metric]

    telemetry[metric] = ((prev * (total - 1)) + value) / total


def validate_query(query: str):

    tokens = len(tokenizer.encode(query))

    if tokens > MAX_QUERY_TOKENS:
        raise ValueError(f"Query exceeds {MAX_QUERY_TOKENS} tokens")

# ======================================================
# EMBEDDING
# ======================================================

@lru_cache(maxsize=512)
@retry(
    wait=wait_exponential(multiplier=1, min=1, max=10),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type(
        (
            RateLimitError,
            APITimeoutError,
            APIConnectionError,
            InternalServerError
        )
    )
)
def embed_query(query: str) -> tuple[float, ...]:

    validate_query(query)

    start = time.perf_counter()

    response = openai_client.embeddings.create( model=EMBED_MODEL, input=query)

    latency = time.perf_counter() - start

    telemetry["api_calls"] += 1

    update_average(
        "avg_embedding_latency",
        "api_calls",
        latency
    )

    return tuple(response.data[0].embedding)


# ======================================================
# RETRIEVAL
# ======================================================

def retrieve(question: str, filters: Optional[dict] = None, k: int = TOP_K) -> list[RetrievalResult]:

    cache_before = embed_query.cache_info().hits

    embedding = list(embed_query(question))

    cache_after = embed_query.cache_info().hits

    if cache_after > cache_before:
        telemetry["cache_hits"] += 1
    else:
        telemetry["cache_misses"] += 1

    params = {
        "query_embeddings": [embedding],
        "n_results": k,
        "include": ["documents", "metadatas","distances"]
    }

    if filters:
        params["where"] = filters

    start = time.perf_counter()

    result = collection.query(**params)

    latency = time.perf_counter() - start

    telemetry["queries_total"] += 1

    update_average("avg_retrieval_latency", "queries_total", latency)

    docs = result.get("documents", [[]])[0]
    meta = result.get("metadatas", [[]])[0]
    dist = result.get("distances", [[]])[0]
    ids = result.get("ids", [[]])[0]

    if not docs:
        telemetry["empty_results"] += 1
        return []

    output = []

    batch_similarity = 0.0
    valid_results = 0

    for chunk_id, text, metadata, distance in zip(ids, docs, meta, dist):

        #27 MAY ADD
        logger.info(f"Dense {chunk_id} dist={distance:.4f}")

        if distance > MAX_DISTANCE: continue

        similarity = max(0.0, 1.0 - distance/2)

        batch_similarity += similarity
        valid_results += 1

        telemetry["results_total"] += 1

        output.append(
            RetrievalResult(
                chunk_id=chunk_id,
                text=text,
                metadata=metadata,
                distance=distance,
                similarity=similarity
            )
        )

    if valid_results:

        update_average("avg_similarity", "queries_total", batch_similarity / valid_results)

    else: 

        update_average("avg_similarity", "queries_total", 0.0)

    if not output:
        telemetry["empty_results"] += 1

    logger.info(
        "Retrieved=%s",
        [x.chunk_id for x in output]
    )

    return output


# ======================================================
# DISPLAY
# ======================================================

def display(chunks: list[RetrievalResult]):

    if not chunks:
        print("\nNo results.\n")
        return

    for idx, chunk in enumerate(chunks, start=1):

        text = chunk.text

        if len(text) > 700:
            text = text[:700] + "..."

        print("=" * 90)

        print(f"Rank: {idx}")

        print(
            f"Similarity: "
            f"{chunk.similarity:.2%}"
        )

        print(
            f"Chunk: "
            f"{chunk.chunk_id}"
        )

        print(
            f"Service: "
            f"{chunk.metadata.get('service','N/A')}"
        )

        print(
            f"Entity: "
            f"{chunk.metadata.get('entity','N/A')}"
        )

        print(
            f"Type: "
            f"{chunk.metadata.get('doc_type','N/A')}"
        )

        print("\nContent\n")

        print(text)

        print()


# ======================================================
# MAIN
# ======================================================

def main():

    logger.info("Terraform Retriever Ready")

    while True:

        try:

            q = input("\nQuestion (exit/help): ").strip()

            if q == "exit":
                break

            if q == "help":

                print(
                    "\nExamples:\n"
                    "terraform ec2 launch template\n"
                    "kms key rotation\n"
                    "dynamodb ttl\n"
                )

                continue

            if not q: continue

            chunks = retrieve(q)

            display(chunks)

        except KeyboardInterrupt:

            logger.info(telemetry)

            print("\nGoodbye.\n")

            break

        except ValueError as exc:

            telemetry["validation_errors"] += 1

            logger.warning(exc)

            print("\nInvalid query.\n")

        except Exception as exc:

            telemetry["retrieval_errors"] += 1

            logger.exception(exc)

            print("\nTry again.\n")

    logger.info(telemetry)

if __name__ == "__main__":
    main()