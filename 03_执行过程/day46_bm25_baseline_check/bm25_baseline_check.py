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


def main() -> None:
    text = FAQ_PATH.read_text(encoding="utf-8")
    chunks = split_text_into_chunks(
        text,
        chunk_size=350,
        chunk_overlap=50,
    )
    query = "RAG 的基本流程是什么？"
    results = retrieve_relevant_chunks_bm25(query, chunks, top_k=3)

    print("Day46 BM25 baseline check")
    print(f"Chunks: {len(chunks)}")
    print(f"Query: {query}")
    print(f"Top chunk: {results[0]['chunk_index']}")
    print()

    for rank, item in enumerate(results, start=1):
        print(f"Rank {rank}")
        print(f"Chunk: {item['chunk_index']}")
        print(f"Score: {item['score']:.4f}")
        print(f"Preview: {item['text'][:80].replace(chr(10), ' ')}")
        print()

    assert results[0]["chunk_index"] == 6


if __name__ == "__main__":
    main()
