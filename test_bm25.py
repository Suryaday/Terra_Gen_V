from bm25_search import BM25Engine
from pathlib import Path
from typing import Optional

INDEX_FILE = Path("vectorstore/bm25.pkl").resolve()

def _get_bm25() -> BM25Engine:

    global _bm25

    if _bm25 is None:

        _bm25 = BM25Engine(INDEX_FILE)
        _bm25._load()

    return _bm25

_bm25: Optional[BM25Engine] = None

bm25 = _get_bm25()

print(type(bm25._metadata))

print(type(bm25._metadata[0]))

print(bm25._metadata[0])