import os

import chromadb
import streamlit as st
from openai import OpenAI, OpenAIError, RateLimitError


MAX_PREVIEW_CHARS = 2000
DEFAULT_CHUNK_SIZE = 500
DEFAULT_CHUNK_OVERLAP = 100
TOP_K = 3
DEEPSEEK_MODEL = "deepseek-v4-flash"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

CONCEPTS = {
    "python": ["python", "脚本", "程序"],
    "api": ["api", "接口", "调用", "请求"],
    "git": ["git", "提交", "版本", "仓库"],
    "rag": ["rag", "检索", "文档", "知识库"],
    "data": ["数据", "csv", "表格", "pandas"],
    "sql": ["sql", "数据库", "查询", "表"],
    "embedding": ["embedding", "向量", "相似度"],
    "chroma": ["chroma", "向量数据库"],
    "llamaindex": ["llamaindex", "索引"],
    "deepseek": ["deepseek", "大模型", "llm"],
}


def read_uploaded_text(uploaded_file) -> tuple[str, str]:
    raw_bytes = uploaded_file.getvalue()

    for encoding in ("utf-8", "gbk"):
        try:
            return raw_bytes.decode(encoding), encoding
        except UnicodeDecodeError:
            continue

    return raw_bytes.decode("utf-8", errors="replace"), "utf-8 with replacement"


def split_text_into_chunks(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    cleaned_text = text.strip()
    if not cleaned_text:
        return []

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be greater than or equal to 0 and less than chunk_size"
        )

    chunks = []
    start = 0

    while start < len(cleaned_text):
        end = start + chunk_size
        chunks.append(cleaned_text[start:end])

        if end >= len(cleaned_text):
            break

        start = end - chunk_overlap

    return chunks


def embed_text(text: str) -> list[float]:
    lowered_text = text.lower()
    vector = []

    for keywords in CONCEPTS.values():
        score = 0
        for keyword in keywords:
            score += lowered_text.count(keyword.lower())
        vector.append(float(score))

    return vector


def get_matched_concepts(text: str) -> list[str]:
    vector = embed_text(text)
    concepts = list(CONCEPTS.keys())
    return [concept for concept, value in zip(concepts, vector) if value > 0]


def build_chunk_collection(chunks: list[str]):
    client = chromadb.EphemeralClient()
    collection = client.get_or_create_collection(name="uploaded_document_chunks")

    ids = [f"chunk-{index}" for index in range(1, len(chunks) + 1)]
    embeddings = [embed_text(chunk) for chunk in chunks]
    metadatas = [{"chunk_index": index} for index in range(1, len(chunks) + 1)]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    return collection


def retrieve_relevant_chunks(question: str, chunks: list[str], top_k: int) -> list[dict]:
    if not chunks:
        return []

    query_embedding = embed_text(question)
    if not any(query_embedding):
        return []

    collection = build_chunk_collection(chunks)
    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, len(chunks)),
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


def build_rag_prompt(question: str, context: str, sources: str) -> str:
    return f"""
请只根据下面的资料回答问题。
如果资料中没有相关信息，就回答：资料中没有找到相关信息。
回答最后必须写一行“来源：{sources}”。

问题：
{question}

资料：
{context}
""".strip()


def generate_answer_with_deepseek(question: str, retrieved_chunks: list[dict]) -> str:
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError("DEEPSEEK_API_KEY is not set.")

    sources = ", ".join(f"Chunk {item['chunk_index']}" for item in retrieved_chunks)
    context = format_retrieved_context(retrieved_chunks)
    prompt = build_rag_prompt(question, context, sources)

    client = OpenAI(
        api_key=api_key,
        base_url=DEEPSEEK_BASE_URL,
    )

    response = client.chat.completions.create(
        model=DEEPSEEK_MODEL,
        messages=[
            {
                "role": "system",
                "content": "你是一个严谨的 RAG 问答助手，只能根据给定资料回答。",
            },
            {"role": "user", "content": prompt},
        ],
        stream=False,
    )

    return response.choices[0].message.content or ""


