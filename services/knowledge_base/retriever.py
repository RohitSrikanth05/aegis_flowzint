import asyncio
import chromadb

client = chromadb.PersistentClient(
    path="./db/chroma"
)

collection = client.get_or_create_collection(
    name="shopnova"
)


async def retrieve(query, n_results=5):
    def _query():
        return collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
    results = await asyncio.to_thread(_query)

    formatted = []

    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]

    for doc, meta in zip(docs, metas):
        # Format metadata attributes into a readable details string
        details = []
        for k in ["price", "rating", "stock", "warranty", "brand", "model", "release_year", "colors", "recommended_for"]:
            if k in meta and meta[k]:
                details.append(f"{k}: {meta[k]}")

        formatted.append(
            {
                "content": doc,
                "title": meta.get("title", ""),
                "type": meta.get("type", ""),
                "category": meta.get("category", ""),
                "details": ", ".join(details) if details else "",
                "metadata": meta,
            }
        )

    return formatted