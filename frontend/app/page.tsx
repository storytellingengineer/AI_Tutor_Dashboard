"use client";

import { FormEvent, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [topic, setTopic] = useState("RAG");
  const [mode, setMode] = useState("Explain");
  const [level, setLevel] = useState("Beginner");
  const [answer, setAnswer] = useState("");
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit(event: FormEvent) {
    event.preventDefault();
    setLoading(true);
    setAnswer("");
    setStatus("Generating your learning response...");

    try {
      const response = await fetch(`${API_URL}/api/v1/tutor`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt, topic, mode, level }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail ?? "Tutor request failed");
      setAnswer(data.answer ?? "No answer returned.");
      setStatus("Response generated");
    } catch (error) {
      setStatus(error instanceof Error ? error.message : "API unavailable");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main style={{ maxWidth: 900, margin: "0 auto", padding: 32 }}>
      <h1>AI Tutor</h1>
      <p>Personalized learning workspace · v0.5</p>
      <form onSubmit={submit} style={{ display: "grid", gap: 16 }}>
        <input value={topic} onChange={(e) => setTopic(e.target.value)} placeholder="Topic" />
        <select value={mode} onChange={(e) => setMode(e.target.value)}>
          {['Explain', 'Quiz', 'Interview', 'Study Plan', 'Revision'].map((item) => <option key={item}>{item}</option>)}
        </select>
        <select value={level} onChange={(e) => setLevel(e.target.value)}>
          {['Beginner', 'Intermediate', 'Advanced'].map((item) => <option key={item}>{item}</option>)}
        </select>
        <textarea value={prompt} onChange={(e) => setPrompt(e.target.value)} placeholder="What do you want to learn?" rows={8} required />
        <button type="submit" disabled={loading}>{loading ? "Generating..." : "Start learning"}</button>
      </form>
      {status && <p>{status}</p>}
      {answer && <article style={{ marginTop: 32, whiteSpace: "pre-wrap" }}><h2>Your tutor response</h2><p>{answer}</p></article>}
    </main>
  );
}
