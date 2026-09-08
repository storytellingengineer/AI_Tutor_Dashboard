import os

import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="AI Tutor Dashboard", page_icon="🎓", layout="wide")

st.title("AI Tutor Dashboard")
st.caption("A focused learning workspace for asking questions, generating explanations, and creating practice tasks.")

with st.sidebar:
    st.header("Learning setup")
    level = st.selectbox("Learner level", ["Beginner", "Intermediate", "Advanced"])
    topic = st.text_input("Topic", placeholder="e.g. RAG, Python, probability")
    mode = st.selectbox("Mode", ["Explain", "Quiz", "Interview", "Study Plan"])
    model = st.text_input("OpenAI model", value=os.getenv("OPENAI_MODEL", "gpt-5-mini"))

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.info("Set OPENAI_API_KEY in your environment to enable live tutoring.")
    st.code("export OPENAI_API_KEY=your_key_here")

prompt = st.text_area("Your question or learning goal", height=180, placeholder="Explain attention mechanisms with an intuitive example...")

if st.button("Generate", type="primary"):
    if not prompt.strip():
        st.warning("Enter a question or learning goal first.")
        st.stop()
    if not api_key:
        st.error("OPENAI_API_KEY is required for live generation.")
        st.stop()

    client = OpenAI(api_key=api_key)
    system_prompt = f"""You are an expert AI tutor. Teach at the {level} level. Topic: {topic or 'general learning'}. Mode: {mode}.\n\nBe clear, practical, and concise. For explanations, build intuition before technical detail. For quizzes, provide questions first and hide answers under a clearly labelled answer section. For interviews, ask realistic questions and give model answers after the questions. For study plans, provide a concrete sequence with practice tasks."""

    with st.spinner("Generating learning material..."):
        response = client.responses.create(
            model=model,
            instructions=system_prompt,
            input=prompt,
        )

    st.subheader("Tutor response")
    st.markdown(response.output_text)

st.divider()
st.markdown("### Suggested workflow")
st.markdown("1. Choose your level and topic.  2. Pick a learning mode.  3. Ask a focused question.  4. Use the generated material as a starting point for active practice.")
