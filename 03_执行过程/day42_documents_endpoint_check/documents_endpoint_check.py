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

    response = client.post(
        "/documents",
        json={
            "text": text,
            "embedding_mode": KEYWORD_EMBEDDING_MODE,
            "chunk_size": 350,
            "chunk_overlap": 50,
        },
    )
    payload = response.json()

    print("Day42 documents endpoint check")
    print(f"Status code: {response.status_code}")
    print(f"Document ID: {payload['document_id']}")
    print(f"Collection name: {payload['collection_name']}")
    print(f"Chunk count: {payload['chunk_count']}")
    print(f"Stored chunk count: {payload['stored_chunk_count']}")

    assert response.status_code == 200
    assert payload["embedding_mode"] == KEYWORD_EMBEDDING_MODE
    assert payload["chunk_count"] == 6
    assert payload["stored_chunk_count"] == 6

    bad_response = client.post(
        "/documents",
        json={
            "text": text,
            "embedding_mode": "unknown",
        },
    )

    print(f"Bad request status: {bad_response.status_code}")
    assert bad_response.status_code == 400


if __name__ == "__main__":
    main()
