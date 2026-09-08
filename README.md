# AI Tutor Dashboard

A focused Streamlit learning workspace powered by an LLM. It turns a topic and learning goal into explanations, quizzes, interview practice, or structured study plans.

## Features

- Learner-level aware responses: Beginner, Intermediate, Advanced
- Four learning modes: Explain, Quiz, Interview, Study Plan
- Topic-aware tutoring prompts
- Configurable OpenAI model
- Simple Streamlit interface

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

## Why this project

The project explores a practical LLM use case: turning a general-purpose model into a structured learning assistant while keeping the interface intentionally simple.
