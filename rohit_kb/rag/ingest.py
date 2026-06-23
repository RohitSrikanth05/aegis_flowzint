import json
import chromadb

client = chromadb.PersistentClient(
    path="./db/chroma"
)

collection = client.get_or_create_collection(
    name="shopnova"
)

with open(
    "seed_data/shopnova_data.json",
    "r",
    encoding="utf-8"
) as f:
    data = json.load(f)

existing = collection.get()

if len(existing["ids"]) > 0:
    collection.delete(ids=existing["ids"])

for item in data:
    collection.add(
        ids=[item["id"]],
        documents=[item["content"]],
        metadatas=[
            {
                "title": item["title"],
                "type": item["type"],
                "category": item["category"]
            }
        ]
    )

print(f"Loaded {len(data)} documents into ChromaDB")