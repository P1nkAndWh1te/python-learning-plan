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

    upload_response = client.post(
        "/documents/upload",
        data={
            "embedding_mode": KEYWORD_EMBEDDING_MODE,
            "chunk_size": "350",
            "chunk_overlap": "50",
        },
        files={
            "file": (
                "python_learning_faq.md",
                text.encode("utf-8"),
                "text/markdown",
            )
        },
    )
    upload_payload = upload_response.json()
    print(f"Upload md status: {upload_response.status_code}")
    print(f"Chunk count: {upload_payload['chunk_count']}")

    assert upload_response.status_code == 200
    assert upload_payload["chunk_count"] == 6
    assert upload_payload["stored_chunk_count"] == 6

    rejected_response = client.post(
        "/documents/upload",
        data={
            "embedding_mode": KEYWORD_EMBEDDING_MODE,
            "chunk_size": "350",
            "chunk_overlap": "50",
        },
        files={
            "file": (
                "document.pdf",
                b"%PDF-1.4 fake",
                "application/pdf",
            )
        },
    )
    print(f"Upload pdf status: {rejected_response.status_code}")
    assert rejected_response.status_code == 400


if __name__ == "__main__":
    main()
