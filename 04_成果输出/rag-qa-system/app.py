import streamlit as st


MAX_PREVIEW_CHARS = 2000
DEFAULT_CHUNK_SIZE = 500
DEFAULT_CHUNK_OVERLAP = 100


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


def main() -> None:
    st.set_page_config(page_title="RAG QA System", page_icon="RAG", layout="wide")

    st.title("RAG QA System")
    st.caption("Day17: split uploaded documents into chunks")

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
        st.write(
            "This is still a placeholder answer. The app has read the uploaded "
            "document and split it into chunks. Day18-Day20 will connect embedding, "
            "retrieval, and LLM generation."
        )


if __name__ == "__main__":
    main()
