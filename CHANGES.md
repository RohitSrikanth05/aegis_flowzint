# CHANGES — Knowledge Base Module (Rohit)

This is the fixed, final version of everything under `services/knowledge_base/`,
`routes/kb.py`, and root `main.py`. What changed from the last checkpoint and why:

## Fixed

1. **DB path bug (critical, was live-breaking retrieval).**
   `retriever.py` and `approval.py` were computing `DB_PATH` one directory level
   too shallow, resolving to `services/db/chroma` — an empty ChromaDB collection —
   while `ingest.py` wrote real data to `db/chroma` (85 documents). Every query
   was silently hitting the empty collection: confidence always 0, everything
   flagged as a learning gap.

   Fix: added `services/knowledge_base/paths.py` as the single source of truth
   for `DB_PATH` and `DATA_PATH`. `ingest.py`, `retriever.py`, and `approval.py`
   all import from it now — this can't drift apart again.

   Verified: booting the app now logs
   `[STARTUP] ChromaDB connected — 85 documents loaded` (see #2 below), and
   `collection.count()` returns 85 from the code path that's actually used at
   runtime, not just from a manual one-off check.

2. **Missing CORS in root `main.py`.**
   It existed in the abandoned `rohit_kb/main.py` but not in the `main.py` that's
   actually wired up. Added `CORSMiddleware` (allow all origins/methods/headers
   for now — tighten before final submission if there's time).

3. **`rohit_kb/` restructure removed.**
   It was missing `rag/confidence.py`, `rag/ingest.py`, `rag/pipeline.py`,
   `rag/retriever.py`, and `learning/gap_logger.py` (never committed, confirmed
   via `git log`), and `api/routes.py` / `learning/approval.py` were empty
   stubs. Not salvageable in the time left. The startup healthcheck pattern
   from its `main.py` was kept and ported into root `main.py` (see below).
   Root `services/knowledge_base/` is now the one and only canonical structure.

4. **Stale `services/db/chroma/` deleted.** It was the empty, wrong-path
   ChromaDB collection created by the bug above. No longer referenced anywhere.

## Added

5. **Startup healthcheck in `main.py`.** On boot, pings ChromaDB and logs the
   document count, so a broken DB path (or any Chroma connection issue) shows
   up immediately in the server logs instead of silently returning empty
   results.

6. **`query_type` support**, to unblock Swathi's intent routing:
   - `POST /kb/search` now accepts an optional `query_type` field
     (`spec_lookup` / `policy` / `complaint` / `general` — defaults to `None`
     if omitted, fully backward compatible).
   - `pipeline.py`'s `process_query()` threads it through and returns it in the
     response.
   - `gap_logger.py` stores it on each learning-queue item (defaults to
     `"general"` if not provided).
   - `approval.py`'s `_draft_entry()` now branches the Groq drafting prompt on
     `query_type` via a new `_build_prompt()` — a different template for specs,
     policy answers, and complaint resolutions, falling back to the original
     FAQ template when `query_type` is missing or unrecognized. This is the one
     feature ported from the Product Intelligence Copilot repo (their
     `graph.py` query-routing idea), reimplemented without LangGraph.

   Verified with unit tests: `gap_logger.log_gap()` correctly stores each
   `query_type` (and defaults to `"general"`), and all four prompt templates in
   `approval._build_prompt()` produce distinct output.

## Not included in this zip

- **`.env`** — never zip or commit this. Drop your own (rotated) `GROQ_API_KEY`
  into a local `.env` file before running.
- **`.git/`** — this is a plain file export, not a git bundle. Commit these
  files into your existing `rohit/knowledge-base` branch yourself so history
  is preserved.

## API contract (frozen — share with Swathi and Shreyas)

```
POST /kb/search  { "query": str, "query_type": str | null }
                 -> { query, query_type, retrieved_chunks[], confidence, needs_learning, learning_item }
GET  /kb/queue                        -> { items: [...] }
GET  /kb/queue/pending                 -> { total, items: [{id, question, retrieved_context, confidence, query_type, status, drafted_entry, timestamp}] }
POST /kb/approve { "id": str }        -> { message, id, drafted_entry }
POST /kb/reject  { "id": str }        -> { message, id }
```
