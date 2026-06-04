import json
from pathlib import Path

input = Path("data/chunks/terraform_chunks.json")

with open(input, encoding="utf-8") as f:
    data = json.load(f)

for chunk in data:
    if chunk.get("terraform_entity") == "aws_db_instance":
        if chunk['chunk_id'] == "resource_aws_db_instance_argument_reference_011":
            print(f"{chunk['chunk_id']} | {chunk['section']} | {chunk['text']}")