"""Streamlit interface for the AI Tutor Dashboard."""

from __future__ import annotations

import os
from datetime import datetime

import streamlit as st
from openai import OpenAI


st.set_page_config(page_title="AI Tutor Dashboard", page_icon="🎓", layout="wide")

st.title("AI Tutor Dashboard")
st.caption("Learn actively: understand, practice, review, and track your learning sessions.")

if "sessions" not in st.session_state:
    st.session_state.sessions = []
if "last_response" not in st.session_state:
    st.session_state.last_response = ""

with st.sidebar:
    st.header("Learning setup")
    level = st.selectbox("Learner level", ["Beginner", "Intermediate", "Advanced"])
    topic = st.text_input("Topic", placeholder="e.g. RAG, Python, probability")
    mode = st.selectbox("Mode", ["Explain", "Quiz", "Interview", "Study Plan", "Revision"])
    model = st.text_input("OpenAI model", value=os.getenv("OPENAI_MODEL", "gpt-5-mini"))
    st.divider()
    st.metric("Sessions", len(st.session_state.sessions))
    if st.button("Clear learning history"):
        st.session_state.sessions = []
        st.session_state.last_response = ""
        st.rerun()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.info("Set OPENAI_API_KEY in your environment to enable live tutoring.")
    st.code("export OPENAI_API_KEY=your_key_here")

prompt = st.text_area(
    "Your question or learning goal",
    height=160,
    placeholder="Explain attention mechanisms with an intuitive example...",
)

col1, col2 = st.columns([1, 1])
with col1:
    generate = st.button("Generate learning material", type="primary", use_container_width=True)
with col2:
    follow_up = st.button("Create practice follow-up", use_container_width=True)

if generate or follow_up:
    if not prompt.strip() and not st.session_state.last_response:
        st.warning("Enter a question or learning goal first.")
        st.stop()
    if not api_key:
        st.error("OPENAI_API_KEY is required for live generation.")
        st.stop()

    client = OpenAI(api_key=api_key)
    requested_mode = "Practice Follow-up" if follow_up else mode
    source_context = st.session_state.last_response if follow_up else ""
    system_prompt = f"""You are an expert AI tutor. Teach at the {level} level.
Topic: {topic or 'general learning'}.
Mode: {requested_mode}.

Rules:
- Use clear headings and concise explanations.
- Build intuition before technical detail.
- Include a practical example whenever useful.
- For quizzes, show questions first and put answers in a clearly labelled section.
- For interviews, provide questions, hints, and model answers.
- For study plans, provide milestones and practice tasks.
- For revision, focus on key concepts, common mistakes, and active recall.
- For practice follow-ups, create exercises based on the previous material.
- Never pretend that the learner has mastered a concept; suggest how to verify understanding."""

    user_input = prompt
    if source_context:
        user_input = f"Create practice tasks based on this previous tutor response:\n\n{source_context}"
    with st.spinner("Generating learning material..."):
        response = client.responses.create(
            model=model,
            instructions=system_prompt,
            input=user_input,
        )

    output = response.output_text.strip()
    st.session_state.last_response = output
    st.session_state.sessions.append(
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "topic": topic or "General learning",
            "mode": requested_mode,
            "level": level,
            "prompt": prompt or "Practice follow-up",
            "response": output,
        }
    )

if st.session_state.last_response:
    st.subheader("Tutor response")
    st.markdown(st.session_state.last_response)
    st.download_button(
        "Download response",
        data=st.session_state.last_response,
        file_name="tutor_response.md",
        mime="text/markdown",
    )

if st.session_state.sessions:
    st.divider()
    st.subheader("Learning history")
    for index, session in enumerate(reversed(st.session_state.sessions)):
        title = f"{session['topic']} · {session['mode']} · {session['timestamp']}"
        with st.expander(title, expanded=index == 0):
            st.caption(f"Level: {session['level']}")
            st.markdown(f"**Prompt:** {session['prompt']}")
            st.markdown(session["response"])

st.divider()
st.markdown(
    "**Suggested workflow:** Learn a concept → generate a practice follow-up → attempt it without help → revise your mistakes."
)
