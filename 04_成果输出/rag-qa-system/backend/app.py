from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from backend.services.chunking import split_text_into_chunks
from backend.services.embeddings import COLLECTION_NAMES, KEYWORD_EMBEDDING_MODE
from backend.services.retrieval import build_chunk_collection, get_collection_name


DEFAULT_CHUNK_SIZE = 350
DEFAULT_CHUNK_OVERLAP = 50


class DocumentRequest(BaseModel):
    text: str = Field(..., min_length=1)
    embedding_mode: str = KEYWORD_EMBEDDING_MODE
    chunk_size: int = DEFAULT_CHUNK_SIZE
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP


class DocumentResponse(BaseModel):
    document_id: str
    embedding_mode: str
    collection_name: str
    chunk_count: int
    stored_chunk_count: int


app = FastAPI(
    title="DocuAsk API",
    description="Backend service for the local document RAG QA system.",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "docuask-api",
        "version": "0.1.0",
    }


@app.post("/documents", response_model=DocumentResponse)
def create_document(request: DocumentRequest) -> DocumentResponse:
    if request.embedding_mode not in COLLECTION_NAMES:
        raise HTTPException(status_code=400, detail="unsupported embedding mode")

    try:
        chunks = split_text_into_chunks(
            request.text,
            chunk_size=request.chunk_size,
            chunk_overlap=request.chunk_overlap,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if not chunks:
        raise HTTPException(status_code=400, detail="document text is empty")

    collection = build_chunk_collection(chunks, request.embedding_mode)
    if collection is None:
        raise HTTPException(status_code=400, detail="document has no embeddable chunks")

    collection_name = get_collection_name(chunks, request.embedding_mode)
    document_id = collection_name.rsplit("_", maxsplit=1)[-1]

    return DocumentResponse(
        document_id=document_id,
        embedding_mode=request.embedding_mode,
        collection_name=collection_name,
        chunk_count=len(chunks),
        stored_chunk_count=collection.count(),
    )
