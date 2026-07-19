# DocuAsk FastAPI Backend

This backend is the first step of the DocuAsk v2 upgrade.

Current scope:

```text
GET /health
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

## Next

The next backend steps are:

- Extract chunking logic from Streamlit.
- Add document upload endpoint.
- Add QA endpoint.
- Add evaluation endpoint.

