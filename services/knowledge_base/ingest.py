import json

import chromadb

from services.knowledge_base.paths import DB_PATH, DATA_PATH


OPTIONAL_FIELDS = [
    "brand",
    "series",
    "model",
    "release_year",
    "price",
    "rating",
    "stock",
    "warranty",
    "description"
]

LIST_FIELDS = [
    "colors",
    "keywords",
    "recommended_for"
]


def get_collection():
    client = chromadb.PersistentClient(path=DB_PATH)
    return client.get_or_create_collection(
        name="shopnova",
        metadata={"hnsw:space": "cosine"}
    )


def ingest_data():

    collection = get_collection()

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    existing = collection.get()

    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    product_count = 0
    faq_count = 0
    policy_count = 0

    for item in data:

        metadata = {
            "title": item["title"],
            "type": item["type"],
            "category": item["category"]
        }

        # Store optional scalar fields
        for field in OPTIONAL_FIELDS:
            if field in item:
                metadata[field] = item[field]

        # Store list fields as comma-separated strings
        for field in LIST_FIELDS:
            if field in item:
                metadata[field] = ", ".join(item[field])

        try:
            collection.add(
                ids=[item["id"]],
                documents=[item["content"]],
                metadatas=[metadata]
            )

            if item["type"] == "product":
                product_count += 1
            elif item["type"] == "faq":
                faq_count += 1
            elif item["type"] == "policy":
                policy_count += 1

        except Exception as e:
            print(f"Failed to ingest '{item['title']}': {e}")

    print("\n========== Knowledge Base Loaded ==========")
    print(f"Products : {product_count}")
    print(f"FAQs     : {faq_count}")
    print(f"Policies : {policy_count}")
    print(f"Total    : {len(data)}")
    print("===========================================\n")

    return collection


if __name__ == "__main__":
    ingest_data()