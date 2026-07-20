import json
import os
from pathlib import Path
import chromadb

CHROMA_DB_PATH = Path(__file__).resolve().parents[2] / "db" / "chroma"
DATA_PATH = Path(__file__).resolve().parents[2] / "rohit_kb" / "data" / "shopnova_data.json"
if not DATA_PATH.exists():
    DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "shopnova_data.json"

OPTIONAL_FIELDS = [
    "brand", "series", "model", "release_year", "price", "rating", "stock", "warranty", "description"
]
LIST_FIELDS = ["colors", "keywords", "recommended_for"]

def ingest_shopnova_kb():
    client = chromadb.PersistentClient(path=str(CHROMA_DB_PATH))
    collection = client.get_or_create_collection(
        name="shopnova",
        metadata={"hnsw:space": "cosine"}
    )

    if not DATA_PATH.exists():
        print(f"Data file not found at {DATA_PATH}")
        return collection

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    existing = collection.get()
    if existing and existing.get("ids"):
        collection.delete(ids=existing["ids"])

    product_count = 0
    faq_count = 0
    policy_count = 0

    for item in data:
        metadata = {
            "title": item.get("title", ""),
            "type": item.get("type", ""),
            "category": item.get("category", "")
        }

        for field in OPTIONAL_FIELDS:
            if field in item and item[field] is not None:
                metadata[field] = str(item[field])

        for field in LIST_FIELDS:
            if field in item and isinstance(item[field], list):
                metadata[field] = ", ".join(str(x) for x in item[field])

        # Build enriched document text for high-accuracy RAG vector matching
        details_list = [f"{k.capitalize()}: {metadata[k]}" for k in OPTIONAL_FIELDS if k in metadata]
        doc_text = f"{item.get('title', '')} - {item.get('content', '')}"
        if details_list:
            doc_text += f" Details: {', '.join(details_list)}."

        try:
            collection.add(
                ids=[item["id"]],
                documents=[doc_text],
                metadatas=[metadata]
            )
            item_type = item.get("type")
            if item_type == "product": product_count += 1
            elif item_type == "faq": faq_count += 1
            elif item_type == "policy": policy_count += 1
        except Exception as e:
            print(f"Failed to ingest '{item.get('title')}': {e}")

    print("\n========== ShopNova Knowledge Base Loaded ==========")
    print(f"Products : {product_count}")
    print(f"FAQs     : {faq_count}")
    print(f"Policies : {policy_count}")
    print(f"Total    : {len(data)}")
    print("====================================================\n")
    return collection

if __name__ == "__main__":
    ingest_shopnova_kb()