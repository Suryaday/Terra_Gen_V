import chromadb

client = chromadb.PersistentClient(
    path="vectorstore/chroma"
)

collection = client.get_collection(
    "terraform_docs"
)

print(collection.count())

sample = collection.peek(5)

print(sample["ids"])