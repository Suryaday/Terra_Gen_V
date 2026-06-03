from __future__ import annotations

import logging

from dependency_expander import expand_entities

from retrieval_types import RetrievalResult

logger = logging.getLogger(__name__)

SECTION_PRIORITY={"argument reference":0, "example usage":1, "basic usage":2, "overview":50, "import":60, "attribute reference":100, "required":101, "optional":102, "identity schema":103}

def inject_dependencies(
    rows: list, bm25_engine,
    hard_only: bool = True
) -> list:

    top_entities = []

    for row in rows[:2]:

        entity = (
            row.metadata
            .get("entity")
        )

        if entity:

            top_entities.append(
                entity
            )

    if not top_entities:

        return []

    expanded = expand_entities(
        top_entities,
        hard_only=hard_only
    )

    existing_entities = {

        row.metadata
        .get("entity")

        for row
        in rows

        if row.metadata
        .get("entity")
    }

    needed_dependencies = [

        entity

        for entity
        in expanded

        if entity
        not in existing_entities

    ]

    dependency_rows = []

    seen_chunks = set()

    for entity in needed_dependencies:

        candidate_rows = [

            row

            for row

            in bm25_engine._metadata

            if (

                row["metadata"]
                .get("entity")

                == entity

                and

                row["metadata"]
                .get("doc_type")

                == "resource"

            )

        ]

        candidate_rows.sort(

            key=lambda row:

            (SECTION_PRIORITY.get(row["metadata"].get("section", "").lower(), 50)))

        results=[]

        if candidate_rows:

            best=candidate_rows[0]

            results.append(

                RetrievalResult(

                    chunk_id=best["chunk_id"],

                    text=best["text"],

                    metadata=best["metadata"],

                    sparse_score=None,

                    similarity=None,

                    rrf_score=None,

                    cross_encoder_score=None

                )

            )

        if not results:

            results = bm25_engine.retrieve(

                query=entity,

                filters={

                    "entity":
                    entity

                },

                k=1

            )

        for row in results:

            if (

                row.chunk_id
                in seen_chunks

            ):

                continue

            seen_chunks.add(
                row.chunk_id
            )

            dependency_rows.append(
                row
            )

    if dependency_rows:

        logger.info(

            "Dependency context injected=%s | %s",

            len(
                dependency_rows
            ),

            needed_dependencies

        )

    return dependency_rows