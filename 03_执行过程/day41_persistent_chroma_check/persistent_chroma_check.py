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

from app import (  # noqa: E402
    BGE_EMBEDDING_MODE,
    DEFAULT_CHUNK_OVERLAP,
    DEFAULT_CHUNK_SIZE,
    EVALUATION_CASES,
    KEYWORD_EMBEDDING_MODE,
    TOP_K,
    calculate_hit_rate,
    calculate_top_k_hit_rate,
    evaluate_retrieval,
)
from backend.services.chunking import split_text_into_chunks  # noqa: E402
from backend.services.retrieval import (  # noqa: E402
    CHROMA_DB_PATH,
    retrieve_relevant_chunks,
)


def main() -> None:
    text = FAQ_PATH.read_text(encoding="utf-8")
    chunks = split_text_into_chunks(
        text,
        chunk_size=DEFAULT_CHUNK_SIZE,
        chunk_overlap=DEFAULT_CHUNK_OVERLAP,
    )

    query = "RAG 的基本流程是什么？"
    retrieved_chunks = retrieve_relevant_chunks(
        query,
        chunks,
        top_k=TOP_K,
        embedding_mode=KEYWORD_EMBEDDING_MODE,
    )

    if not retrieved_chunks:
        raise AssertionError("Expected at least one retrieved chunk.")

    print("Day41 persistent Chroma check")
    print(f"Storage path: {CHROMA_DB_PATH}")
    print(f"Storage exists: {CHROMA_DB_PATH.exists()}")
    print(f"Chunks: {len(chunks)}")
    print(f"Query: {query}")
    print(f"Top chunk: {retrieved_chunks[0]['chunk_index']}")
    print()
    print("| Embedding mode | Top-1 hit | Top-k recall |")
    print("|---|---:|---:|")

    for embedding_mode in (
        KEYWORD_EMBEDDING_MODE,
        BGE_EMBEDDING_MODE,
    ):
        rows = evaluate_retrieval(
            EVALUATION_CASES,
            chunks,
            top_k=TOP_K,
            embedding_mode=embedding_mode,
        )
        hit_rate = calculate_hit_rate(rows)
        top_k_hit_rate = calculate_top_k_hit_rate(rows)
        print(
            f"| {embedding_mode} | {hit_rate:.0%} | {top_k_hit_rate:.0%} |"
        )

    assert CHROMA_DB_PATH.exists()
    assert retrieved_chunks[0]["chunk_index"] == 6


if __name__ == "__main__":
    main()
