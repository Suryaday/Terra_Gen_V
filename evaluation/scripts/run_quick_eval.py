from __future__ import annotations

import json
import math
import statistics

from pathlib import Path
from datetime import datetime
from collections import defaultdict

from hybrid_retriever import hybrid_retrieve

from reranker import load_model


TOP_K = 8

DATASET = (
    Path(__file__)
    .resolve()
    .parents[1]
    / "golden_quick.json"
)

RESULTS_FILE = (
    Path(__file__)
    .resolve()
    .parents[1]
    / "results"
    / "latest_quick.json"
)


def relevance(entity: str, case: dict) -> float:

    if not entity:
        return 0.0

    if entity in case.get("primary", []):

        return 1.0

    if entity in case.get("acceptable", []):

        return 0.7

    return 0.0


def success_at_1(rows, case) -> int:

    if not rows:
        return 0

    entity = (
        rows[0]
        .metadata
        .get("entity")
    )

    return int(
        relevance(entity, case) > 0
    )


def recall_at_k(rows, case) -> int:

    for row in rows:

        entity = (
            row.metadata
            .get("entity")
        )

        if relevance(entity, case) > 0:

            return 1

    return 0


def reciprocal_rank(rows, case) -> float:

    for rank, row in enumerate(
        rows,
        start=1
    ):

        entity = (
            row.metadata
            .get("entity")
        )

        if relevance(entity, case) > 0:

            return 1 / rank

    return 0


def ndcg(rows, case, k=TOP_K) -> float:

    dcg = 0

    seen = set()

    for rank, row in enumerate(
        rows[:k],
        start=1
    ):

        entity = (
            row.metadata
            .get("entity")
        )

        if entity in seen:
            continue

        seen.add(entity)

        rel = relevance(entity, case)

        dcg += (
            rel / math.log2(rank + 1)
        )

    ideal = []

    ideal.extend(
        [1.0] * len(case.get("primary", []))
    )

    ideal.extend(
        [0.7] * len(case.get("acceptable", []))
    )

    ideal.sort(reverse=True)

    ideal = ideal[:k]

    idcg = 0

    for rank, rel in enumerate(
        ideal,
        start=1
    ):

        idcg += (
            rel / math.log2(rank + 1)
        )

    if not idcg:

        return 0

    return dcg / idcg


def evaluate():

    load_model()

    dataset = json.loads(
        DATASET.read_text()
    )

    recalls = []

    reciprocal_ranks = []

    successes = []

    ndcgs = []

    failures = []

    results = []

    category_success = defaultdict(list)

    type_success = defaultdict(list)

    print()
    print("=" * 100)

    for case in dataset:

        query = case["query"]

        rows = hybrid_retrieve(
            query,
            k=TOP_K
        )

        recall = recall_at_k(
            rows,
            case
        )

        rr = reciprocal_rank(
            rows,
            case
        )

        success = success_at_1(
            rows,
            case
        )

        ndcg_score = ndcg(
            rows,
            case
        )

        recalls.append(recall)

        reciprocal_ranks.append(rr)

        successes.append(success)

        category_success[case["category"]].append(success)

        type_success[case["type"]].append(success)

        ndcgs.append(ndcg_score)

        rank1 = (
            rows[0]
            .metadata
            .get("entity")
            if rows
            else "EMPTY"
        )

        top_results = []

        for row in rows[:5]:

            top_results.append({

                "entity":
                    row.metadata.get(
                        "entity"
                    ),

                "section":
                    row.metadata.get(
                        "section"
                    ),

                "score":
                    getattr(
                        row,
                        "score",
                        None
                    )
            })

        result = {

            "query":
                query,

            "primary":
                case.get(
                    "primary",
                    []
                ),

            "acceptable":
                case.get(
                    "acceptable",
                    []
                ),

            "category":
                case.get(
                    "category"
                ),

            "type":
                case.get(
                    "type"
                ),

            "success_at_1":
                success,

            "recall_at_k":
                recall,

            "reciprocal_rank":
                rr,

            "ndcg":
                ndcg_score,

            "rank1":
                rank1,

            "top_results":
                top_results,

            "failure_type": None
        }

        results.append(result)

        if not success:

            failures.append(result)

        print(
            f"{query:<40} "
            f"S@1={success:<1} "
            f"RR={rr:.3f} "
            f"nDCG={ndcg_score:.3f} "
            f"R1={rank1}"
        )

    final = {

        "timestamp":
            datetime.utcnow().isoformat(),

        "dataset":
            str(DATASET),

        "top_k":
            TOP_K,

        "metrics": {

            "recall_at_k":
                statistics.mean(recalls),

            "mrr":
                statistics.mean(
                    reciprocal_ranks
                ),

            "success_at_1":
                statistics.mean(
                    successes
                ),

            "ndcg":
                statistics.mean(
                    ndcgs
                ),

            "total_failures": len(failures),

            "category_metrics": {

                category:
                    statistics.mean(scores)

                for category, scores
                in category_success.items()
            }, 

            "type_metrics": {

                query_type:
                    statistics.mean(scores)

                for query_type, scores
                in type_success.items()
            }
        },

        "failures":
            failures,

        "results":
            results
    }

    RESULTS_FILE.write_text(
        json.dumps(
            final,
            indent=2
        )
    )

    print()

    print("=" * 100)

    print(
        f"Recall@{TOP_K}: "
        f"{statistics.mean(recalls):.3f}"
    )

    print(
        f"MRR: "
        f"{statistics.mean(reciprocal_ranks):.3f}"
    )

    print(
        f"Success@1: "
        f"{statistics.mean(successes):.3f}"
    )

    print(
        f"nDCG@{TOP_K}: "
        f"{statistics.mean(ndcgs):.3f}"
    )

    print("=" * 100)

    print()

    print(
        f"Results written to:\n"
        f"{RESULTS_FILE}"
    )

    print()

    print("CATEGORY SUCCESS@1")

    for category, scores in category_success.items():

        print(
            f"{category:<20} "
            f"{statistics.mean(scores):.3f}"
        )

    print()

    print("TYPE SUCCESS@1")

    for query_type, scores in type_success.items():

        print(
            f"{query_type:<20} "
            f"{statistics.mean(scores):.3f}"
        )

if __name__ == "__main__":

    evaluate()

