from __future__ import annotations

import os
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
    print(f"Document status: {document_response.status_code}")
    assert document_response.status_code == 200

    collection_name = document_response.json()["collection_name"]
    answer_request = {
        "collection_name": collection_name,
        "question": "RAG 的基本流程是什么？",
        "embedding_mode": KEYWORD_EMBEDDING_MODE,
        "top_k": 3,
        "retrieval_mode": "rrf",
    }

    original_key = os.environ.pop("DEEPSEEK_API_KEY", None)
    try:
        missing_key_response = client.post("/answer", json=answer_request)
    finally:
        if original_key:
            os.environ["DEEPSEEK_API_KEY"] = original_key

    print(f"Answer without key status: {missing_key_response.status_code}")
    assert missing_key_response.status_code == 503

    unknown_mode_response = client.post(
        "/answer",
        json={**answer_request, "retrieval_mode": "unknown"},
    )
    print(f"Unknown mode status: {unknown_mode_response.status_code}")
    assert unknown_mode_response.status_code == 400

    if original_key and os.environ.get("RUN_REAL_ANSWER_CHECK") == "1":
        real_response = client.post("/answer", json=answer_request)
        print(f"Real answer status: {real_response.status_code}")
        assert real_response.status_code == 200
        payload = real_response.json()
        print(f"Sources: {payload['sources']}")
        print(f"Answer preview: {payload['answer'][:120]}")
    else:
        print("Real answer call skipped.")


if __name__ == "__main__":
    main()
