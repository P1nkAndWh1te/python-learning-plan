from __future__ import annotations

import sys
from pathlib import Path


sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
APP_ROOT = PROJECT_ROOT / "04_成果输出" / "rag-qa-system"
FAQ_PATH = (
    PROJECT_ROOT
    / "02_资料与素材"
    / "day10_dify_knowledge"
    / "python_learning_faq.md"
)

if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from backend.services.bm25 import retrieve_relevant_chunks_bm25  # noqa: E402
from backend.services.chunking import split_text_into_chunks  # noqa: E402
from backend.services.embeddings import KEYWORD_EMBEDDING_MODE  # noqa: E402
from backend.services.retrieval import retrieve_relevant_chunks  # noqa: E402
from backend.services.rrf import retrieve_relevant_chunks_rrf  # noqa: E402


def main() -> None:
    text = FAQ_PATH.read_text(encoding="utf-8")
    chunks = split_text_into_chunks(
        text,
        chunk_size=350,
        chunk_overlap=50,
    )
    query = "RAG 的基本流程是什么？"

    vector_results = retrieve_relevant_chunks(
        query,
        chunks,
        top_k=3,
        embedding_mode=KEYWORD_EMBEDDING_MODE,
    )
    bm25_results = retrieve_relevant_chunks_bm25(query, chunks, top_k=3)
    rrf_results = retrieve_relevant_chunks_rrf(
        query,
        chunks,
        top_k=3,
        embedding_mode=KEYWORD_EMBEDDING_MODE,
    )

    print("Day47 RRF baseline check")
    print(f"Chunks: {len(chunks)}")
    print(f"Query: {query}")
    print(f"Vector top chunks: {format_indexes(vector_results)}")
    print(f"BM25 top chunks: {format_indexes(bm25_results)}")
    print(f"RRF top chunks: {format_indexes(rrf_results)}")
    print(f"RRF top chunk: {rrf_results[0]['chunk_index']}")
    print()

    for rank, item in enumerate(rrf_results, start=1):
        print(f"Rank {rank}")
        print(f"Chunk: {item['chunk_index']}")
        print(f"RRF score: {item['rrf_score']:.6f}")
        print(f"Sources: {item['sources']}")
        print(f"Preview: {item['text'][:80].replace(chr(10), ' ')}")
        print()

    assert rrf_results[0]["chunk_index"] == 6


def format_indexes(results: list[dict]) -> str:
    return ", ".join(f"Chunk {item['chunk_index']}" for item in results)


if __name__ == "__main__":
    main()
