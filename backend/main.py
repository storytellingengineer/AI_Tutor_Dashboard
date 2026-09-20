import io
import os
from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel, Field
from pypdf import PdfReader

from rag import PersistentRetriever, format_context

app = FastAPI(title="AI Tutor API", version="0.7.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
retriever = PersistentRetriever()


class TutorRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=12000)
    topic: str = Field(default="General", max_length=200)
    mode: Literal["Explain", "Quiz", "Interview", "Study Plan", "Revision"] = "Explain"
    level: Literal["Beginner", "Intermediate", "Advanced"] = "Beginner"
    top_k: int = Field(default=5, ge=1, le=10)


def build_instructions(request: TutorRequest, context: str) -> str:
    return ("You are a structured AI tutor. Teach clearly, accurately, and practically. "
            f"The learner's level is {request.level}. The topic is {request.topic}. "
            f"The requested mode is {request.mode}. Use headings and concise examples. "
            "Use study material when relevant; if it is insufficient, say so.\n\n"
            f"Retrieved study material:\n{context or '[No study material retrieved]'}")


@app.get("/")
def root() -> dict:
    return {"service": "ai-tutor-api", "version": "0.7.0", "status": "ok"}


@app.get("/health")
def health() -> dict:
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat(), "chunks": retriever.count()}


@app.post("/api/v1/documents")
async def upload_document(file: UploadFile = File(...)) -> dict:
    raw = await file.read()
    filename = file.filename or "uploaded-document"
    try:
        if filename.lower().endswith(".pdf") or file.content_type == "application/pdf":
            reader = PdfReader(io.BytesIO(raw))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        else:
            text = raw.decode("utf-8")
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Could not parse the uploaded document") from exc
    if not text.strip():
        raise HTTPException(status_code=400, detail="The uploaded document contains no readable text")
    document_id = str(uuid4())
    chunks = retriever.add_document(document_id, filename, text)
    return {"status": "success", "document_id": document_id, "source": filename, "chunks_created": chunks, "persistent": True}


@app.post("/api/v1/retrieve")
def retrieve(request: TutorRequest) -> dict:
    chunks = retriever.retrieve(request.prompt, request.top_k)
    return {"status": "success", "matches": [{"document_id": c.document_id, "source": c.source, "chunk_id": c.chunk_id, "text": c.text} for c in chunks]}


@app.post("/api/v1/tutor")
def tutor(request: TutorRequest) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=503, detail="OPENAI_API_KEY is not configured")
    chunks = retriever.retrieve(request.prompt, request.top_k)
    client = OpenAI(api_key=api_key)
    model = os.getenv("OPENAI_MODEL", "gpt-5-mini")
    try:
        response = client.responses.create(model=model, instructions=build_instructions(request, format_context(chunks)), input=request.prompt)
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Tutor model request failed") from exc
    return {"status": "success", "topic": request.topic, "mode": request.mode, "level": request.level, "model": model, "retrieved_chunks": len(chunks), "answer": response.output_text}


@app.post("/api/v1/tutor/preview")
def tutor_preview(request: TutorRequest) -> dict:
    return {"status": "accepted", "message": "Use /api/v1/tutor for live tutoring.", "request": request.model_dump()}
