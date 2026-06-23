import chromadb

client = chromadb.PersistentClient(
    path="./db/chroma"
)

collection = client.get_or_create_collection(
    name="shopnova"
)


def retrieve(query, n_results=3):

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    formatted = []

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    for doc, meta in zip(docs, metas):

        formatted.append(
            {
                "content": doc,
                "title": meta["title"],
                "type": meta["type"],
                "category": meta["category"]
            }
        )

    return formatted