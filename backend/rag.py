"""Lightweight document chunking and lexical retrieval for the AI Tutor API."""

from dataclasses import dataclass
import re
from typing import Iterable


@dataclass(frozen=True)
class DocumentChunk:
    document_id: str
    source: str
    chunk_id: int
    text: str


class InMemoryRetriever:
    """Simple dependency-free retriever for the v0.6 foundation.

    This store is intentionally process-local. Replace it with a persistent
    vector store in a later version without changing the API contract.
    """

    def __init__(self) -> None:
        self._chunks: list[DocumentChunk] = []

    @staticmethod
    def _terms(text: str) -> set[str]:
        return {term for term in re.findall(r"[a-zA-Z0-9_]{2,}", text.lower())}

    def add_document(self, document_id: str, source: str, text: str, chunk_size: int = 1200, overlap: int = 200) -> int:
        if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
            raise ValueError("chunk_size must be positive and overlap must be smaller than chunk_size")

        words = text.split()
        step = chunk_size - overlap
        chunks: list[DocumentChunk] = []
        for start in range(0, len(words), step):
            part = " ".join(words[start : start + chunk_size]).strip()
            if part:
                chunks.append(DocumentChunk(document_id, source, len(chunks), part))
            if start + chunk_size >= len(words):
                break

        self._chunks = [chunk for chunk in self._chunks if chunk.document_id != document_id]
        self._chunks.extend(chunks)
        return len(chunks)

    def retrieve(self, query: str, top_k: int = 5) -> list[DocumentChunk]:
        query_terms = self._terms(query)
        if not query_terms:
            return []

        scored: list[tuple[int, DocumentChunk]] = []
        for chunk in self._chunks:
            overlap = len(query_terms & self._terms(chunk.text))
            if overlap:
                scored.append((overlap, chunk))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [chunk for _, chunk in scored[:top_k]]

    def count(self) -> int:
        return len(self._chunks)


def format_context(chunks: Iterable[DocumentChunk]) -> str:
    return "\n\n".join(
        f"[Source: {chunk.source} | Chunk: {chunk.chunk_id}]\n{chunk.text}"
        for chunk in chunks
    )
