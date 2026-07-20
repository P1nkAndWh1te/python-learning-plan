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
DOCUASK_BACKEND_FAQ_PATH = (
    PROJECT_ROOT
    / "02_资料与素材"
    / "day53_multi_document_eval"
    / "docuask_backend_faq.md"
)

if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from backend.app import app  # noqa: E402
from backend.services.embeddings import KEYWORD_EMBEDDING_MODE  # noqa: E402


def main() -> None:
    client = TestClient(app)
    evaluation_runs = [
        {
            "name": "python_learning_faq",
            "path": FAQ_PATH,
            "retrieval_mode": "rrf",
            "evaluation_cases": None,
            "expected_cases": 10,
        },
        {
            "name": "docuask_backend_faq",
            "path": DOCUASK_BACKEND_FAQ_PATH,
            "retrieval_mode": "bm25",
            "evaluation_cases": [
                {
                    "question": "FastAPI 后端有哪些接口？",
                    "expected_top_chunk": 2,
                },
                {
                    "question": "documents/upload 文件上传支持什么格式？",
                    "expected_top_chunk": 3,
                },
                {
                    "question": "RRF 混合检索有什么作用？",
                    "expected_top_chunk": 4,
                },
            ],
            "expected_cases": 3,
        },
    ]

    print("Document | Cases | Top-1 | Top-k")
    print("---|---:|---:|---:")

    for evaluation_run in evaluation_runs:
        request_body = {
            "text": evaluation_run["path"].read_text(encoding="utf-8"),
            "embedding_mode": KEYWORD_EMBEDDING_MODE,
            "chunk_size": 350,
            "chunk_overlap": 50,
            "top_k": 3,
            "retrieval_mode": evaluation_run["retrieval_mode"],
        }
        if evaluation_run["evaluation_cases"] is not None:
            request_body["evaluation_cases"] = evaluation_run["evaluation_cases"]

        response = client.post("/evaluation", json=request_body)
        payload = response.json()

        print(
            f"{evaluation_run['name']} | "
            f"{payload['case_count']} | "
            f"{payload['top_1_hit_rate']:.1f} | "
            f"{payload['top_k_recall']:.1f}"
        )

        assert response.status_code == 200
        assert payload["case_count"] == evaluation_run["expected_cases"]
        assert payload["top_k_recall"] == 1.0


if __name__ == "__main__":
    main()
