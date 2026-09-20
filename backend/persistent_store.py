"""SQLite-backed document chunk storage with optional semantic embeddings."""

from __future__ import annotations

import json
import os
import sqlite3
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class StoredChunk:
    document_id: str
    source: str
    chunk_id: int
    text: str
    embedding: list[float] | None = None


class PersistentStore:
    def __init__(self, db_path: str | None = None) -> None:
        self.db_path = db_path or os.getenv("AI_TUTOR_DB_PATH", "data/tutor.db")
        os.makedirs(os.path.dirname(self.db_path) or ".", exist_ok=True)
        with self._connect() as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS chunks (document_id TEXT, source TEXT, chunk_id INTEGER, text TEXT NOT NULL, embedding TEXT, PRIMARY KEY (document_id, chunk_id))")

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def add_chunks(self, chunks: Iterable[StoredChunk]) -> int:
        rows = list(chunks)
        if not rows:
            return 0
        with self._connect() as conn:
            conn.execute("DELETE FROM chunks WHERE document_id = ?", (rows[0].document_id,))
            conn.executemany("INSERT INTO chunks VALUES (?, ?, ?, ?, ?)", [(c.document_id, c.source, c.chunk_id, c.text, json.dumps(c.embedding) if c.embedding else None) for c in rows])
        return len(rows)

    def all_chunks(self) -> list[StoredChunk]:
        with self._connect() as conn:
            rows = conn.execute("SELECT document_id, source, chunk_id, text, embedding FROM chunks").fetchall()
        return [StoredChunk(a, b, c, d, json.loads(e) if e else None) for a, b, c, d, e in rows]

    def count(self) -> int:
        with self._connect() as conn:
            return int(conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0])


def cosine_similarity(left: list[float], right: list[float]) -> float:
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = sum(a * a for a in left) ** 0.5
    right_norm = sum(b * b for b in right) ** 0.5
    return dot / (left_norm * right_norm) if left_norm and right_norm else 0.0
