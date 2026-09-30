import pytest

from retrieval_eval import RetrievalCase, evaluate_retrieval


class Result:
    def __init__(self, document_id):
        self.document_id = document_id


class StubRetriever:
    def __init__(self, results_by_query):
        self.results_by_query = results_by_query

    def retrieve(self, query, top_k=5):
        return [Result(document_id) for document_id in self.results_by_query[query][:top_k]]


def test_evaluate_retrieval_calculates_recall_and_precision():
    retriever = StubRetriever({
        "rag": ["doc-1", "doc-2"],
        "agents": ["doc-3"],
    })
    cases = [
        RetrievalCase("rag", frozenset({"doc-1", "doc-4"}), top_k=2),
        RetrievalCase("agents", frozenset({"doc-3"}), top_k=2),
    ]

    metrics = evaluate_retrieval(cases, retriever)

    assert metrics.evaluated_cases == 2
    assert metrics.recall_at_k == pytest.approx(0.75)
    assert metrics.precision_at_k == pytest.approx(0.75)


def test_f1_at_k_is_harmonic_mean_of_precision_and_recall():
    metrics = evaluate_retrieval(
        [RetrievalCase("query", frozenset({"doc-1"}))],
        StubRetriever({"query": ["doc-1", "doc-2"]}),
    )

    assert metrics.f1_at_k == pytest.approx(2 / 3)


def test_f1_at_k_is_zero_when_precision_and_recall_are_zero():
    metrics = evaluate_retrieval(
        [RetrievalCase("query", frozenset({"doc-1"}))],
        StubRetriever({"query": []}),
    )

    assert metrics.f1_at_k == 0.0


def test_empty_cases_return_zero_metrics():
    metrics = evaluate_retrieval([], StubRetriever({}))

    assert metrics.evaluated_cases == 0
    assert metrics.recall_at_k == 0.0
    assert metrics.precision_at_k == 0.0
    assert metrics.f1_at_k == 0.0


@pytest.mark.parametrize(
    "case",
    [
        RetrievalCase("", frozenset({"doc-1"})),
        RetrievalCase("query", frozenset()),
        RetrievalCase("query", frozenset({"doc-1"}), top_k=0),
    ],
)
def test_invalid_evaluation_cases_are_rejected(case):
    with pytest.raises(ValueError):
        evaluate_retrieval([case], StubRetriever({"query": ["doc-1"]}))


def test_top_k_is_forwarded_to_retriever():
    class TrackingRetriever:
        def __init__(self):
            self.top_k = None

        def retrieve(self, query, top_k=5):
            self.top_k = top_k
            return [Result("doc-1")]

    retriever = TrackingRetriever()
    evaluate_retrieval(
        [RetrievalCase("query", frozenset({"doc-1"}), top_k=3)],
        retriever,
    )

    assert retriever.top_k == 3
