import chromadb

from backend.services.embeddings import (
    COLLECTION_NAMES,
    KEYWORD_EMBEDDING_MODE,
    embed_for_mode,
)


def build_chunk_collection(chunks: list[str], embedding_mode: str):
    client = chromadb.EphemeralClient()
    collection = client.get_or_create_collection(
        name=COLLECTION_NAMES[embedding_mode],
        metadata={"hnsw:space": "cosine"},
    )

    embedded_chunks = []
    for index, chunk in enumerate(chunks, start=1):
        embedding = embed_for_mode(chunk, embedding_mode)
        if any(embedding):
            embedded_chunks.append((index, chunk, embedding))

    if not embedded_chunks:
        return None

    ids = [f"chunk-{index}" for index, _, _ in embedded_chunks]
    documents = [chunk for _, chunk, _ in embedded_chunks]
    embeddings = [embedding for _, _, embedding in embedded_chunks]
    metadatas = [{"chunk_index": index} for index, _, _ in embedded_chunks]

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    return collection


def retrieve_relevant_chunks(
    question: str,
    chunks: list[str],
    top_k: int,
    embedding_mode: str = KEYWORD_EMBEDDING_MODE,
) -> list[dict]:
    if not chunks:
        return []

    query_embedding = embed_for_mode(question, embedding_mode)
    if not any(query_embedding):
        return []

    collection = build_chunk_collection(chunks, embedding_mode)
    if collection is None:
        return []

    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    retrieved_chunks = []
    for document, metadata, distance in zip(
        result["documents"][0],
        result["metadatas"][0],
        result["distances"][0],
    ):
        retrieved_chunks.append(
            {
                "text": document,
                "chunk_index": metadata["chunk_index"],
                "distance": distance,
            }
        )

    return retrieved_chunks


def format_retrieved_context(retrieved_chunks: list[dict]) -> str:
    context_blocks = []

    for item in retrieved_chunks:
        context_blocks.append(
            f"[Chunk {item['chunk_index']}]\n{item['text']}"
        )

    return "\n\n---\n\n".join(context_blocks)
