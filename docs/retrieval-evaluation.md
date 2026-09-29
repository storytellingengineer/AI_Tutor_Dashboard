# RAG Retrieval Evaluation

This guide defines the minimum evaluation loop for the AI Tutor retrieval layer.

## Metrics

Track these separately:

- **Recall@K:** whether relevant chunks appear in the top K results.
- **Precision@K:** how many returned chunks are relevant.
- **Score distribution:** whether relevance scores separate strong and weak matches.
- **Empty-result rate:** how often a valid query returns no chunks.
- **Latency:** retrieval time with and without semantic embeddings.

## Test scenarios

1. Exact keyword query
2. Paraphrased semantic query
3. Query with no matching material
4. Multiple documents with overlapping terms
5. top_k=1 and larger values
6. Increasing min_score thresholds
7. Empty or invalid inputs
8. Restarting the API and confirming persisted chunks remain available

## Baseline regression checks

The backend suite should always cover:

- document replacement
- chunking validation
- keyword fallback
- unknown queries
- top_k
- min_score
- retrieval score exposure

## Manual acceptance test

After a successful CI run:

1. Upload a study document.
2. Retrieve a question that is clearly answered by the document.
3. Confirm the best matching chunk has the highest score.
4. Increase min_score until weaker matches disappear.
5. Try an unrelated question and confirm no irrelevant chunk is returned.
6. Restart the backend and repeat the retrieval test.

The next retrieval milestone should use a small labeled evaluation set so changes to chunking, embeddings, and ranking can be measured rather than judged only by manual inspection.
