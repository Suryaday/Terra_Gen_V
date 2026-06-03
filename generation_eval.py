from __future__ import annotations

import json
import re
import subprocess
import tempfile
import os

from pathlib import Path

from generator import generate

DATASET = Path("evaluation/generation_eval.json")

FAILURES_FILE = Path("generation_failures.txt")

RESOURCE_PATTERN = re.compile(r'^\s*resource\s+"([^"]+)"', re.MULTILINE)

TF_CACHE_DIR = (Path.home() / ".terraform.d" / "plugin-cache")

TF_CACHE_DIR.mkdir(parents=True, exist_ok=True)

os.environ["TF_PLUGIN_CACHE_DIR"] = str(TF_CACHE_DIR)

def extract_resources(terraform_text: str) -> set[str]:

    return set(RESOURCE_PATTERN.findall(terraform_text))

def terraform_checks(files: dict[str, str]) -> tuple[bool, str]:

    try:

        with tempfile.TemporaryDirectory() as tmpdir:

            workdir = Path(tmpdir)

            for filename, content in files.items():

                (workdir / filename).write_text(content, encoding="utf-8")

            fmt = subprocess.run(
                ["terraform", "fmt"],
                cwd=workdir,
                capture_output=True,
                text=True,
            )

            if fmt.returncode != 0:

                return (
                    False,
                    f"terraform fmt failed:\n{fmt.stdout}\n{fmt.stderr}"
                )

            init = subprocess.run(
                [
                    "terraform",
                    "init",
                    "-backend=false",
                    "-input=false"
                ],
                cwd=workdir,
                capture_output=True,
                text=True,
            )

            if init.returncode != 0:

                return (False, f"terraform init failed:\n{init.stdout}\n{init.stderr}")

            validate = subprocess.run(
                [
                    "terraform",
                    "validate"
                ],
                cwd=workdir,
                capture_output=True,
                text=True,
            )

            if validate.returncode != 0:

                return (False, f"terraform validate failed:\n{validate.stdout}\n{validate.stderr}")

            return (True, "")

    except Exception as exc:

        return (False, str(exc))
    
def evaluate():

    dataset = json.loads(DATASET.read_text(encoding="utf-8"))

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

        main_tf = result.files.get("main.tf", "")

        terraform_ok, terraform_error = terraform_checks(result.files)

        generated_resources = (extract_resources(main_tf))

        missing = sorted(required_resources - generated_resources)

        has_warnings = bool(result.warnings)

        if (not missing and terraform_ok):

            passed += 1

            print(f"PASS | Generated: {sorted(generated_resources)}")

            if has_warnings:

                print(f"  WARNINGS: {result.warnings}")

        else:
            
            print("FAIL")

            if missing:

                print(f"FAIL | Missing: {missing}")

            if has_warnings:

                print(f"WARNINGS: {result.warnings}")

            if not terraform_ok:
                 print(f"  -> TF Error: {terraform_error[:200]}")

            failures.append({

                "query": query,

                "missing": missing,

                "generated": sorted(generated_resources),

                "warnings": result.warnings,

                "terraform_error": terraform_error,

                "main_tf": main_tf
            })

    with open(FAILURES_FILE, "w", encoding="utf-8") as f:

        f.write(
            "=" * 100
            + "\n"
        )

        f.write("GENERATION FAILURES\n")

        f.write("=" * 100 + "\n\n")

        if not failures:

            f.write("No failures.\n")

        else:

            for failure in failures:

                f.write("=" * 100 + "\n")

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

                    f.write(f"  - {item}\n")

                f.write("\n")
                f.write("GENERATED:\n")

                for item in failure.get("generated", []):

                    f.write(f"  - {item}\n")

                f.write("\n")

                if failure.get("warnings"):

                    f.write("WARNINGS:\n")

                    for warning in failure["warnings"]:

                        f.write(f"  - {warning}\n")

                    f.write("\n")

                if failure.get("terraform_error"):

                    f.write("TERRAFORM ERROR:\n\n")

                    f.write(failure["terraform_error"])

                    f.write("\n\n")

                if failure.get("main_tf"):

                    f.write("MAIN.TF:\n\n")

                    f.write(failure["main_tf"])

                    f.write("\n\n")

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