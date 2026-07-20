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
        "/evaluation",
        json={
            "text": text,
            "embedding_mode": KEYWORD_EMBEDDING_MODE,
            "chunk_size": 350,
            "chunk_overlap": 50,
            "top_k": 3,
        },
    )
    payload = response.json()

    print("Day45 evaluation endpoint check")
    print(f"Status code: {response.status_code}")
    print(f"Chunk count: {payload['chunk_count']}")
    print(f"Case count: {payload['case_count']}")
    print(f"Top-1 hit rate: {payload['top_1_hit_rate']}")
    print(f"Top-k recall: {payload['top_k_recall']}")
    print(f"Last question hit: {payload['rows'][-1]['hit']}")

    assert response.status_code == 200
    assert payload["chunk_count"] == 6
    assert payload["case_count"] == 10
    assert payload["top_1_hit_rate"] == 0.6
    assert payload["top_k_recall"] == 1.0
    assert payload["rows"][-1]["hit"] is True


if __name__ == "__main__":
    main()
