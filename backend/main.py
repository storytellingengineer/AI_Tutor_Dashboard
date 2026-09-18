from datetime import datetime, timezone
from typing import Literal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="AI Tutor API", version="0.4.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TutorRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=12000)
    topic: str = Field(default="General", max_length=200)
    mode: Literal["Explain", "Quiz", "Interview", "Study Plan", "Revision"] = "Explain"
    level: Literal["Beginner", "Intermediate", "Advanced"] = "Beginner"


@app.get("/")
def root() -> dict:
    return {"service": "ai-tutor-api", "version": "0.4.0", "status": "ok"}


@app.get("/health")
def health() -> dict:
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}


@app.post("/api/v1/tutor/preview")
def tutor_preview(request: TutorRequest) -> dict:
    """Temporary contract endpoint; LLM orchestration will be added next."""
    return {
        "status": "accepted",
        "message": "Tutor orchestration contract is ready for the next implementation phase.",
        "request": request.model_dump(),
    }
