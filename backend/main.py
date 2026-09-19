import os
from datetime import datetime, timezone
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel, Field

app = FastAPI(title="AI Tutor API", version="0.5.0")

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


def build_instructions(request: TutorRequest) -> str:
    return (
        "You are a structured AI tutor. Teach clearly, accurately, and practically. "
        f"The learner's level is {request.level}. The topic is {request.topic}. "
        f"The requested mode is {request.mode}. Adapt depth and examples to the level. "
        "Use headings and concise examples. Encourage active recall where appropriate."
    )


@app.get("/")
def root() -> dict:
    return {"service": "ai-tutor-api", "version": "0.5.0", "status": "ok"}


@app.get("/health")
def health() -> dict:
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}


@app.post("/api/v1/tutor")
def tutor(request: TutorRequest) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=503, detail="OPENAI_API_KEY is not configured")

    client = OpenAI(api_key=api_key)
    model = os.getenv("OPENAI_MODEL", "gpt-5-mini")

    try:
        response = client.responses.create(
            model=model,
            instructions=build_instructions(request),
            input=request.prompt,
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Tutor model request failed") from exc

    return {
        "status": "success",
        "topic": request.topic,
        "mode": request.mode,
        "level": request.level,
        "model": model,
        "answer": response.output_text,
    }


@app.post("/api/v1/tutor/preview")
def tutor_preview(request: TutorRequest) -> dict:
    return {
        "status": "accepted",
        "message": "Use /api/v1/tutor for live tutoring.",
        "request": request.model_dump(),
    }
