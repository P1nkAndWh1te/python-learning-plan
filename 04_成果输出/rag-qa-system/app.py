import streamlit as st


def main() -> None:
    st.set_page_config(page_title="RAG QA System", page_icon="RAG", layout="wide")

    st.title("RAG QA System")
    st.caption("Day15: Streamlit minimal interface")

    uploaded_file = st.file_uploader(
        "Upload a document",
        type=["txt", "md", "pdf"],
        help="Today only builds the UI. File parsing starts on Day16.",
    )

    question = st.text_area(
        "Question",
        placeholder="Ask a question about the uploaded document.",
        height=120,
    )

    submitted = st.button("Ask", type="primary")

    if uploaded_file is not None:
        st.info(f"Uploaded file: {uploaded_file.name}")

    if submitted:
        if uploaded_file is None:
            st.warning("Please upload a document first.")
            return

        if not question.strip():
            st.warning("Please enter a question.")
            return

        st.subheader("Answer")
        st.write(
            "This is a placeholder answer. Day16-Day20 will connect document "
            "reading, chunking, retrieval, and LLM generation."
        )


if __name__ == "__main__":
    main()
