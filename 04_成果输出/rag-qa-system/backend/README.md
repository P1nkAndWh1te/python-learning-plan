# DocuAsk FastAPI Backend

This backend is the first step of the DocuAsk v2 upgrade.

Current scope:

```text
GET /health
POST /documents
POST /qa
POST /evaluation
services/chunking.py
services/bm25.py
services/embeddings.py
services/evaluation.py
services/retrieval.py
services/rrf.py
storage/chroma_db*/ (local, ignored)
```

It does not replace the Streamlit app yet. The goal is to introduce a reusable
backend service boundary before moving RAG logic out of `app.py`.

## Run

From the project root:

```powershell
python -m uvicorn backend.app:app --app-dir "04_成果输出/rag-qa-system" --host 127.0.0.1 --port 8000
```

Open:

```text
http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "docuask-api",
  "version": "0.1.0"
}
```

## Index a Document

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/documents" -Method Post -ContentType "application/json" -Body '{
  "text": "# Python 学习 FAQ\n\n## RAG 的基本流程是什么？\nRAG 会先检索资料，再让 LLM 根据资料回答。",
  "embedding_mode": "Teaching keyword embedding",
  "chunk_size": 350,
  "chunk_overlap": 50
}'
```

Expected fields:

```text
document_id
embedding_mode
collection_name
chunk_count
stored_chunk_count
```

## Query a Document

Use the `collection_name` returned by `POST /documents`.

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/qa" -Method Post -ContentType "application/json" -Body '{
  "collection_name": "uploaded_document_chunks_keyword_xxxxxxxxxxxx",
  "question": "RAG 的基本流程是什么？",
  "embedding_mode": "Teaching keyword embedding",
  "top_k": 3,
  "retrieval_mode": "vector"
}'
```

Expected fields:

```text
question
embedding_mode
collection_name
top_k
retrieval_mode
retrieved_chunks
context
```

## Test

From the project root:

```powershell
python -m pytest -q
```

Current automated coverage:

```text
POST /documents
POST /qa
404 for missing collection
Teaching keyword retrieval metrics
```

## Evaluate Retrieval

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/evaluation" -Method Post -ContentType "application/json" -Body '{
  "text": "# Python 学习 FAQ\n\n## RAG 的基本流程是什么？\nRAG 会先检索资料，再让 LLM 根据资料回答。",
  "embedding_mode": "Teaching keyword embedding",
  "chunk_size": 350,
  "chunk_overlap": 50,
  "top_k": 3,
  "retrieval_mode": "vector"
}'
```

Expected fields:

```text
chunk_count
case_count
retrieval_mode
top_1_hit_rate
top_k_recall
rows
```

## Next

The next backend steps are:

- Add optional LLM generation.
- Add optional multipart file upload endpoint.
