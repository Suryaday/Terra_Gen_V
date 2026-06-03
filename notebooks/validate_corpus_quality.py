import json

with open(
    "C:/Users/Suryaday Nath/Downloads/Projects/RAG/data/processed/terraform_aws_corpus.json",
    encoding="utf-8"
) as f:

    docs = json.load(f)

print("Total docs:", len(docs))

services = set()

for d in docs:
    if d["service"]:
        services.add(d["service"])

print("\nServices:\n")
print("\n".join(sorted(list(services))[:20]))

print("\nSample document:\n")
print(docs[0].keys())