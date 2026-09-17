"""Streamlit AI Tutor Dashboard with persistent profiles and notes context."""

from __future__ import annotations

import os
from datetime import datetime

import streamlit as st
from openai import OpenAI

from learning_store import clear_sessions, get_profile, init_db, list_sessions, save_profile, save_session


st.set_page_config(page_title="AI Tutor Dashboard", page_icon="🎓", layout="wide")
init_db()
profile = get_profile()

st.title("AI Tutor Dashboard")
st.caption("Learn actively: understand, practice, review, and track your learning journey.")

with st.sidebar:
    st.header("Learner profile")
    learner_name = st.text_input("Name", value=profile["name"])
    learner_goal = st.text_area("Learning goal", value=profile["goal"], height=80)
    level = st.selectbox("Learner level", ["Beginner", "Intermediate", "Advanced"], index=["Beginner", "Intermediate", "Advanced"].index(profile["level"]) if profile["level"] in ["Beginner", "Intermediate", "Advanced"] else 0)
    if st.button("Save profile", use_container_width=True):
        save_profile(learner_name, learner_goal, level)
        st.success("Profile saved.")

    st.divider()
    topic = st.text_input("Topic", placeholder="e.g. RAG, Python, probability")
    mode = st.selectbox("Mode", ["Explain", "Quiz", "Interview", "Study Plan", "Revision"])
    model = st.text_input("OpenAI model", value=os.getenv("OPENAI_MODEL", "gpt-5-mini"))
    st.metric("Saved sessions", len(list_sessions()))
    if st.button("Clear saved history", use_container_width=True):
        clear_sessions()
        st.rerun()

st.subheader("Study material")
uploaded_file = st.file_uploader("Upload notes (TXT or PDF)", type=["txt", "pdf"])
notes_context = ""
if uploaded_file:
    if uploaded_file.name.lower().endswith(".txt"):
        notes_context = uploaded_file.getvalue().decode("utf-8", errors="ignore")
    else:
        try:
            from pypdf import PdfReader

            reader = PdfReader(uploaded_file)
            notes_context = "\n\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as exc:
            st.error(f"Could not read PDF: {exc}")
    if notes_context:
        st.success(f"Loaded {len(notes_context):,} characters from {uploaded_file.name}.")
        with st.expander("Preview extracted notes"):
            st.text(notes_context[:4000])

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.info("Set OPENAI_API_KEY in your environment to enable live tutoring.")
    st.code("export OPENAI_API_KEY=your_key_here")

prompt = st.text_area("Your question or learning goal", height=160, placeholder="Explain attention mechanisms with an intuitive example...")
col1, col2 = st.columns(2)
with col1:
    generate = st.button("Generate learning material", type="primary", use_container_width=True)
with col2:
    follow_up = st.button("Create practice follow-up", use_container_width=True)

sessions = list_sessions()
last_response = sessions[0]["response"] if sessions else ""

if generate or follow_up:
    if not prompt.strip() and not last_response:
        st.warning("Enter a question or learning goal first.")
        st.stop()
    if not api_key:
        st.error("OPENAI_API_KEY is required for live generation.")
        st.stop()

    requested_mode = "Practice Follow-up" if follow_up else mode
    source_context = last_response if follow_up else ""
    if notes_context:
        source_context += f"\n\nReference notes:\n{notes_context[:12000]}"
    user_input = prompt or "Create practice tasks from the latest learning material."
    if source_context:
        user_input = f"{user_input}\n\nUse this context when relevant:\n{source_context}"

    system_prompt = f"""You are an expert AI tutor helping {learner_name or 'the learner'} at the {level} level.
Topic: {topic or 'general learning'}.
Learning goal: {learner_goal or 'build durable understanding'}.
Mode: {requested_mode}.

Rules:
- Use clear headings and concise explanations.
- Build intuition before technical detail.
- Use uploaded notes as reference, but state when the notes do not contain an answer.
- Include practical examples and active-recall questions where useful.
- For quizzes, show questions first and label answers separately.
- For interviews, provide hints and model answers.
- Never claim mastery without evidence."""

    with st.spinner("Generating learning material..."):
        response = OpenAI(api_key=api_key).responses.create(model=model, instructions=system_prompt, input=user_input)
    output = response.output_text.strip()
    record = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"), "topic": topic or "General learning", "mode": requested_mode, "level": level, "prompt": prompt or "Practice follow-up", "response": output}
    save_session(record)
    st.rerun()

sessions = list_sessions()
if sessions:
    st.subheader("Latest tutor response")
    st.markdown(sessions[0]["response"])
    st.download_button("Download response", data=sessions[0]["response"], file_name="tutor_response.md", mime="text/markdown")
    st.divider()
    st.subheader("Learning history")
    for index, session in enumerate(sessions):
        title = f"{session['topic']} · {session['mode']} · {session['timestamp']}"
        with st.expander(title, expanded=index == 0):
            st.caption(f"Level: {session['level']}")
            st.markdown(f"**Prompt:** {session['prompt']}")
            st.markdown(session["response"])

st.divider()
st.markdown("**Suggested workflow:** Set your goal → upload notes → learn → practice → revise mistakes.")
