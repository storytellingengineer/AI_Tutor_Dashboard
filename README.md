# 🧠 AI-Powered Student Dashboard 📚

A smart dashboard built with **Streamlit**, **Google Classroom API**, and **OpenAI GPT**, designed to help students manage their academic workload effectively and get instant answers to study-related queries using an LLM-powered chatbot.

---

## Features

- 📅 **Assignment Tracker**: Pulls live data from Google Classroom – shows pending, submitted, and upcoming assignments.
- 🎓 **Class & Seminar Info**: Displays classes you should attend and upcoming academic events.
- 💬 **LLM Chatbot Assistant**:
  - Answers questions like “What’s due today?” or “Explain Decision Trees.”
  - Handles ML, NLP, coding topics, project queries, and more.
- 🔎 **Vector Search**: Uses ChromaDB to fetch study notes and resources for deeper context.

---

## Tech Stack

- [Streamlit](https://streamlit.io/) – UI framework
- [OpenAI GPT (via LangChain)](https://openai.com/) – for natural language Q&A
- [Google Classroom API](https://developers.google.com/classroom) – for real-time academic info
- [Chromadb](https://www.trychroma.com/) – for vector-based semantic search
- Python 3.10+

---

## Installation

### 1. Clone the Repository

```
git clone https://github.com/your-username/student-dashboard-ai.git
cd student-dashboard-ai
```

### 2. Set Up Environment

```
python -m venv venv
venv\Scripts\activate         # Windows
# or
source venv/bin/activate     # macOS/Linux

pip install -r requirements.txt
```

### 3. Set Up .env File

Create a .env file in the root folder:

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
GOOGLE_CLIENT_SECRET_FILE=credentials.json
```

### 4. Add Your Google Credentials
- Go to Google Cloud Console
- Enable **Google Classroom API**
- Create **OAuth 2.0 Client ID**
- Download the `credentials.json` and place it in the project root

---

## Run the App

```streamlit run app.py```

## Project Structure

```
├── app.py                 # Streamlit app
├── chatbot.py             # LangChain-based GPT chatbot
├── classroom_api.py       # Google Classroom API integration
├── prompt.py              # Custom prompt templates
├── credentials.json       # Google OAuth credentials
├── .env                   # API keys and secrets
├── requirements.txt       # Python dependencies
├── README.md              # This file
```

## Example Queries for Chatbot
- "What assignments are pending for me this week?"
- "Explain PCA with an example."
- "What is the latest Leetcode problem I should try?"
- "What are the current ML/NLP topics being studied?"

## 👨‍🔬 Author
Made with ❤️ by [Aayush Saxena](https://www.linkedin.com/in/storytellingengineer/)
