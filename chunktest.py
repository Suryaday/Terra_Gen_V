from retriever import retrieve, collection

print("\n=== TEST 1 ===")
results = retrieve(
    "security group rules",
    filters={"doc_type": "resource"}
)

for r in results:
    print(r.chunk_id, r.metadata.get("doc_type"))

print("\n=== TEST 2 ===")
doc = collection.get(
    ids=["data_source_aws_vpc_security_group_rules_0"]
)

print(doc["metadatas"])

print("\n=== TEST 3 ===")
doc = collection.get(
    ids=["resource_aws_security_group_rule_0"]
)

print(doc["metadatas"])