from __future__ import annotations

import warnings

import logging

import torch

from functools import lru_cache

from sentence_transformers import CrossEncoder

from retrieval_types import RetrievalResult

from dataclasses import replace

from torch import nn

logger=logging.getLogger(__name__)


#MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L6-v2"
#MODEL_NAME="BAAI/bge-reranker-base"
MODEL_NAME = "BAAI/bge-reranker-v2-m3"
_MODEL=None

warnings.filterwarnings(
    "ignore",
    category=Warning,
    module="requests"
)

@lru_cache(maxsize=1)

def load_model():

    logger.info("Loading reranker %s", MODEL_NAME)

    device=("cuda" if torch.cuda.is_available() else "cpu")

    logger.info("Reranker device=%s", device)

    try:

        _MODEL=CrossEncoder(

            MODEL_NAME,

            device=device,

            default_activation_function = nn.Identity()

        )

        logger.info("Reranker loaded OK")

        return _MODEL

    except Exception:

        logger.exception("Reranker load failed")

        raise


def rerank(query:str, rows:list[RetrievalResult], k:int) -> list[RetrievalResult]:

    if not rows:

        return []

    model=load_model()

    #pairs=[(query,row.text) for row in rows]

    #27 May change

    pairs=[]

    for row in rows:

        section=(row.metadata.get("section", ""))

        entity=(row.metadata.get("entity",""))

        service=(row.metadata.get("service", ""))

        chunk=(

            f"Entity: {entity}\n"

            f"Service: {service}\n"

            f"Section: {section}\n\n"

            f"{row.text}"

        )

        rerank_query = query

        if "jump box" in query.lower():

            rerank_query += (
                " bastion host "
                "security group "
                "public subnet "
                "ssh access "
                "public ip "
                "key pair "
                "network interface "
            )

        pairs.append((rerank_query, chunk))

    scores=model.predict(pairs, batch_size=32, show_progress_bar=False)

    rescored=[]

    for row,score in zip(rows, scores):

        rescored.append(

            replace(row, cross_encoder_score = float(score))

        )

    rescored.sort(key=lambda x:x.cross_encoder_score, reverse=True)
    return rescored[:k]