#Makes Python treat all type hints as strings, so List[Str] can be used
from __future__ import annotations

import concurrent.futures  #Python's built-in parallel execution framework uses a thread pool
import itertools  #Create efficient loops -> used here to make batches from a list
import json 
import logging #Print log messages with timestamps and severity levels
import os  #Interact with os, read env
import threading  #Semaphores - limits how many tasks run at once
import time  #Measures how long things take

from datetime import datetime, timezone   #Current date & time including timezone
from pathlib import Path

#Type hints for better code clarity
from typing import (
    Any,
    Dict,
    Iterable,
    Iterator,
    List
)

import chromadb
import tiktoken #Open AI Tokenizer - count tokens locally for free before making API Calls

from chromadb.config import Settings #import config settings for ChromaDB - eg. telemetry off
from dotenv import load_dotenv
from openai import OpenAI

#A retry library - if API calls fail - exponential backoff
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential
)

from tqdm import tqdm  #Shows progress bars for long running loops


# =====================================================
# CONFIG
# =====================================================

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

#If key not found, stop immediately with error

if not OPENAI_API_KEY: raise RuntimeError("OPENAI_API_KEY missing") 

#Folder Structure Awareness

INPUT_FILE = Path("data/chunks/terraform_chunks.json")

VECTOR_DIR = Path("vectorstore/chroma")

ARTIFACT_DIR = Path("artifacts")

ARTIFACT_DIR.mkdir(exist_ok=True)

FAILED_FILE = (ARTIFACT_DIR /"failed_batches.json") #Failed Chunk IDs get written

MANIFEST_FILE = (ARTIFACT_DIR /"embedding_manifest.json")  #Run Summary / AUDIT LOG

COLLECTION_NAME = ("terraform_docs")   #The name of the collection (like a table) inside Chromadb

EMBED_MODEL = ("text-embedding-3-small")

CORPUS_VERSION = "v1" #Get's written into every chunk's metadata in ChromaDB

PIPELINE_VERSION = ("phase2_final") #Stamped into every vector's metadata

MAX_TOKENS_PER_CHUNK = 8190  #text-embeddin-3-small's hard limit is 8191

BATCH_SIZE = 100 #How many chunks to send in 1 API Call

MAX_CONCURRENT_REQUESTS = 5 #Max Parallel threads hitting OPENAI simultaneously

EMBED_COST_PER_1M = 0.02  #OPEN AI PUBLISHED RATE


# =====================================================
# LOGGING
# =====================================================

#Configure logging to show time, severity(INFO) and message

logging.basicConfig(level=logging.INFO, format=("%(asctime)s | " "%(levelname)s | " "%(message)s"))

#Creates a logger object to print messages throughout the script
logger = logging.getLogger(__name__)

# =====================================================
# CLIENTS
# =====================================================

openai_client = OpenAI(api_key=OPENAI_API_KEY)

#Loads tokenizer that matches text-embedding-3-small - to count tokens locally
tokenizer = (tiktoken.encoding_for_model(EMBED_MODEL))

#Opens or creates a Chromda DB stored on disk at VECTOR_DIR, telemetry OFF - doesn't send any usage data
chroma_client = (chromadb.PersistentClient(path=str(VECTOR_DIR), settings=Settings(anonymized_telemetry=False)))

#Inside Chroma, gets or craetes a collection (table) where embeddings will be stored
collection = (chroma_client.get_or_create_collection(name=COLLECTION_NAME, metadata={"description": "Terraform AWS corpus"}))

# Protect OpenAI concurrency

#A Semaphore is a concurrency gate - prevents all 5 concurrent threads from blasting OpenAI simultaneously and triggering rate limit errors
rate_limit = threading.Semaphore(MAX_CONCURRENT_REQUESTS)


# =====================================================
# HELPERS
# =====================================================

#To read input JSON FILE - opens files, parse JSON content and returns it as Python list/dict
#Reads whole JSON file and returns a list of chunk dicts - called once at start of main()
def load_chunks():

    if not INPUT_FILE.exists(): raise FileNotFoundError(INPUT_FILE)

    with open(INPUT_FILE, encoding="utf-8") as f: return json.load(f)


#Takes a list or any iterable and a batch size and returns one batch at a time until nothing left
#Splits any list into groupos of size - main uses it to split chunk list into batches of BATCH_SIZE
def batched(iterable:Iterable, size:int)->Iterator:

    it=iter(iterable)  #Creates iterator from the list

#Loop - slice out size items, if slice empty -> stop otherwise hand batch out via YIELD
    while True:

        batch=list(itertools.islice(it, size))

        if not batch: return

        yield batch

