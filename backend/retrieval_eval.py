"""Lightweight evaluation helpers for retrieval quality benchmarks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass(frozen=True)
class RetrievalCase:
    query: str
    relevant_document_ids: frozenset[str]
    top_k: int = 5


@dataclass(frozen=True)
class RetrievalMetrics:
    recall_at_k: float
    precision_at_k: float
    evaluated_cases: int


def evaluate_retrieval(
    cases: Iterable[RetrievalCase],
    retriever,
) -> RetrievalMetrics:
    cases = list(cases)
    if not cases:
        return RetrievalMetrics(0.0, 0.0, 0)

    recall_total = 0.0
    precision_total = 0.0

    for case in cases:
        if not case.query.strip():
            raise ValueError("evaluation query must not be empty")
        if not case.relevant_document_ids:
            raise ValueError("each evaluation case needs at least one relevant document")
        if case.top_k <= 0:
            raise ValueError("evaluation top_k must be greater than zero")

        results = retriever.retrieve(case.query, top_k=case.top_k)
        retrieved_ids = [result.document_id for result in results]
        relevant_retrieved = sum(
            document_id in case.relevant_document_ids
            for document_id in retrieved_ids
        )

        recall_total += relevant_retrieved / len(case.relevant_document_ids)
        precision_total += relevant_retrieved / max(len(retrieved_ids), 1)

    count = len(cases)
    return RetrievalMetrics(
        recall_at_k=recall_total / count,
        precision_at_k=precision_total / count,
        evaluated_cases=count,
    )
