# AI Tutor Dashboard

A production-oriented AI learning workspace built around **Next.js + FastAPI**, designed for Vercel + Render deployment.

## Current milestone: v0.8 — Document workspace

### Architecture

- **Frontend:** Next.js + React + TypeScript, deployable on Vercel
- **Backend:** FastAPI, deployable on Render
- **AI layer:** OpenAI Responses API with retrieved study context
- **RAG:** Chunking, SQLite persistence, optional Sentence Transformers embeddings, and lexical fallback
- **Storage:** SQLite by default via `AI_TUTOR_DB_PATH`

### Current capabilities

- Persistent document chunks stored in SQLite
- Optional semantic retrieval using `all-MiniLM-L6-v2`
- Lexical fallback if the embedding model is unavailable
- TXT/PDF ingestion through `/api/v1/documents`
- Retrieval through `/api/v1/retrieve`
- Tutor responses grounded in retrieved context
- Next.js frontend document upload flow

## Run locally

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Set `OPENAI_API_KEY` for live tutoring. Optional settings:

```bash
export AI_TUTOR_DB_PATH=data/tutor.db
export OPENAI_MODEL=gpt-5-mini
```

### Frontend

```bash
cd frontend
npm install
NEXT_PUBLIC_API_URL=http://localhost:8000 npm run dev
```

Open `http://localhost:3000`.

## API endpoints

- `GET /health`
- `POST /api/v1/documents`
- `POST /api/v1/retrieve`
- `POST /api/v1/tutor`
- `POST /api/v1/tutor/preview`

## Testing flow

1. Start the backend and frontend.
2. Upload a TXT or PDF document from the frontend.
3. Ask a question related to the document.
4. Confirm that the response reports retrieved chunks.
5. Restart the backend and verify persistence using the configured SQLite path.

Do not commit API keys, learner data, `.env` files, or local databases.

## Roadmap

- [x] Next.js + FastAPI foundation
- [x] Document ingestion and chunking
- [x] Persistent chunk storage
- [x] Optional embeddings-based retrieval
- [x] Next.js document upload workspace
- [ ] Document library listing and deletion
- [ ] Source citations in the UI
- [ ] PostgreSQL persistence and authentication
- [ ] Quiz scoring and progress analytics
- [ ] Automated tests and CI
