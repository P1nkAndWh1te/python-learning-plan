from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient


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

from backend.app import app  # noqa: E402
from backend.services.embeddings import KEYWORD_EMBEDDING_MODE  # noqa: E402


def main() -> None:
    client = TestClient(app)
    text = FAQ_PATH.read_text(encoding="utf-8")

    document_response = client.post(
        "/documents",
        json={
            "text": text,
            "embedding_mode": KEYWORD_EMBEDDING_MODE,
            "chunk_size": 350,
            "chunk_overlap": 50,
        },
    )
    collection_name = document_response.json()["collection_name"]

    print("Day48 QA retrieval modes check")
    print(f"Document status: {document_response.status_code}")
    print(f"Collection name: {collection_name}")

    for retrieval_mode in ("vector", "bm25", "rrf"):
        qa_response = client.post(
            "/qa",
            json={
                "collection_name": collection_name,
                "question": "RAG 的基本流程是什么？",
                "embedding_mode": KEYWORD_EMBEDDING_MODE,
                "top_k": 3,
                "retrieval_mode": retrieval_mode,
            },
        )
        payload = qa_response.json()
        top_chunk = payload["retrieved_chunks"][0]["chunk_index"]
        print(f"Mode: {retrieval_mode} | Top chunk: {top_chunk}")

        assert qa_response.status_code == 200
        assert payload["retrieval_mode"] == retrieval_mode
        assert top_chunk == 6

    unknown_response = client.post(
        "/qa",
        json={
            "collection_name": collection_name,
            "question": "RAG 的基本流程是什么？",
            "embedding_mode": KEYWORD_EMBEDDING_MODE,
            "top_k": 3,
            "retrieval_mode": "unknown",
        },
    )

    print(f"Unknown mode status: {unknown_response.status_code}")
    assert unknown_response.status_code == 400


if __name__ == "__main__":
    main()
