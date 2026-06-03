import json

with open(
"data/chunks/terraform_chunks.json",
encoding="utf-8"
) as f:

    chunks=json.load(f)

ids=[

x["chunk_id"]

for x in chunks

]

print(len(ids))

print(len(set(ids)))