from __future__ import annotations

import json
import re
from pathlib import Path

from generator import generate

DATASET = Path("evaluation/generation_eval.json")

FAILURES_FILE = Path("evaluation/generation_failures.txt")

RESOURCE_PATTERN = re.compile(
    r'^\s*resource\s+"([^"]+)"', 
    re.MULTILINE
)


def extract_resources(terraform_text: str) -> set[str]:

    return set(
        RESOURCE_PATTERN.findall(terraform_text)
    )


def evaluate():

    dataset = json.loads(
        DATASET.read_text(
            encoding="utf-8"
        )
    )

    failures = []

    passed = 0

    total = len(dataset)

    print()
    print("=" * 100)
    print("GENERATION EVALUATION")
    print("=" * 100)

    for case in dataset:

        query = case.get("query", "UNKNOWN QUERY")
        required_resources = set(case.get("required_resources", []))

        print()
        print(f"Running: {query}")

        try:

            result = generate(query)

        except Exception as exc:

            failures.append({

                "query": query,

                "error": str(exc),

                "missing": list(required_resources),

                "generated": []
            })

            print(f"ERROR: {exc}")

            continue

        main_tf = result.files.get(
            "main.tf",
            ""
        )

        generated_resources = (
            extract_resources(main_tf)
        )

        missing = sorted(

            required_resources
            -
            generated_resources

        )

        if not missing:

            passed += 1

            print("PASS")

        else:

            print(
                f"FAIL | Missing: {missing}"
            )

            failures.append({

                "query": query,

                "missing": missing,

                "generated": sorted(
                    generated_resources
                )
            })

    with open(
        FAILURES_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            "=" * 100
            + "\n"
        )

        f.write(
            "GENERATION FAILURES\n"
        )

        f.write(
            "=" * 100
            + "\n\n"
        )

        if not failures:

            f.write(
                "No failures.\n"
            )

        else:

            for failure in failures:

                f.write(
                    "=" * 100
                    + "\n"
                )

                f.write(
                    f"QUERY:\n"
                    f"{failure['query']}\n\n"
                )

                if "error" in failure:

                    f.write(
                        f"ERROR:\n"
                        f"{failure['error']}\n\n"
                    )

                f.write(
                    "MISSING:\n"
                )

                for item in failure["missing"]:

                    f.write(
                        f"  - {item}\n"
                    )

                f.write("\n")

                f.write(
                    "GENERATED:\n"
                )

                for item in failure.get(
                    "generated",
                    []
                ):

                    f.write(
                        f"  - {item}\n"
                    )

                f.write("\n")

    print()
    print("=" * 100)

    pass_pct = (passed / total) if total > 0 else 0.0
    print(
        f"PASS RATE: "
        f"{passed}/{total} "
        f"({pass_pct:.1%})"
    )

    print(
        f"Failure report:\n"
        f"{FAILURES_FILE}"
    )

    print("=" * 100)


if __name__ == "__main__":

    evaluate()