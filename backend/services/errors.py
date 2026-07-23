from enum import StrEnum

from fastapi import HTTPException


class ErrorCode(StrEnum):
    UNSUPPORTED_EMBEDDING_MODE = "unsupported_embedding_mode"
    UNSUPPORTED_RETRIEVAL_MODE = "unsupported_retrieval_mode"
    UNSUPPORTED_FILE_TYPE = "unsupported_file_type"
    DOCUMENT_PARSE_FAILED = "document_parse_failed"
    EMPTY_DOCUMENT = "empty_document"
    INVALID_CHUNKING_CONFIG = "invalid_chunking_config"
    NO_EMBEDDABLE_CHUNKS = "no_embeddable_chunks"
    COLLECTION_NOT_FOUND = "collection_not_found"
    MISSING_API_KEY = "missing_api_key"
    LLM_RATE_LIMIT = "llm_rate_limit"
    LLM_REQUEST_FAILED = "llm_request_failed"


def error_detail(code: ErrorCode, message: str) -> dict[str, str]:
    return {
        "code": code.value,
        "message": message,
    }


def raise_http_error(status_code: int, code: ErrorCode, message: str) -> None:
    raise HTTPException(
        status_code=status_code,
        detail=error_detail(code, message),
    )
