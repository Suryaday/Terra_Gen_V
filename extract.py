import os
import re
import json
import yaml
from pathlib import Path


PROJECT_ROOT = Path("C:/Users/Suryaday Nath/Downloads/Projects/RAG")

TERRAFORM_DOCS_DIR = PROJECT_ROOT / "terraform-provider-aws" / "website" / "docs"

DOCS_PATHS = [
    TERRAFORM_DOCS_DIR / "r",
    TERRAFORM_DOCS_DIR / "d",
]

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

os.makedirs(OUTPUT_DIR, exist_ok=True)

documents = []


def extract_frontmatter(content):

    match = re.match(r"---(.*?)---", content, re.DOTALL)

    if not match:
        return {}, content

    frontmatter_raw = match.group(1)

    try:
        metadata = yaml.safe_load(frontmatter_raw)
    except Exception:
        metadata = {}

    remaining_content = content[match.end():]

    return metadata, remaining_content


def extract_code_blocks(content):

    pattern = r"```(?:\w+)?\n(.*?)```"

    return re.findall(pattern, content, re.DOTALL)


for docs_path in DOCS_PATHS:

    for file_path in Path(docs_path).glob("*.markdown"):

        try:

            with open(file_path, "r", encoding="utf-8") as f:
                raw_content = f.read()

            metadata, markdown_content = extract_frontmatter(raw_content)

            code_blocks = extract_code_blocks(markdown_content)

            terraform_entity = ""

            title = metadata.get("page_title", "")

            if ":" in title:
                terraform_entity = (title.split(":")[-1].strip())

            doc = {
                "title": metadata.get("page_title", ""),
                "terraform_entity": terraform_entity,
                "service": metadata.get("subcategory", ""),
                "description": metadata.get("description", ""),
                "layout": metadata.get("layout", ""),
                "source_file": file_path.name,
                "doc_type": (
                    "resource"
                    if "/r/" in str(file_path)
                    else "data_source"
                ),
                "content": markdown_content.strip(),
                "code_blocks": code_blocks,
            }

            documents.append(doc)

        except Exception as e:
            print(f"Error processing {file_path}: {e}")


output_file = f"{OUTPUT_DIR}/terraform_aws_corpus.json"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(documents, f, indent=2, ensure_ascii=False)

print(f"\nProcessed {len(documents)} documents")
print(f"Saved to {output_file}")