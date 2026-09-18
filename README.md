# AI Tutor Dashboard

A production-oriented AI learning workspace. The project is transitioning from the original Streamlit prototype to a deployable **Next.js + FastAPI** architecture.

## Current milestone: v0.4 — Deployment-ready foundation

### Architecture

- **Frontend:** Next.js + React + TypeScript, deployed on Vercel
- **Backend:** FastAPI, deployed on Render
- **AI layer:** Tutor orchestration, RAG, quizzes, and progress tracking (incremental roadmap)
- **Persistence:** Existing Streamlit/SQLite prototype retained while the production persistence layer is introduced

### Added in v0.4 foundation

- FastAPI service with `/health` endpoint
- Versioned tutor preview contract at `/api/v1/tutor/preview`
- Next.js frontend scaffold with topic, mode, level, and prompt controls
- Frontend-to-backend API integration through `NEXT_PUBLIC_API_URL`
- Render deployment blueprint in `render.yaml`

## Run locally

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
NEXT_PUBLIC_API_URL=http://localhost:8000 npm run dev
```

Open the frontend at `http://localhost:3000`.

## Legacy prototype

The original Streamlit prototype remains in the repository as a reference implementation:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Do not commit API keys, learner data, `.env` files, or local SQLite databases.

## Roadmap

- [x] Next.js frontend foundation
- [x] FastAPI backend foundation
- [x] Vercel/Render-oriented project structure
- [ ] Move tutoring orchestration from Streamlit into FastAPI
- [ ] Add document ingestion and chunked retrieval
- [ ] Add embeddings-based RAG and reranking
- [ ] Add PostgreSQL persistence and authentication
- [ ] Add quiz scoring and progress analytics
- [ ] Add automated tests and CI