#Encode batch tokenizes all texts in one shot - len gives token count for each text, sum gives total tokens for the entire run
#main estimates total tokens upfront for cost reporting and each chunk's token count to check against the limit
def estimate_tokens(texts:List[str])->int: 
    return sum(len(t) for t in tokenizer.encode_batch(texts))

#Coverts token counts to dollars
def estimate_cost(tokens:int)->float: 
    return (tokens/1_000_000) * EMBED_COST_PER_1M

#Safely writes JSON data to a file, avoids corruption if program crashes mid-write
#main writes the final failed_batches.json and embedding_manifest.json
def atomic_write_json(data,path:Path):

    temp=path.with_suffix(".tmp")  #Creates a temporary file name e.g., failed_batches.tmp

    #Write data to a temporary file
    with open(temp, "w", encoding="utf-8") as f:

        json.dump(data, f, indent=2, ensure_ascii=False)

    temp.replace(path)     #Automatically rename the temp file to the final name

#Retry decorator wrapped around the actual function that calls OpenAi to get embeddings (Exponential backoff algorithm)
@retry(

    wait=wait_exponential(multiplier=2, min=2, max=30),

    stop=stop_after_attempt(5)

)

#Core API call - sends lists of texts to Open AI, gets embedding vectors back
#Submitted to the thread pool - once per batch
def create_embeddings(texts:List[str]):
    #Acquire the semaphore, only 5 threads can be inside the block at once
    with rate_limit:

        response=(openai_client.embeddings.create(model=EMBED_MODEL, input=texts))   #Call OpenAI API with the list of texts

    embeddings=[x.embedding for x in response.data]  #Extract the actual embedding vectors from the response

    #Safety check - we should get one embedding per input text
    if len(embeddings) != len(texts):

        raise RuntimeError("Embedding count mismatch")

    return embeddings

#Takes one chunk's raw data and builds a clean metadata dictionary for ChromaDB
#Called for every valid chunk in a batch
def sanitize_metadata(row:Dict[str,Any]):

    meta={

        "service": str(row.get("service") or "unknown"),   #Fills in standard fields using .get() with defaults

        "entity": str(row.get("terraform_entity") or "unknown"),

        "doc_type": str(row.get("doc_type") or "unknown"),

        "chunk_index": int(row.get("chunk_index") or 0),

        "source_file": str(row.get("source_file") or "unknown"),

        "embedding_model": EMBED_MODEL,

        "corpus_version": CORPUS_VERSION,

        "pipeline_version": PIPELINE_VERSION

    }

    #If chunk has extra metadata under header_metadata, prefix those keys with header_ and add them
    headers=(row.get("header_metadata") or {})

    for k,v in headers.items():

        if v:

            meta[f"header_{k}"]=str(v)

    return meta

#Creates a small dict (event) for a failed chunk, recording what went wrong
#Called whenever a chunk or batch fails
def dlq_event(error_type:str, chunk_ids:List[str], message:str):

    return {

        "timestamp": datetime.now(timezone.utc).isoformat(),

        "error_type": error_type,

        "chunk_ids": chunk_ids,

        "message":message

    }


# =====================================================
# MAIN - runs in 4 phases: Preparation -> Token & Cost Estimation -> Parallel Batch Processing -> Finalization
# =====================================================

"""

Phase A: Preparation

Start a high precision timer.

Initialise counters (metrics) and an empty failed list.

Load chunks via load_chunks().

Query ChromaDB for existing IDs, filter out already stored chunks.

If nothing new, exit early.


"""


