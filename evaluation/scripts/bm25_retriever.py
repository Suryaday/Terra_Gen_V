from __future__ import annotations

import json
import logging
import pickle
import re
from pathlib import Path
from typing import Any

from rank_bm25 import BM25Okapi

# ======================================================
# CONFIG
# ======================================================

CHUNKS_FILE = Path("data/chunks/terraform_chunks.json").resolve()
INDEX_FILE = Path("vectorstore/bm25.pkl").resolve()

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

STOPWORDS = {
    "the", "a", "an", "is", "in", "it", "to", "and", "of",
    "for", "on", "with", "as", "by", "this", "that",
    "are", "be", "or"
}


# ======================================================
# TOKENIZER
# ======================================================

def tokenize(text: str) -> list[str]:
    """
    Infrastructure-aware tokenizer.

    Preserves:
    aws_security_group_rule
    us-east-1
    t3.micro
    10.0.0.0/16
    """

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9_\-\.\/]+",
        " ",
        text
    )

    tokens = []

    for term in text.split():

        clean = term.strip(".-")

        if not clean: continue

        if clean in STOPWORDS: continue

        if len(clean) == 1 and not clean.isdigit(): continue

        tokens.append(clean)

    return tokens


# ======================================================
# PAYLOAD BUILDER
# ======================================================

def build_searchable_payload(chunk: dict[str, Any]) -> str:

    entity = chunk.get("terraform_entity", "")
    service = chunk.get("service", "")

    headers = " ".join(
        str(v)
        for v in (chunk.get("header_metadata") or {}).values()
    )

    text = chunk.get("text", "")

    boosted_entity = f"{entity} " * 3
    boosted_service = f"{service} " * 2

    return f"{boosted_entity} {boosted_service} {headers} {text}"


# ======================================================
# BM25 BUILD
# ======================================================

def build():

    if not CHUNKS_FILE.exists():
        raise FileNotFoundError(f"Missing chunks file: {CHUNKS_FILE}")

    logger.info("Loading chunks")

    with open(CHUNKS_FILE, encoding="utf-8") as f:
        chunks = json.load(f)

    logger.info(f"Chunks loaded: {len(chunks)}")

    corpus = []
    metadata = []

    skipped = 0

    for chunk in chunks:

        raw_text = chunk.get("text", "").strip()

        if not raw_text:
            skipped += 1
            continue

        payload = build_searchable_payload(chunk)

        tokens = tokenize(payload)

        if not tokens:
            skipped += 1
            continue

        corpus.append(tokens)

        metadata.append({
            "chunk_id": chunk["chunk_id"],
            "text": raw_text,
            "metadata": {
                "service": chunk.get("service", ""),
                "entity": chunk.get("terraform_entity", ""),
                "doc_type": chunk.get("doc_type", ""),
                "section": chunk.get("section", "")
            }
        })

    logger.info(f"Indexed docs: {len(corpus)}")
    logger.info(f"Skipped docs: {skipped}")

    logger.info("Fitting BM25")

    bm25 = BM25Okapi(corpus)

    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)

    logger.info("Saving BM25")

    with open(INDEX_FILE, "wb") as f:
        pickle.dump(
            {
                "bm25": bm25,
                "metadata": metadata
            },
            f
        )

    logger.info("BM25 COMPLETE")
    logger.info(f"Saved -> {INDEX_FILE}")


if __name__ == "__main__":
    build()