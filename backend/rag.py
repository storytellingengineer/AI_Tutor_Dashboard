"""Persistent chunking and optional embedding retrieval for the AI Tutor API."""

from dataclasses import dataclass
import re
from typing import Iterable

from persistent_store import PersistentStore, StoredChunk, cosine_similarity


@dataclass(frozen=True)
class DocumentChunk:
    document_id: str
    source: str
    chunk_id: int
    text: str
    embedding: list[float] | None = None


class PersistentRetriever:
    def __init__(self, store: PersistentStore | None = None) -> None:
        self.store = store or PersistentStore()
        self._embedder = None

    @staticmethod
    def _terms(text: str) -> set[str]:
        return {term for term in re.findall(r"[a-zA-Z0-9_]{2,}", text.lower())}

    def _encode(self, texts: list[str]) -> list[list[float]] | None:
        try:
            if self._embedder is None:
                from sentence_transformers import SentenceTransformer
                self._embedder = SentenceTransformer("all-MiniLM-L6-v2")
            return [vector.tolist() for vector in self._embedder.encode(texts, normalize_embeddings=True)]
        except Exception:
            return None

    def add_document(self, document_id: str, source: str, text: str, chunk_size: int = 1200, overlap: int = 200) -> int:
        if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
            raise ValueError("chunk_size must be positive and overlap must be smaller than chunk_size")
        words = text.split()
        step = chunk_size - overlap
        parts: list[str] = []
        for start in range(0, len(words), step):
            part = " ".join(words[start:start + chunk_size]).strip()
            if part:
                parts.append(part)
            if start + chunk_size >= len(words):
                break
        embeddings = self._encode(parts)
        chunks = [StoredChunk(document_id, source, i, part, embeddings[i] if embeddings else None) for i, part in enumerate(parts)]
        return self.store.add_chunks(chunks)

    def retrieve(self, query: str, top_k: int = 5) -> list[DocumentChunk]:
        stored = self.store.all_chunks()
        if not stored:
            return []
        query_embedding = self._encode([query])
        scored: list[tuple[float, StoredChunk]] = []
        query_terms = self._terms(query)
        for chunk in stored:
            if query_embedding and chunk.embedding:
                score = cosine_similarity(query_embedding[0], chunk.embedding)
            else:
                score = float(len(query_terms & self._terms(chunk.text)))
            if score > 0:
                scored.append((score, chunk))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [DocumentChunk(c.document_id, c.source, c.chunk_id, c.text, c.embedding) for _, c in scored[:top_k]]

    def count(self) -> int:
        return self.store.count()


def format_context(chunks: Iterable[DocumentChunk]) -> str:
    return "\n\n".join(f"[Source: {chunk.source} | Chunk: {chunk.chunk_id}]\n{chunk.text}" for chunk in chunks)
