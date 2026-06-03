from __future__ import annotations

import concurrent.futures  #Python's built-in parallel execution framework
import itertools
import json
import logging
import os
import threading
import time

from datetime import datetime, timezone
from pathlib import Path

from typing import (
    Any,
    Dict,
    Iterable,
    Iterator,
    List
)

import chromadb
import tiktoken #Open AI Tokenizer - count tokens locally for free before making API Calls

from chromadb.config import Settings
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
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential
)

from tqdm import tqdm


# =====================================================
# CONFIG
# =====================================================

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY: raise RuntimeError("OPENAI_API_KEY missing")

#Folder Structure Awareness

INPUT_FILE = Path("data/chunks/terraform_chunks.json")

VECTOR_DIR = Path("vectorstore/chroma")

ARTIFACT_DIR = Path("artifacts")

ARTIFACT_DIR.mkdir(exist_ok=True)

FAILED_FILE = (ARTIFACT_DIR /"failed_batches.json") #Failed Chunk IDs get written

MANIFEST_FILE = (ARTIFACT_DIR /"embedding_manifest.json")  #Run Summary / AUDIT LOG

LOCK_FILE = ARTIFACT_DIR/ "pipeline.lock"

COLLECTION_NAME = ("terraform_docs")

EMBED_MODEL = ("text-embedding-3-small")

CORPUS_VERSION = "v1" #Get's written into every chunk's metadata in ChromaDB

PIPELINE_VERSION = ("phase2_final") #Stamped into every vector's metadata

MAX_TOKENS_PER_CHUNK = 8190  #text-embeddin-3-small's hard limit is 8191

BATCH_SIZE = 64

MAX_CONCURRENT_REQUESTS = 2 #Max Parallel threads hitting OPENAI simultaneously

EMBED_COST_PER_1M = 0.02  #OPEN AI PUBLISHED RATE


# =====================================================
# LOGGING
# =====================================================

logging.basicConfig(level=logging.INFO, format=("%(asctime)s | " "%(levelname)s | " "%(message)s"))

logger = logging.getLogger(__name__)

# =====================================================
# CLIENTS
# =====================================================

openai_client = OpenAI(api_key=OPENAI_API_KEY)

#Loads tokenizer that matches text-embedding-3-small
tokenizer = (tiktoken.encoding_for_model(EMBED_MODEL))

chroma_client = (chromadb.PersistentClient(path=str(VECTOR_DIR), settings=Settings(anonymized_telemetry=False)))

collection = (chroma_client.get_or_create_collection(name=COLLECTION_NAME, metadata={"description": "Terraform AWS corpus"}))

# Protect OpenAI concurrency

#A Semaphore is a concurrency gate - prevents all 5 concurrent threads from blasting OpenAI simultaneously and triggering rate limit errors
rate_limit = threading.Semaphore(MAX_CONCURRENT_REQUESTS)


# =====================================================
# HELPERS
# =====================================================

def load_chunks():

    if not INPUT_FILE.exists(): raise FileNotFoundError(INPUT_FILE)

    with open(INPUT_FILE, encoding="utf-8") as f: return json.load(f)


def batched(iterable:Iterable, size:int)->Iterator:

    it=iter(iterable)

    while True:

        batch=list(itertools.islice(it, size))

        if not batch: return

        yield batch

#Encode batch tokenizes all texts in one shot - len gives token count for each text, sum gives total tokens for the entire run
def estimate_tokens(texts:List[str])->int: return sum(len(t) for t in tokenizer.encode_batch(texts))

#Coverts token counts to dollars
def estimate_cost(tokens:int)->float: return (tokens/1_000_000) * EMBED_COST_PER_1M


def atomic_write_json(data,path:Path):

    temp=path.with_suffix(".tmp")

    with open(temp, "w", encoding="utf-8") as f:

        json.dump(data, f, indent=2, ensure_ascii=False)

    temp.replace(path)


@retry(
        
    retry = retry_if_exception_type((RateLimitError, APITimeoutError, APIConnectionError, InternalServerError)),

    wait=wait_exponential(multiplier=2, min=2, max=30),

    stop=stop_after_attempt(5)

)

def create_embeddings(texts:List[str]):

    with rate_limit:

        response=(openai_client.embeddings.create(model=EMBED_MODEL, input=texts))

    embeddings=[x.embedding for x in response.data]

    if len(embeddings) != len(texts):

        raise RuntimeError("Embedding count mismatch")

    return embeddings


