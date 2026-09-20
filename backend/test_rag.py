from rag import InMemoryRetriever, format_context


def test_retrieval_returns_relevant_chunk():
    retriever = InMemoryRetriever()
    count = retriever.add_document("doc-1", "notes.txt", "Retrieval augmented generation combines search with generation.")
    assert count == 1
    matches = retriever.retrieve("How does retrieval work?")
    assert matches
    assert "Retrieval" in format_context(matches)


def test_document_replacement_does_not_duplicate_chunks():
    retriever = InMemoryRetriever()
    retriever.add_document("doc-1", "notes.txt", "first version")
    retriever.add_document("doc-1", "notes.txt", "updated version")
    assert retriever.count() == 1
