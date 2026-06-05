import json
from pathlib import Path

input = Path("data/chunks/terraform_chunks.json")

with open(input, encoding="utf-8") as f:
    data = json.load(f)

for chunk in data:
    if "bucket_namespace" in chunk["text"]:
        print(chunk["chunk_id"])
        print(chunk["title"])
        print(chunk["terraform_entity"])