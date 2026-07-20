from fastapi.testclient import TestClient

from backend.app import app
from backend.services.embeddings import KEYWORD_EMBEDDING_MODE
from conftest import FAQ_PATH


def test_documents_endpoint_indexes_faq_document():
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

    assert response.status_code == 200
    assert payload["embedding_mode"] == KEYWORD_EMBEDDING_MODE
    assert payload["chunk_count"] == 6
    assert payload["stored_chunk_count"] == 6
    assert payload["collection_name"].startswith("uploaded_document_chunks_keyword_")


def test_documents_upload_endpoint_indexes_markdown_file():
    client = TestClient(app)
    text = FAQ_PATH.read_text(encoding="utf-8")

    response = client.post(
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

    payload = response.json()

    assert response.status_code == 200
    assert payload["embedding_mode"] == KEYWORD_EMBEDDING_MODE
    assert payload["chunk_count"] == 6
    assert payload["stored_chunk_count"] == 6


def test_documents_upload_endpoint_rejects_unsupported_file_type():
    client = TestClient(app)

    response = client.post(
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

    assert response.status_code == 400
    assert response.json()["detail"] == "unsupported file type"


def test_qa_endpoint_retrieves_expected_chunk():
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

    qa_response = client.post(
        "/qa",
        json={
            "collection_name": collection_name,
            "question": "RAG 的基本流程是什么？",
            "embedding_mode": KEYWORD_EMBEDDING_MODE,
            "top_k": 3,
        },
    )

    payload = qa_response.json()
    retrieved_chunks = payload["retrieved_chunks"]

    assert qa_response.status_code == 200
    assert payload["retrieval_mode"] == "vector"
    assert retrieved_chunks[0]["chunk_index"] == 6
    assert len(retrieved_chunks) == 3
    assert "[Chunk 6]" in payload["context"]


def test_qa_endpoint_supports_bm25_mode():
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

    qa_response = client.post(
        "/qa",
        json={
            "collection_name": collection_name,
            "question": "RAG 的基本流程是什么？",
            "embedding_mode": KEYWORD_EMBEDDING_MODE,
            "top_k": 3,
            "retrieval_mode": "bm25",
        },
    )

    payload = qa_response.json()
    retrieved_chunks = payload["retrieved_chunks"]

    assert qa_response.status_code == 200
    assert payload["retrieval_mode"] == "bm25"
    assert retrieved_chunks[0]["chunk_index"] == 6
    assert retrieved_chunks[0]["score"] > 0


def test_qa_endpoint_supports_rrf_mode():
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

    qa_response = client.post(
        "/qa",
        json={
            "collection_name": collection_name,
            "question": "RAG 的基本流程是什么？",
            "embedding_mode": KEYWORD_EMBEDDING_MODE,
            "top_k": 3,
            "retrieval_mode": "rrf",
        },
    )

    payload = qa_response.json()
    retrieved_chunks = payload["retrieved_chunks"]

    assert qa_response.status_code == 200
    assert payload["retrieval_mode"] == "rrf"
    assert retrieved_chunks[0]["chunk_index"] == 6
    assert retrieved_chunks[0]["rrf_score"] > 0


def test_qa_endpoint_returns_404_for_missing_collection():
    client = TestClient(app)

    response = client.post(
        "/qa",
        json={
            "collection_name": "missing_collection",
            "question": "RAG 的基本流程是什么？",
            "embedding_mode": KEYWORD_EMBEDDING_MODE,
            "top_k": 3,
        },
    )

    assert response.status_code == 404


def test_qa_endpoint_returns_400_for_unknown_retrieval_mode():
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

    response = client.post(
        "/qa",
        json={
            "collection_name": collection_name,
            "question": "RAG 的基本流程是什么？",
            "embedding_mode": KEYWORD_EMBEDDING_MODE,
            "top_k": 3,
            "retrieval_mode": "unknown",
        },
    )

    assert response.status_code == 400


def test_answer_endpoint_returns_503_when_api_key_is_missing(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)

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

    response = client.post(
        "/answer",
        json={
            "collection_name": collection_name,
            "question": "RAG 的基本流程是什么？",
            "embedding_mode": KEYWORD_EMBEDDING_MODE,
            "top_k": 3,
            "retrieval_mode": "vector",
        },
    )

    assert response.status_code == 503
    assert response.json()["detail"] == "DEEPSEEK_API_KEY is not set."


def test_answer_endpoint_returns_400_for_unknown_retrieval_mode():
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

    response = client.post(
        "/answer",
        json={
            "collection_name": collection_name,
            "question": "RAG 的基本流程是什么？",
            "embedding_mode": KEYWORD_EMBEDDING_MODE,
            "top_k": 3,
            "retrieval_mode": "unknown",
        },
    )

    assert response.status_code == 400


def test_evaluation_endpoint_returns_fixed_metrics():
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

    assert response.status_code == 200
    assert payload["retrieval_mode"] == "vector"
    assert payload["chunk_count"] == 6
    assert payload["case_count"] == 10
    assert payload["top_1_hit_rate"] == 0.6
    assert payload["top_k_recall"] == 1.0
    assert payload["rows"][-1]["question"] == "RAG 的基本流程是什么？"
    assert payload["rows"][-1]["hit"] is True


def test_evaluation_endpoint_supports_bm25_mode():
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
            "retrieval_mode": "bm25",
        },
    )

    payload = response.json()

    assert response.status_code == 200
    assert payload["retrieval_mode"] == "bm25"
    assert payload["chunk_count"] == 6
    assert payload["case_count"] == 10
    assert payload["top_k_recall"] >= 0.8


def test_evaluation_endpoint_supports_rrf_mode():
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
            "retrieval_mode": "rrf",
        },
    )

    payload = response.json()

    assert response.status_code == 200
    assert payload["retrieval_mode"] == "rrf"
    assert payload["chunk_count"] == 6
    assert payload["case_count"] == 10
    assert payload["top_k_recall"] >= 0.8


def test_evaluation_endpoint_returns_400_for_unknown_retrieval_mode():
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
            "retrieval_mode": "unknown",
        },
    )

    assert response.status_code == 400