def main() -> None:
    st.set_page_config(page_title="RAG QA System", page_icon="RAG", layout="wide")

    st.title("RAG QA System")
    st.caption("Day20: generate answers from retrieved context with DeepSeek")

    uploaded_file = st.file_uploader(
        "Upload a document",
        type=["txt", "md"],
        help="Day16 supports plain text and Markdown files.",
    )

    document_text = ""
    chunks = []

    if uploaded_file is not None:
        document_text, encoding = read_uploaded_text(uploaded_file)
        file_size = len(uploaded_file.getvalue())
        chunks = split_text_into_chunks(
            document_text,
            chunk_size=DEFAULT_CHUNK_SIZE,
            chunk_overlap=DEFAULT_CHUNK_OVERLAP,
        )

        st.success(f"Uploaded file: {uploaded_file.name}")
        st.write(f"Size: {file_size} bytes")
        st.write(f"Characters: {len(document_text)}")
        st.write(f"Detected encoding: {encoding}")
        st.write(f"Chunks: {len(chunks)}")

        with st.expander("Document preview", expanded=True):
            st.code(document_text[:MAX_PREVIEW_CHARS], language="markdown")

        st.subheader("Chunks")
        st.caption(
            f"Chunk size: {DEFAULT_CHUNK_SIZE} characters, "
            f"overlap: {DEFAULT_CHUNK_OVERLAP} characters"
        )

        for index, chunk in enumerate(chunks, start=1):
            with st.expander(f"Chunk {index} | {len(chunk)} characters"):
                st.code(chunk, language="markdown")

    question = st.text_area(
        "Question",
        placeholder="Ask a question about the uploaded document.",
        height=120,
    )

    submitted = st.button("Ask", type="primary")

    if submitted:
        if uploaded_file is None:
            st.warning("Please upload a document first.")
            return

        if not document_text.strip():
            st.warning("The uploaded document is empty.")
            return

        if not question.strip():
            st.warning("Please enter a question.")
            return

        st.subheader("Answer")
        retrieved_chunks = retrieve_relevant_chunks(question, chunks, top_k=TOP_K)
        matched_concepts = get_matched_concepts(question)

        if not retrieved_chunks:
            st.warning(
                "No relevant chunks found by the manual embedding. Try a question "
                "with keywords such as Python, API, RAG, SQL, embedding, or Chroma."
            )
            return

        st.write(
            "The app has embedded chunks with a manual keyword vector and retrieved "
            "the most relevant chunks from Chroma. DeepSeek will generate the final "
            "answer from these chunks only."
        )

        st.write("Matched concepts:", ", ".join(matched_concepts))
        st.caption("Distance is returned by Chroma. Lower distance means more similar.")

        st.subheader("Context for later LLM")
        st.code(format_retrieved_context(retrieved_chunks), language="markdown")

        st.subheader("Sources")
        st.write(
            ", ".join(
                f"Chunk {item['chunk_index']}" for item in retrieved_chunks
            )
        )

        try:
            with st.spinner("Generating answer with DeepSeek..."):
                final_answer = generate_answer_with_deepseek(question, retrieved_chunks)
        except RuntimeError:
            st.warning(
                "DEEPSEEK_API_KEY is not set in the current environment. "
                "Set it before running the app to generate the final answer."
            )
            final_answer = ""
        except RateLimitError as exc:
            st.error("DeepSeek request reached the server, but quota or rate limit failed.")
            st.exception(exc)
            final_answer = ""
        except OpenAIError as exc:
            st.error("DeepSeek request failed.")
            st.exception(exc)
            final_answer = ""

        if final_answer:
            st.subheader("Final answer")
            st.write(final_answer)

        st.subheader("Retrieved chunks")
        for rank, item in enumerate(retrieved_chunks, start=1):
            with st.expander(
                f"Rank {rank} | Chunk {item['chunk_index']} | Distance {item['distance']:.4f}",
                expanded=rank == 1,
            ):
                st.code(item["text"], language="markdown")


if __name__ == "__main__":
    main()
