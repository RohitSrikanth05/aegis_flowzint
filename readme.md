# AEGIS Flowzint

AEGIS Flowzint is a full-stack customer support and product-intelligence demo. It combines a FastAPI backend, Ollama-powered LLM calls, a SQLite session store, and a TanStack Start frontend for chat, trust monitoring, and admin workflows.

## What's In The Repo

- `main.py` starts the FastAPI app and mounts the API routers.
- `routes/` contains the chat and admin endpoints.
- `services/` contains the Ollama client, trust engine, knowledge-base pipeline, and product-intelligence pipeline.
- `utils/` contains the SQLite session and database helpers.
- `front-end/` contains the TanStack Start UI.
- `data/` and `rohit_kb/data/` contain sample source data used by the pipelines.

## Features

- Chat handling with intent routing for `SALES`, `SUPPORT`, `CARE`, and `PRODUCT_INTEL`.
- Trust scoring and escalation modes such as `NORMAL`, `CAUTIOUS`, and `LOCKDOWN`.
- Knowledge-base retrieval backed by ChromaDB and a learning queue for gaps.
- Product-intelligence workflows for prioritization, competitor analysis, and related signals.
- Admin views and routes for session summaries, queue review, and demo resets.
- Frontend views for guest chat and admin cockpit flows.

## Requirements

- Python 3.10+ recommended.
- Node.js 22.x for the frontend toolchain.
- Ollama running locally, with the configured model pulled.

If your default Node version is older than Vite's minimum, use `npx -y node@22.12.0` for frontend install/build commands.

## Backend Setup

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Set the optional Ollama environment variables if needed:

```bash
export OLLAMA_BASE_URL=http://localhost:11434
export OLLAMA_MODEL=gemma3:latest
```

Start the backend:

```bash
uvicorn main:app --reload --port 8000
```

The root endpoint returns a small health/status payload at `/`.

## Frontend Setup

From `front-end/`:

```bash
npm install
npm run dev
```

If you prefer Bun:

```bash
bun install
bun dev
```

Useful frontend commands:

```bash
npm run build
npm run preview
npm run lint
npm run format
```

## API Overview

The backend exposes these main routes:

- `POST /chat` - main chat endpoint.
- `GET /learning-queue` - list unresolved knowledge gaps.
- `POST /learning-queue/{id}/approve` - synthesize and ingest an answer.
- `POST /learning-queue/{id}/reject` - reject a queued item.
- `POST /session/reset` - reset sessions and trust scores.
- `GET /sessions` and `GET /admin/sessions` - session and trust summaries.

Admin-only backend workflows expect the `X-AEGIS-ROLE: admin` header.

## Frontend Views

The UI includes two main experiences:

- `/guest` for chat-only access.
- `/admin` for the trust and security cockpit.

## Testing

There are lightweight Python test scripts in the repository root, including:

```bash
python test_chat.py
python test_kb_pipeline.py
python test_retrieval_check.py
```

These scripts expect the backend and any required local services to be running.

## Data And Storage

- SQLite data is created under `db/`.
- ChromaDB data is stored under `db/chroma/`.
- The repository also includes sample JSON and CSV inputs for the product-intelligence and knowledge-base pipelines.

## Notes

- CORS is currently open in development so the frontend can reach the backend easily.
- The backend will fall back gracefully if Ollama is unavailable, but full behavior depends on a running Ollama server.
