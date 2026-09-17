# AI Tutor Dashboard

A Streamlit learning workspace powered by an LLM. It turns a topic and learning goal into explanations, quizzes, interview practice, revision notes, study plans, and practice follow-ups.

## Current milestone: v0.2 — Learning Workspace

### Features

- Learner-level aware responses: Beginner, Intermediate, Advanced
- Six learning modes: Explain, Quiz, Interview, Study Plan, Revision, Practice Follow-up
- Topic-aware tutoring prompts
- Configurable OpenAI model through `OPENAI_MODEL`
- Session-based learning history
- Downloadable Markdown tutor responses
- Practice follow-ups based on the latest generated response
- Clear learning-history control
- Simple, responsive Streamlit interface

> Learning history is stored in Streamlit session state and is cleared when the session restarts or the history is manually cleared. Persistent learner profiles are planned for a future milestone.

## Run locally

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=your_key_here
streamlit run app.py
```

On Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="your_key_here"
streamlit run app.py
```

You can override the default model with `OPENAI_MODEL`.

## Project structure

```text
.
├── app.py
├── requirements.txt
└── README.md
```

## Suggested learning workflow

1. Choose your level and topic.
2. Generate an explanation or study plan.
3. Create a practice follow-up.
4. Attempt the exercises without assistance.
5. Review mistakes and repeat with the Revision mode.

## Roadmap

- [x] Core tutoring modes
- [x] Session learning history
- [x] Practice follow-ups
- [x] Markdown export
- [ ] Persistent learner profiles
- [ ] PDF/notes ingestion and RAG
- [ ] Quiz answer submission and scoring
- [ ] Progress analytics
- [ ] Authentication and multi-user deployment

## Why this project

The project explores a practical LLM use case: turning a general-purpose model into a structured learning assistant while encouraging active recall and deliberate practice.
