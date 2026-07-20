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
    assert retrieved_chunks[0]["chunk_index"] == 6
    assert len(retrieved_chunks) == 3
    assert "[Chunk 6]" in payload["context"]


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
    assert payload["chunk_count"] == 6
    assert payload["case_count"] == 10
    assert payload["top_1_hit_rate"] == 0.6
    assert payload["top_k_recall"] == 1.0
    assert payload["rows"][-1]["question"] == "RAG 的基本流程是什么？"
    assert payload["rows"][-1]["hit"] is True
