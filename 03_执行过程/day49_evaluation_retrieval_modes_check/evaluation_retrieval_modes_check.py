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

    print("Day49 evaluation retrieval modes check")
    print("Mode | Top-1 | Top-k")
    print("---|---:|---:")

    for retrieval_mode in ("vector", "bm25", "rrf"):
        response = client.post(
            "/evaluation",
            json={
                "text": text,
                "embedding_mode": KEYWORD_EMBEDDING_MODE,
                "chunk_size": 350,
                "chunk_overlap": 50,
                "top_k": 3,
                "retrieval_mode": retrieval_mode,
            },
        )
        payload = response.json()
        print(
            f"{retrieval_mode} | "
            f"{payload['top_1_hit_rate']:.1f} | "
            f"{payload['top_k_recall']:.1f}"
        )

        assert response.status_code == 200
        assert payload["retrieval_mode"] == retrieval_mode
        assert payload["chunk_count"] == 6
        assert payload["case_count"] == 10
        assert payload["top_k_recall"] >= 0.8

    unknown_response = client.post(
        "/evaluation",
        json={
            "text": text,
            "embedding_mode": KEYWORD_EMBEDDING_MODE,
            "chunk_size": 350,
            "chunk_overlap": 50,
            "top_k": 3,
            "retrieval_mode": "unknown",
        },
    )
    print(f"Unknown mode status: {unknown_response.status_code}")
    assert unknown_response.status_code == 400


if __name__ == "__main__":
    main()
