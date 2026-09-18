"use client";

import { FormEvent, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [topic, setTopic] = useState("RAG");
  const [mode, setMode] = useState("Explain");
  const [level, setLevel] = useState("Beginner");
  const [status, setStatus] = useState("");

  async function submit(event: FormEvent) {
    event.preventDefault();
    setStatus("Connecting to tutor API...");
    try {
      const response = await fetch(`${API_URL}/api/v1/tutor/preview`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt, topic, mode, level }),
      });
      const data = await response.json();
      setStatus(data.message ?? "Request accepted");
    } catch {
      setStatus("API unavailable. Check NEXT_PUBLIC_API_URL and backend status.");
    }
  }

  return (
    <main style={{ maxWidth: 900, margin: "0 auto", padding: 32 }}>
      <h1>AI Tutor</h1>
      <p>Personalized learning workspace · v0.4 foundation</p>
      <form onSubmit={submit} style={{ display: "grid", gap: 16 }}>
        <input value={topic} onChange={(e) => setTopic(e.target.value)} placeholder="Topic" />
        <select value={mode} onChange={(e) => setMode(e.target.value)}>
          {['Explain', 'Quiz', 'Interview', 'Study Plan', 'Revision'].map((item) => <option key={item}>{item}</option>)}
        </select>
        <select value={level} onChange={(e) => setLevel(e.target.value)}>
          {['Beginner', 'Intermediate', 'Advanced'].map((item) => <option key={item}>{item}</option>)}
        </select>
        <textarea value={prompt} onChange={(e) => setPrompt(e.target.value)} placeholder="What do you want to learn?" rows={8} required />
        <button type="submit">Start learning</button>
      </form>
      {status && <p>{status}</p>}
    </main>
  );
}
