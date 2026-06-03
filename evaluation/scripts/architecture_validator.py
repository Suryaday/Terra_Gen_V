from bm25_search import BM25Engine

from pathlib import Path

_bm25 = BM25Engine(Path("vectorstore/bm25.pkl"))


def validate_entities(entities, known_entities):

    return [entity for entity in entities if entity in known_entities]