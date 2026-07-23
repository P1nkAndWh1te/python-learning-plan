from backend.services.bm25 import tokenize


def rerank_chunks(question: str, retrieved_chunks: list[dict], top_k: int) -> list[dict]:
    query_terms = set(tokenize(question))
    if not query_terms:
        return retrieved_chunks[:top_k]

    reranked = []
    for original_rank, item in enumerate(retrieved_chunks, start=1):
        chunk_terms = set(tokenize(item["text"]))
        overlap_count = len(query_terms & chunk_terms)
        overlap_ratio = overlap_count / len(query_terms)
        title_bonus = 0.2 if question.strip("？?") in item["text"][:120] else 0.0
        source_rank_bonus = 1 / (original_rank + 10)
        rerank_score = overlap_ratio + title_bonus + source_rank_bonus
        reranked.append(
            {
                **item,
                "rerank_score": rerank_score,
            }
        )

    reranked.sort(key=lambda item: (-item["rerank_score"], item["chunk_index"]))
    return reranked[:top_k]
