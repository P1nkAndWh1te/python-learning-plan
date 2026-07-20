from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from backend.services.chunking import split_text_into_chunks
from backend.services.embeddings import COLLECTION_NAMES, KEYWORD_EMBEDDING_MODE
from backend.services.evaluation import (
    EVALUATION_CASES,
    calculate_hit_rate,
    calculate_top_k_hit_rate,
    evaluate_retrieval,
)
from backend.services.retrieval import (
    build_chunk_collection,
    format_retrieved_context,
    get_collection_name,
    retrieve_relevant_chunks_from_collection,
)


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


class RetrievedChunk(BaseModel):
    chunk_index: int
    distance: float
    text: str


class QaRequest(BaseModel):
    collection_name: str = Field(..., min_length=1)
    question: str = Field(..., min_length=1)
    embedding_mode: str = KEYWORD_EMBEDDING_MODE
    top_k: int = Field(default=3, ge=1, le=10)


class QaResponse(BaseModel):
    question: str
    embedding_mode: str
    collection_name: str
    top_k: int
    retrieved_chunks: list[RetrievedChunk]
    context: str


class EvaluationRequest(BaseModel):
    text: str = Field(..., min_length=1)
    embedding_mode: str = KEYWORD_EMBEDDING_MODE
    chunk_size: int = DEFAULT_CHUNK_SIZE
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP
    top_k: int = Field(default=3, ge=1, le=10)


class EvaluationRow(BaseModel):
    question: str
    embedding_mode: str
    expected_top_chunk: str
    matched_concepts: str
    top_chunks: str
    best_distance: str
    hit: bool
    top_k_hit: bool


class EvaluationResponse(BaseModel):
    embedding_mode: str
    chunk_count: int
    case_count: int
    top_1_hit_rate: float
    top_k_recall: float
    rows: list[EvaluationRow]


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


@app.post("/qa", response_model=QaResponse)
def query_document(request: QaRequest) -> QaResponse:
    if request.embedding_mode not in COLLECTION_NAMES:
        raise HTTPException(status_code=400, detail="unsupported embedding mode")

    retrieved_chunks = retrieve_relevant_chunks_from_collection(
        request.collection_name,
        request.question,
        top_k=request.top_k,
        embedding_mode=request.embedding_mode,
    )

    if retrieved_chunks is None:
        raise HTTPException(status_code=404, detail="collection not found")

    return QaResponse(
        question=request.question,
        embedding_mode=request.embedding_mode,
        collection_name=request.collection_name,
        top_k=request.top_k,
        retrieved_chunks=[
            RetrievedChunk(
                chunk_index=item["chunk_index"],
                distance=item["distance"],
                text=item["text"],
            )
            for item in retrieved_chunks
        ],
        context=format_retrieved_context(retrieved_chunks),
    )


@app.post("/evaluation", response_model=EvaluationResponse)
def evaluate_document(request: EvaluationRequest) -> EvaluationResponse:
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

    rows = evaluate_retrieval(
        EVALUATION_CASES,
        chunks,
        top_k=request.top_k,
        embedding_mode=request.embedding_mode,
    )

    return EvaluationResponse(
        embedding_mode=request.embedding_mode,
        chunk_count=len(chunks),
        case_count=len(rows),
        top_1_hit_rate=calculate_hit_rate(rows),
        top_k_recall=calculate_top_k_hit_rate(rows),
        rows=[EvaluationRow(**row) for row in rows],
    )
