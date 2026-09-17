# AI Tutor Dashboard

A Streamlit learning workspace powered by an LLM. It supports explanations, quizzes, interviews, revision, study plans, persistent learner profiles, and notes-assisted tutoring.

## Current milestone: v0.3 — Persistent Learning Workspace

### Features

- Learner profile with name, level, and learning goal
- Persistent SQLite storage for profile and learning sessions
- Six learning modes: Explain, Quiz, Interview, Study Plan, Revision, Practice Follow-up
- TXT and PDF notes upload using `pypdf`
- Notes context included in tutor prompts
- Configurable OpenAI model through `OPENAI_MODEL`
- Downloadable Markdown tutor responses
- Saved learning history across app restarts
- Clear saved-history control

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

The SQLite database (`ai_tutor.db`) is created automatically beside `app.py` and should be kept local. Do not commit learner data or API keys.

## Project structure

```text
.
├── app.py
├── learning_store.py
├── requirements.txt
└── README.md
```

## Suggested workflow

1. Save your learner profile and learning goal.
2. Upload TXT or PDF notes.
3. Ask for an explanation, quiz, interview, or revision session.
4. Generate practice follow-ups.
5. Review saved sessions and repeat.

## Roadmap

- [x] Core tutoring modes
- [x] Persistent learner profiles
- [x] Persistent learning history
- [x] TXT/PDF notes ingestion
- [x] Notes-assisted tutoring context
- [x] Markdown export
- [ ] Chunked retrieval and embeddings-based RAG
- [ ] Quiz answer submission and scoring
- [ ] Progress analytics
- [ ] Authentication and multi-user deployment

## Why this project

The project explores a practical LLM use case: turning a general-purpose model into a structured learning assistant while encouraging active recall and deliberate practice.
