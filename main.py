from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.kb import router as kb_router

app = FastAPI(
    title="AEGIS Knowledge Base",
    description="RAG retrieval and self-healing knowledge base for AEGIS",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(
    kb_router,
    prefix="/kb",
    tags=["Knowledge Base"]
)


@app.get("/")
def home():

    return {
        "status": "running",
        "service": "AEGIS Knowledge Base"
    }


@app.on_event("startup")
async def startup_check():
    try:
        from services.knowledge_base.retriever import collection
        count = collection.count()
        print(f"[STARTUP] ChromaDB connected — {count} documents loaded")
    except Exception as e:
        print(f"[STARTUP ERROR] ChromaDB failed to connect: {e}")
