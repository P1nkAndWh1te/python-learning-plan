from __future__ import annotations

import sys
from pathlib import Path


sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
APP_ROOT = PROJECT_ROOT / "04_成果输出" / "rag-qa-system"
sys.path.insert(0, str(APP_ROOT))

from backend.services.embeddings import (  # noqa: E402
    BGE_EMBEDDING_MODE,
    KEYWORD_EMBEDDING_MODE,
    embed_for_mode,
    get_matched_concepts,
)


def main() -> None:
    sample = "RAG 的基本流程是什么？"
    keyword_embedding = embed_for_mode(sample, KEYWORD_EMBEDDING_MODE)
    bge_embedding = embed_for_mode(sample, BGE_EMBEDDING_MODE)

    print("Day39 embedding service check")
    print(f"Sample: {sample}")
    print(f"Matched concepts: {', '.join(get_matched_concepts(sample))}")
    print(f"Keyword embedding dimension: {len(keyword_embedding)}")
    print(f"BGE embedding dimension: {len(bge_embedding)}")

    if len(keyword_embedding) != 12:
        raise AssertionError(f"Expected keyword embedding dimension 12, got {len(keyword_embedding)}")

    if len(bge_embedding) != 512:
        raise AssertionError(f"Expected BGE embedding dimension 512, got {len(bge_embedding)}")


if __name__ == "__main__":
    main()

