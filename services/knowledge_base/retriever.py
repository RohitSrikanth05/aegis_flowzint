import chromadb

from services.knowledge_base.paths import DB_PATH


def get_collection():
    client = chromadb.PersistentClient(path=DB_PATH)
    return client.get_or_create_collection(
        name="shopnova",
        metadata={"hnsw:space": "cosine"}
    )


collection = get_collection()


def retrieve(query: str, n_results: int = 3):

    total_documents = collection.count()

    if total_documents == 0:
        return []

    n_results = min(n_results, total_documents)

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    retrieved = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        item = {
            "content": document,
            "title": metadata.get("title"),
            "type": metadata.get("type"),
            "category": metadata.get("category"),

            "brand": metadata.get("brand"),
            "series": metadata.get("series"),
            "model": metadata.get("model"),

            "price": metadata.get("price"),
            "rating": metadata.get("rating"),
            "stock": metadata.get("stock"),

            "release_year": metadata.get("release_year"),
            "warranty": metadata.get("warranty"),

            "description": metadata.get("description"),

            "keywords": metadata.get("keywords"),
            "recommended_for": metadata.get("recommended_for"),
            "colors": metadata.get("colors"),

            "distance": round(float(distance), 4),

            # Higher is better (0-100)
            "similarity": round(
                max(0.0, (1 - float(distance))) * 100,
                2
            )
        }

        retrieved.append(item)

    retrieved.sort(
        key=lambda x: x["distance"]
    )

    return retrieved