def main():

    pipeline_start=(time.perf_counter()) #Records the start time (high-precision) to measure total duration later

    failed=[]  #Collects error events for chunks that fail

    #Dict to count success, failures, API Calls, batches and tokens
    metrics={

        "chunks_success":0,

        "chunks_failed":0,

        "api_calls":0,

        "batches":0,

        "tokens":0

    }

    logger.info("Loading chunks")

    chunks=load_chunks()  #Loads list of chunk dictionaries from input JSON

    #Get all IDs already stored in Chromadb - put them into a set for fast lookup
    existing=(collection.get(include=[]))

    indexed=set(existing["ids"])

    #Filter out any chunks whose ID already exists in the DB - only new chunks remain
    chunks=[c for c in chunks if c.get("chunk_id") not in indexed]

    if not chunks:

        logger.info("Nothing to embed")

        return

    """
    Phase B: Token & cost estimation (upfront)
    Use estimate_tokens() on all remaining texts to get an approximate total.

    Log chunk count, token count, and estimated dollar cost.

    """
    #Counts total tokens of all texts - only those with "text" field & store in metrics
    metrics["tokens"]=(estimate_tokens([c["text"] for c in chunks if c.get("text")])) 

    #Logs total chunks, tokens and estimated cost
    logger.info(f"Chunks: " f"{len(chunks)}")

    logger.info(f"Tokens: " f"{metrics['tokens']:,}")

    logger.info(f"Estimated cost " f"${estimate_cost(metrics['tokens']):.4f}")

    """
    Phase C: Parallel batch processing

    Split the remaining chunks into batches with batched().

    Open a thread pool (ThreadPoolExecutor) that can run up to MAX_CONCURRENT_REQUESTS jobs at once.

    For each batch:

    Inspect every chunk: skip empty ones, discard oversized chunks (with failure recording).

    Collect valid IDs, texts, and metadata.

    Submit create_embeddings(texts) to the pool; store the future in a dictionary together with the batchs IDs, texts, and metadata.

    As futures complete (as_completed), retrieve the embeddings, upsert them into ChromaDB (collection.upsert), and update success counters. If any future raised an exception, record the whole batch as failed.
    
    """

    #Dict to keep track of parallel tasks - each task is a batch being processed
    futures={}

    #Split all chunks into batches of size BATCH_SIZE
    batches=list(batched(chunks, BATCH_SIZE))

    #Start a thread pool that can run upto 5 tasks at the same time
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_CONCURRENT_REQUESTS) as executor:

        #Go through each batch - for each batch, prepare empty lists for IDs, texts and metadata
        for batch in batches:

            ids=[]
            texts=[]
            metadata=[]

            #For each chunk in batch
            for row in batch:

                text=(row.get("text","").strip())   #Get the text, strip whitespace; if empty, skip this chunk

                if not text:continue

                #Counts how many tokens this single text has
                token_count=len(tokenizer.encode(text))

                #If it's too big, we can't embed it (>8190 tokens)
                if token_count > MAX_TOKENS_PER_CHUNK:
                    
                    #Record failure, increment the failed count and skip to the next chunk
                    failed.append(dlq_event("oversized_chunk", [row["chunk_id"]], (f"{token_count} tokens")))

                    metrics["chunks_failed"] += 1

                    continue

                #Otherwise add it's ID, text and cleaned metadata to the batch lists
                ids.append(row["chunk_id"])

                texts.append(text)

                metadata.append(sanitize_metadata(row))

            #If after filtering the batch has no valid texts, skip this batch entirely
            if not texts:continue

            #Submit the batch to the thread pool for embedding, store the future object along with the batch data in the dict
            future=(executor.submit(create_embeddings, texts))

            futures[future]=(ids, texts, metadata)

        #As each submitted job finishes(in any order), iterate over them with a progress bar
        for future in tqdm(concurrent.futures.as_completed(futures),

            total=len(futures)

        ):

            ids,texts,metadata=(futures[future])    #Retieve the batch data we stored when we submitted the job

            batch_start=(time.perf_counter())       #Start timing the batch's database insertion

            try:
                #Get the actual embeddings returned by the API call, if the call raises exception, this will re-raise inside try block
                embeddings=(future.result())   

                #Insert or update these chunks into chromadb with embeddings, original texts and metadata
                collection.upsert(

                    ids=ids,

                    embeddings=embeddings,

                    documents=texts,

                    metadatas=metadata

                )

                #Update counts
                metrics["chunks_success"] += len(ids)

                metrics["api_calls"] += 1

                metrics["batches"] += 1

            #If anything goes wrong (API error, DB error etc.), record all chunk IDs in that batch as failed, log the error and increment failure count
            except Exception as exc:

                failed.append(dlq_event("batch_failure", ids, str(exc)))

                metrics["chunks_failed"] += len(ids)

                logger.exception(exc)
            
            #Log how long the batch took
            elapsed=(time.perf_counter() - batch_start)

            logger.info(f"Batch {elapsed:.2f}s")

    """
    Phase D: Finalisation
    
    Stop the clock.

    Build a manifest dictionary with run stats, duration, throughput, and cost.

    Write the failed batch list and the manifest to disk using atomic_write_json().

    Log the manifest as pretty printed JSON.
    
    """

    #Log how long the batch took
    duration=(time.perf_counter() - pipeline_start)

    #Build summary dict with timestamp, model, versions, number of vectors in collection, metrics, duration, speed and estimated cost
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

    #Write failed events and manifest to their respective files safely
    atomic_write_json(failed, FAILED_FILE)

    atomic_write_json(manifest, MANIFEST_FILE)

    #Print summary to the log - nicely formatted
    logger.info(json.dumps(manifest, indent=2))


if __name__=="__main__":

    main()