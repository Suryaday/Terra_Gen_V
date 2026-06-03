#Inspect Raw Embeddings - Quick Sanity Check
import chromadb
import numpy as np
import os
import umap
import matplotlib.pyplot as plt

from openai import OpenAI
from dotenv import load_dotenv
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai_client = OpenAI(api_key=OPENAI_API_KEY)

client = chromadb.PersistentClient(path="vectorstore/chroma")

collection = client.get_collection("terraform_docs")

results = collection.peek(5)

for i in range(5):

    embedding = results["embeddings"][i]

    print("\nID:", results["ids"][i])

    print("Dimensions:",len(embedding))

    print("First 10 values:", embedding[:10])

    print("Norm:", np.linalg.norm(embedding))

#Similarity Sanity Check

query = """terraform ec2 instance launch template"""

query_embedding = openai_client.embeddings.create(model="text-embedding-3-small", input=query).data[0].embedding

results = collection.query(query_embeddings=[query_embedding], n_results=5)

for doc in results["documents"][0]:

    print("="*80)

    print(doc[:500])


#Visualize Embeddings (2D Map)

client = chromadb.PersistentClient(path="vectorstore/chroma")

collection = client.get_collection("terraform_docs")

data = collection.get(include=["embeddings", "metadatas"])

embeddings = np.array(data["embeddings"])

print(embeddings.shape)

metadata = data["metadatas"]

services = [m["service"] for m in metadata]

reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, random_state=42)

projection = reducer.fit_transform(embeddings)

plt.figure(figsize=(14,10))

scatter = plt.scatter(projection[:,0], projection[:,1], alpha=0.5)

plt.title("Terraform Embedding Space")

plt.show()


#Color by Metadata

encoder = LabelEncoder()

labels = encoder.fit_transform(services)

plt.figure(figsize=(14,10))

scatter = plt.scatter(projection[:,0], projection[:,1], c=labels, cmap="tab20", alpha=0.6)

plt.colorbar(scatter)

plt.title("Terraform Service Clustering")

plt.show()


#Distance Distribution

sample = embeddings[:1000]

similarities = cosine_similarity(sample)

upper = similarities[np.triu_indices_from(similarities,k=1)]

plt.hist(upper,bins=50)

plt.title("Cosine Similarity Distribution")

plt.show()
