"""Lightweight evaluation helpers for retrieval quality benchmarks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class RetrievalCase:
    query: str
    relevant_document_ids: frozenset[str]
    top_k: int = 5


@dataclass(frozen=True)
class RetrievalCaseMetrics:
    query: str
    recall_at_k: float
    precision_at_k: float
    f1_at_k: float


@dataclass(frozen=True)
class RetrievalMetrics:
    recall_at_k: float
    precision_at_k: float
    evaluated_cases: int

    @property
    def f1_at_k(self) -> float:
        """Return the harmonic mean of aggregate precision and recall."""
        if self.precision_at_k + self.recall_at_k == 0:
            return 0.0
        return (
            2 * self.precision_at_k * self.recall_at_k
            / (self.precision_at_k + self.recall_at_k)
        )


def _validate_case(case: RetrievalCase) -> None:
    if not case.query.strip():
        raise ValueError("evaluation query must not be empty")
    if not case.relevant_document_ids:
        raise ValueError("each evaluation case needs at least one relevant document")
    if case.top_k <= 0:
        raise ValueError("evaluation top_k must be greater than zero")


def evaluate_retrieval_detailed(
    cases: Iterable[RetrievalCase],
    retriever,
) -> tuple[RetrievalCaseMetrics, ...]:
    """Return per-query retrieval metrics for diagnosing evaluation failures."""
    results: list[RetrievalCaseMetrics] = []

    for case in cases:
        _validate_case(case)

        retrieved = retriever.retrieve(case.query, top_k=case.top_k)
        retrieved_ids = [result.document_id for result in retrieved]
        relevant_retrieved = sum(
            document_id in case.relevant_document_ids
            for document_id in retrieved_ids
        )

        recall = relevant_retrieved / len(case.relevant_document_ids)
        precision = relevant_retrieved / max(len(retrieved_ids), 1)
        f1 = (
            0.0
            if precision + recall == 0
            else 2 * precision * recall / (precision + recall)
        )

        results.append(
            RetrievalCaseMetrics(
                query=case.query,
                recall_at_k=recall,
                precision_at_k=precision,
                f1_at_k=f1,
            )
        )

    return tuple(results)


def evaluate_retrieval(
    cases: Iterable[RetrievalCase],
    retriever,
) -> RetrievalMetrics:
    cases = list(cases)
    if not cases:
        return RetrievalMetrics(0.0, 0.0, 0)

    detailed = evaluate_retrieval_detailed(cases, retriever)
    count = len(detailed)

    return RetrievalMetrics(
        recall_at_k=sum(item.recall_at_k for item in detailed) / count,
        precision_at_k=sum(item.precision_at_k for item in detailed) / count,
        evaluated_cases=count,
    )
