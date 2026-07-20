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
    document_payload = document_response.json()
    collection_name = document_payload["collection_name"]

    qa_response = client.post(
        "/qa",
        json={
            "collection_name": collection_name,
            "question": "RAG 的基本流程是什么？",
            "embedding_mode": KEYWORD_EMBEDDING_MODE,
            "top_k": 3,
        },
    )
    qa_payload = qa_response.json()
    retrieved_chunks = qa_payload["retrieved_chunks"]

    print("Day43 QA endpoint check")
    print(f"Document status: {document_response.status_code}")
    print(f"Collection name: {collection_name}")
    print(f"QA status: {qa_response.status_code}")
    print(f"Top chunk: {retrieved_chunks[0]['chunk_index']}")
    print(f"Retrieved chunks: {len(retrieved_chunks)}")
    print(f"Context has sources: {'[Chunk 6]' in qa_payload['context']}")

    assert document_response.status_code == 200
    assert qa_response.status_code == 200
    assert retrieved_chunks[0]["chunk_index"] == 6
    assert len(retrieved_chunks) == 3
    assert "[Chunk 6]" in qa_payload["context"]

    missing_response = client.post(
        "/qa",
        json={
            "collection_name": "missing_collection",
            "question": "RAG 的基本流程是什么？",
            "embedding_mode": KEYWORD_EMBEDDING_MODE,
            "top_k": 3,
        },
    )

    print(f"Missing collection status: {missing_response.status_code}")
    assert missing_response.status_code == 404


if __name__ == "__main__":
    main()
