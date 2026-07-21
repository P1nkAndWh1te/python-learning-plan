from backend.services.bm25 import retrieve_relevant_chunks_bm25
from backend.services.embeddings import KEYWORD_EMBEDDING_MODE
from backend.services.retrieval import retrieve_relevant_chunks


def reciprocal_rank_fusion(
    ranked_lists: list[list[dict]],
    top_k: int,
    rrf_k: int = 60,
) -> list[dict]:
    fused_by_chunk = {}

    for source_index, ranked_items in enumerate(ranked_lists):
        source_name = f"source_{source_index + 1}"
        for rank, item in enumerate(ranked_items, start=1):
            chunk_index = item["chunk_index"]
            if chunk_index not in fused_by_chunk:
                fused_by_chunk[chunk_index] = {
                    "text": item["text"],
                    "chunk_index": chunk_index,
                    "rrf_score": 0.0,
                    "sources": [],
                }

            fused_by_chunk[chunk_index]["rrf_score"] += 1 / (rrf_k + rank)
            fused_by_chunk[chunk_index]["sources"].append(
                {
                    "source": source_name,
                    "rank": rank,
                }
            )

    fused_results = list(fused_by_chunk.values())
    fused_results.sort(key=lambda item: (-item["rrf_score"], item["chunk_index"]))
    return fused_results[:top_k]


def retrieve_relevant_chunks_rrf(
    question: str,
    chunks: list[str],
    top_k: int,
    embedding_mode: str = KEYWORD_EMBEDDING_MODE,
    candidate_k: int | None = None,
    rrf_k: int = 60,
) -> list[dict]:
    candidate_count = candidate_k or top_k
    vector_results = retrieve_relevant_chunks(
        question,
        chunks,
        top_k=candidate_count,
        embedding_mode=embedding_mode,
    )
    bm25_results = retrieve_relevant_chunks_bm25(
        question,
        chunks,
        top_k=candidate_count,
    )

    return reciprocal_rank_fusion(
        [vector_results, bm25_results],
        top_k=top_k,
        rrf_k=rrf_k,
    )
