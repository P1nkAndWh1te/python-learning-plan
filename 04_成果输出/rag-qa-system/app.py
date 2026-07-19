import streamlit as st


MAX_PREVIEW_CHARS = 2000


def read_uploaded_text(uploaded_file) -> tuple[str, str]:
    raw_bytes = uploaded_file.getvalue()

    for encoding in ("utf-8", "gbk"):
        try:
            return raw_bytes.decode(encoding), encoding
        except UnicodeDecodeError:
            continue

    return raw_bytes.decode("utf-8", errors="replace"), "utf-8 with replacement"


def main() -> None:
    st.set_page_config(page_title="RAG QA System", page_icon="RAG", layout="wide")

    st.title("RAG QA System")
    st.caption("Day16: read uploaded TXT/Markdown documents")

    uploaded_file = st.file_uploader(
        "Upload a document",
        type=["txt", "md"],
        help="Day16 supports plain text and Markdown files.",
    )

    document_text = ""

    if uploaded_file is not None:
        document_text, encoding = read_uploaded_text(uploaded_file)
        file_size = len(uploaded_file.getvalue())

        st.success(f"Uploaded file: {uploaded_file.name}")
        st.write(f"Size: {file_size} bytes")
        st.write(f"Characters: {len(document_text)}")
        st.write(f"Detected encoding: {encoding}")

        with st.expander("Document preview", expanded=True):
            st.code(document_text[:MAX_PREVIEW_CHARS], language="markdown")

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
            "document, and Day17-Day20 will connect chunking, retrieval, and LLM "
            "generation."
        )


if __name__ == "__main__":
    main()