def sanitize_metadata(row:Dict[str,Any]):

    meta={

        "service": str(row.get("service") or "unknown"),

        "entity": str(row.get("terraform_entity") or "unknown"),

        "doc_type": str(row.get("doc_type") or "unknown"),

        "section": str(row.get("section") or "unknown"),

        "chunk_index": int(row.get("chunk_index") or 0),

        "source_file": str(row.get("source_file") or "unknown"),

        "embedding_model": EMBED_MODEL,

        "corpus_version": CORPUS_VERSION,

        "pipeline_version": PIPELINE_VERSION

    }

    headers=(row.get("header_metadata") or {})

    for k,v in headers.items():

        if v:

            meta[f"header_{k}"]=str(v)

    return meta


def dlq_event(error_type:str, chunk_ids:List[str], message:str):

    return {

        "timestamp": datetime.now(timezone.utc).isoformat(),

        "error_type": error_type,

        "chunk_ids": chunk_ids,

        "message":message

    }


# =====================================================
# MAIN
# =====================================================

def main():

    pipeline_start=(time.perf_counter())

    failed=[]

    metrics={

        "chunks_success":0,

        "chunks_failed":0,

        "api_calls":0,

        "batches":0,

        "tokens":0

    }

    logger.info("Loading chunks")

    chunks=load_chunks()

    existing=(collection.get(include=[]))

    indexed=set(existing["ids"])

    chunks=[c for c in chunks if c.get("chunk_id") not in indexed]

    if not chunks:

        logger.info("Nothing to embed")

        return

    metrics["tokens"]=(estimate_tokens([c["text"] for c in chunks if c.get("text")]))

    logger.info(f"Chunks: " f"{len(chunks)}")

    logger.info(f"Tokens: " f"{metrics['tokens']:,}")

    logger.info(f"Estimated cost " f"${estimate_cost(metrics['tokens']):.4f}")

    futures={}

    batches=list(batched(chunks, BATCH_SIZE))

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_CONCURRENT_REQUESTS) as executor:

        for batch in batches:

            ids=[]
            texts=[]
            metadata=[]

            for row in batch:

                text=(row.get("text","").strip())

                if not text:continue

                token_count=len(tokenizer.encode(text))

                if token_count > MAX_TOKENS_PER_CHUNK:

                    failed.append(

                        dlq_event("oversized_chunk", [row["chunk_id"]], (f"{token_count} tokens")))

                    metrics["chunks_failed"] += 1

                    continue

                ids.append(row["chunk_id"])

                texts.append(text)

                metadata.append(sanitize_metadata(row)) 

            if not texts:continue

            future=(executor.submit(create_embeddings, texts))

            futures[future]=(ids, texts, metadata, time.perf_counter())

        for future in tqdm(concurrent.futures.as_completed(futures),

            total=len(futures)

        ):

            ids,texts,metadata,batch_start=(futures[future])

            try:

                embeddings=(future.result())

                collection.upsert(

                    ids=ids,

                    embeddings= embeddings,

                    documents= texts,

                    metadatas= metadata

                )

                metrics["chunks_success"] += len(ids)

                metrics["api_calls"] += 1

                metrics["batches"] += 1

            except Exception as exc:

                failed.append(dlq_event("batch_failure", ids, str(exc)))

                metrics["chunks_failed"] += len(ids)

                logger.exception(exc)

            elapsed=(time.perf_counter() - batch_start)

            logger.info(f"Batch {elapsed:.2f}s")

    duration=(time.perf_counter() - pipeline_start)

    manifest={

        "created_at": datetime.now(timezone.utc).isoformat(),

        "embedding_model": EMBED_MODEL,

        "pipeline_version": PIPELINE_VERSION,

        "corpus_version": CORPUS_VERSION,

        "vector_count": collection.count(),

        "metrics": metrics,

        "duration_seconds": round(duration,2),

        "chunks_per_second": round(metrics["chunks_success"] / duration, 2),

        "estimated_cost": round(estimate_cost(metrics["tokens"]), 4)

    }

    atomic_write_json(failed, FAILED_FILE)

    atomic_write_json(manifest, MANIFEST_FILE)

    logger.info(json.dumps(manifest, indent=2))


if __name__=="__main__":

    main()