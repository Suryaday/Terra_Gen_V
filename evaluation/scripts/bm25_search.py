from __future__ import annotations

import logging
import pickle
from pathlib import Path
from typing import Any

from bm25_retriever import tokenize

from retrieval_types import RetrievalResult


INDEX_FILE = Path("vectorstore/bm25.pkl").resolve()
TOP_K = 8

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


class BM25Engine:

    def __init__(self, index_path: Path):

        self.index_path = index_path
        self._bm25 = None
        self._metadata = None

    def _load(self):
        if self._bm25 is not None:
            return
        
        if not self.index_path.exists():
            raise FileNotFoundError(f"BM25 index not found at {self.index_path}. Run Indexer first")
        
        logger.info(f"Loading BM25 index from {self.index_path} into memory...")

        with open(self.index_path, "rb") as f:
            data = pickle.load(f)
            self._bm25 = data["bm25"]
            self._metadata = data["metadata"]
        
        logger.info("BM25 index loaded successfully")


    def retrieve(self, query: str, k: int = TOP_K, filters:dict|None=None) -> list[RetrievalResult]: 
        
        self._load()

        tokens = tokenize(query)

        if not tokens: return []  

        scores = self._bm25.get_scores(tokens)

        ranked = sorted(((idx, score) for idx, score in enumerate(scores) if score > 0), 
                        key=lambda x:x[1], 
                        reverse=True)

        results = []

        for idx, score in ranked:

            if score <= 0.0: continue

            row = self._metadata[idx]

            if filters:

                if not all(row["metadata"].get(key)==v for key,v in filters.items()):
                    continue

            results.append(
                RetrievalResult(
                    chunk_id=row["chunk_id"],
                    text=row["text"],
                    metadata=row["metadata"],
                    sparse_score=float(score)
                )
            )

            if len(results) >= k: break

        return results


def display(results: list[RetrievalResult]):

    if not results:
        print("\n[!] No exact keyword matches found.\n")
        return

    for rank, row in enumerate(results, start=1):

        print("=" * 90)

        print(f"Rank: {rank}")
        print(f"BM25: {row.sparse_score:.4f}")
        print(f"Chunk: {row.chunk_id}")
        print(f"Entity: {row.metadata.get('entity', 'N/A')}")
        print(f"Service: {row.metadata.get('service', 'N/A')}")
        print("\nCONTENT\n")

        text = row.text

        if len(text) > 600:
            text = text[:600] + "..."
        
        print(text)
        print()


def main():
    logger.info("Initializing BM25 Search Engine")

    engine = BM25Engine(INDEX_FILE)

    while True:
        try:
            q = input("\nQuery (exit to quit): ").strip()
            if q.lower() == "exit":
                break
            if not q:
                continue

            results = engine.retrieve(q)
            display(results)

        except KeyboardInterrupt:
            print("\nGoodbye.")
            break
        except Exception as e:
            logger.error(f"Search failed: {e}")


if __name__ == "__main__":
    main()