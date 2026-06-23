# main.py
from fastapi import FastAPI
from routes.chat import router as chat_router

app = FastAPI(title="AEGIS Backend", version="0.1.0")

app.include_router(chat_router)

@app.get("/")
def root():
    return {"status": "AEGIS backend running"}