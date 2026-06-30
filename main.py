# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.chat import router as chat_router
from routes.admin import router as admin_router

# Initialize database on startup
import utils.database  # noqa: F401 - triggers init_db() on import

app = FastAPI(
    title="AEGIS Backend",
    version="1.0.0",
    description=(
        "Adaptive Enterprise Guardian Intelligence System — "
        "FastAPI backend integrating Ollama LLM, ChromaDB RAG, and Trust Engine."
    )
)

# ── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # In production, restrict to the frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ──────────────────────────────────────────────────────────────────
app.include_router(chat_router)
app.include_router(admin_router)


@app.get("/")
def root():
    return {
        "status": "AEGIS backend running",
        "version": "1.0.0",
        "endpoints": {
            "chat": "POST /chat",
            "learning_queue": "GET /learning-queue",
            "approve_item": "POST /learning-queue/{id}/approve",
            "reject_item": "POST /learning-queue/{id}/reject",
            "reset_session": "POST /session/reset",
        }
    }