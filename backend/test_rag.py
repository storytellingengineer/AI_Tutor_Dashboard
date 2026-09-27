import pytest

from rag import PersistentRetriever, format_context
from persistent_store import PersistentStore


def build_retriever(tmp_path):
    retriever = PersistentRetriever(PersistentStore(str(tmp_path / "tutor.db")))
    retriever._encode = lambda texts: None
    return retriever


def test_retrieval_uses_keyword_fallback(tmp_path):
    retriever = build_retriever(tmp_path)
    assert retriever.add_document(
        "doc-1", "notes.txt", "Retrieval augmented generation combines search with generation."
    ) == 1

    matches = retriever.retrieve("How does retrieval work?")

    assert len(matches) == 1
    assert "retrieval" in format_context(matches).lower()
    assert matches[0].score > 0


def test_document_replacement_removes_previous_chunks(tmp_path):
    retriever = build_retriever(tmp_path)
    retriever.add_document("doc-1", "notes.txt", "first version")
    retriever.add_document("doc-1", "notes.txt", "updated version")

    assert retriever.count() == 1
    assert retriever.retrieve("updated")
    assert not retriever.retrieve("first")


def test_chunking_rejects_invalid_configuration(tmp_path):
    retriever = build_retriever(tmp_path)

    with pytest.raises(ValueError):
        retriever.add_document("doc-1", "notes.txt", "text", chunk_size=0)

    with pytest.raises(ValueError):
        retriever.add_document("doc-2", "notes.txt", "text", chunk_size=10, overlap=10)


def test_document_metadata_rejects_empty_values(tmp_path):
    retriever = build_retriever(tmp_path)

    with pytest.raises(ValueError):
        retriever.add_document("", "notes.txt", "text")

    with pytest.raises(ValueError):
        retriever.add_document("doc-1", "", "text")

    with pytest.raises(ValueError):
        retriever.add_document("doc-2", "notes.txt", "   ")


def test_retrieval_rejects_invalid_inputs(tmp_path):
    retriever = build_retriever(tmp_path)
    retriever.add_document("doc-1", "notes.txt", "Python testing and retrieval")

    with pytest.raises(ValueError):
        retriever.retrieve("   ")

    with pytest.raises(ValueError):
        retriever.retrieve("retrieval", top_k=0)

    with pytest.raises(ValueError):
        retriever.retrieve("retrieval", min_score=-0.1)


def test_retrieval_returns_empty_for_unknown_query(tmp_path):
    retriever = build_retriever(tmp_path)
    retriever.add_document("doc-1", "notes.txt", "Python testing and retrieval")

    assert retriever.retrieve("quantum physics") == []


def test_min_score_filters_weak_matches(tmp_path):
    retriever = build_retriever(tmp_path)
    retriever.add_document("doc-1", "notes.txt", "python testing retrieval")
    retriever.add_document("doc-2", "guide.txt", "python testing retrieval evaluation")

    matches = retriever.retrieve("python retrieval", min_score=0.8)

    assert matches
    assert all(match.score >= 0.8 for match in matches)


def test_top_k_limits_results(tmp_path):
    retriever = build_retriever(tmp_path)
    retriever.add_document("doc-1", "notes.txt", "retrieval search generation")
    retriever.add_document("doc-2", "guide.txt", "retrieval search evaluation")

    matches = retriever.retrieve("retrieval search", top_k=1)

    assert len(matches) == 1
    assert matches[0].score > 0
