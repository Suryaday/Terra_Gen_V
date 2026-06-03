from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RetrievalResult:

    chunk_id:str

    text:str

    metadata:dict[str,Any]

    similarity:float|None=None

    distance:float|None=None

    dense_score:float|None=None

    sparse_score:float|None=None

    rrf_score:float|None=None

    cross_encoder_score:float|None=None