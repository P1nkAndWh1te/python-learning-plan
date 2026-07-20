import os
import sys
from pathlib import Path

import streamlit as st
from openai import OpenAI, OpenAIError, RateLimitError


APP_ROOT = Path(__file__).resolve().parent
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from backend.services.chunking import split_text_into_chunks
from backend.services.embeddings import (
    BGE_EMBEDDING_MODE,
    BGE_MODEL_NAME,
    KEYWORD_EMBEDDING_MODE,
    get_matched_concepts,
)
from backend.services.retrieval import (
    format_retrieved_context,
    retrieve_relevant_chunks,
)


MAX_PREVIEW_CHARS = 2000
DEFAULT_CHUNK_SIZE = 350
DEFAULT_CHUNK_OVERLAP = 50
TOP_K = 3
DEEPSEEK_MODEL = "deepseek-v4-flash"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

EVALUATION_CASES = [
    {"question": "Day8 学了什么？", "expected_top_chunk": 2},
    {"question": "DeepSeek API 怎么配置？", "expected_top_chunk": 2},
    {"question": "OpenAI API 额度和 ChatGPT Plus 互通吗？", "expected_top_chunk": 2},
    {"question": "API Key 为什么不能写进代码？", "expected_top_chunk": 3},
    {"question": "怎么从环境变量读取 DEEPSEEK_API_KEY？", "expected_top_chunk": 3},
    {"question": "Day9 学了什么？", "expected_top_chunk": 4},
    {"question": "什么是 embedding？", "expected_top_chunk": 4},
    {"question": "向量数据库有什么作用？", "expected_top_chunk": 5},
    {"question": "当前项目使用哪个向量数据库？", "expected_top_chunk": 5},
    {"question": "RAG 的基本流程是什么？", "expected_top_chunk": 6},
]

def read_uploaded_text(uploaded_file) -> tuple[str, str]:
    raw_bytes = uploaded_file.getvalue()

    for encoding in ("utf-8", "gbk"):
        try:
            return raw_bytes.decode(encoding), encoding
        except UnicodeDecodeError:
            continue

    return raw_bytes.decode("utf-8", errors="replace"), "utf-8 with replacement"


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


def evaluate_retrieval(
    evaluation_cases: list[dict],
    chunks: list[str],
    top_k: int,
    embedding_mode: str = KEYWORD_EMBEDDING_MODE,
) -> list[dict]:
    rows = []

    for case in evaluation_cases:
        question = case["question"]
        expected_top_chunk = case["expected_top_chunk"]
        retrieved_chunks = retrieve_relevant_chunks(
            question,
            chunks,
            top_k=top_k,
            embedding_mode=embedding_mode,
        )
        matched_concepts = get_matched_concepts(question)
        actual_top_chunk = (
            retrieved_chunks[0]["chunk_index"]
            if retrieved_chunks
            else None
        )
        retrieved_chunk_indexes = [
            item["chunk_index"]
            for item in retrieved_chunks
        ]

        rows.append(
            {
                "question": question,
                "embedding_mode": embedding_mode,
                "expected_top_chunk": f"Chunk {expected_top_chunk}",
                "matched_concepts": ", ".join(matched_concepts) or "none",
                "top_chunks": ", ".join(
                    f"Chunk {item['chunk_index']}" for item in retrieved_chunks
                ) or "none",
                "best_distance": (
                    f"{retrieved_chunks[0]['distance']:.4f}"
                    if retrieved_chunks
                    else "none"
                ),
                "hit": actual_top_chunk == expected_top_chunk,
                "top_k_hit": expected_top_chunk in retrieved_chunk_indexes,
            }
        )

    return rows


def calculate_hit_rate(evaluation_rows: list[dict]) -> float:
    if not evaluation_rows:
        return 0.0

    hit_count = sum(1 for row in evaluation_rows if row["hit"])
    return hit_count / len(evaluation_rows)


def calculate_top_k_hit_rate(evaluation_rows: list[dict]) -> float:
    if not evaluation_rows:
        return 0.0

    hit_count = sum(1 for row in evaluation_rows if row["top_k_hit"])
    return hit_count / len(evaluation_rows)


def main() -> None:
    st.set_page_config(page_title="RAG QA System", page_icon="RAG", layout="wide")

    st.title("RAG QA System")
    st.caption("Local document QA with retrieval evaluation and source citations")

    embedding_mode = st.sidebar.radio(
        "Embedding mode",
        [KEYWORD_EMBEDDING_MODE, BGE_EMBEDDING_MODE],
        help=(
            "Teaching mode is fast and explainable. BGE mode uses a real Chinese "
            "embedding model and may take longer on first load."
        ),
    )

    st.sidebar.caption(f"Current mode: {embedding_mode}")
    if embedding_mode == BGE_EMBEDDING_MODE:
        st.sidebar.caption(f"Model: {BGE_MODEL_NAME}")
        st.sidebar.info(
            "BGE mode loads a local Chinese embedding model. The first evaluation "
            "or question may take longer."
        )

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

        st.subheader("Retrieval evaluation")
        st.caption(
            "Run fixed questions to inspect which chunks are retrieved before LLM generation."
        )
        evaluation_rows = evaluate_retrieval(
            EVALUATION_CASES,
            chunks,
            top_k=TOP_K,
            embedding_mode=embedding_mode,
        )
        hit_rate = calculate_hit_rate(evaluation_rows)
        top_k_hit_rate = calculate_top_k_hit_rate(evaluation_rows)
        metric_columns = st.columns(2)
        metric_columns[0].metric("Top-1 hit", f"{hit_rate:.0%}")
        metric_columns[1].metric("Top-k recall", f"{top_k_hit_rate:.0%}")
        st.dataframe(evaluation_rows, use_container_width=True, hide_index=True)

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
        retrieved_chunks = retrieve_relevant_chunks(
            question,
            chunks,
            top_k=TOP_K,
            embedding_mode=embedding_mode,
        )
        matched_concepts = get_matched_concepts(question)

        if not retrieved_chunks:
            st.warning(
                "No relevant chunks found by the selected embedding mode. Try a question "
                "with keywords such as Python, API, RAG, SQL, embedding, or Chroma."
            )
            return

        st.write(
            f"The app has embedded chunks with {embedding_mode} and retrieved "
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
