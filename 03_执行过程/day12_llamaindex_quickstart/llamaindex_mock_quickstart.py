import sys
from pathlib import Path


sys.stdout.reconfigure(encoding="utf-8")


CONCEPTS = {
    "api": ["api", "key", "环境变量", "deepseek", "base_url", "sdk"],
    "embedding": ["embedding", "向量", "chroma", "相似度"],
    "dify": ["dify", "chatflow", "knowledge", "retrieval", "知识库"],
    "sql": ["sql", "select", "where", "order by", "group by", "join", "结构化", "表格", "学生表", "课程表"],
}


class KeywordEmbedding:
    def __init__(self, concepts):
        self.concepts = concepts

    def _embed(self, text):
        text = text.lower()
        vector = []

        for keywords in self.concepts.values():
            score = 0.0
            for keyword in keywords:
                if keyword.lower() in text:
                    score += 1.0
            vector.append(score)

        return vector

    def __call__(self, texts):
        return [self._embed(text) for text in texts]


def main():
    try:
        from llama_index.core import Settings
        from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
        from llama_index.core.llms import MockLLM
        from llama_index.core.embeddings import BaseEmbedding
    except ModuleNotFoundError:
        print("llama-index is not installed.")
        print("Install it with: python -m pip install llama-index")
        return

    class LocalKeywordEmbedding(BaseEmbedding):
        def _get_text_embedding(self, text):
            return KeywordEmbedding(CONCEPTS)._embed(text)

        def _get_query_embedding(self, query):
            return KeywordEmbedding(CONCEPTS)._embed(query)

        async def _aget_query_embedding(self, query):
            return self._get_query_embedding(query)

    current_dir = Path(__file__).resolve().parent
    data_dir = current_dir / "data"

    Settings.llm = MockLLM(max_tokens=128)
    Settings.embed_model = LocalKeywordEmbedding()

    print("Loading documents...")
    documents = SimpleDirectoryReader(str(data_dir)).load_data()
    print(f"Loaded documents: {len(documents)}")

    for doc in documents:
        print(f"- Document ID: {doc.doc_id}")
        print(f"  Text preview: {doc.text[:80].replace(chr(10), ' ')}...")

    print()
    print("Building VectorStoreIndex...")
    index = VectorStoreIndex.from_documents(documents)
    print("Index built.")

    query_engine = index.as_query_engine()
    question = "SQL 适合查询什么类型的数据？"

    print()
    print(f"Query: {question}")

    retriever = index.as_retriever(similarity_top_k=2)
    retrieved_nodes = retriever.retrieve(question)

    print()
    print("Retrieved nodes:")
    for rank, node_with_score in enumerate(retrieved_nodes, start=1):
        text_preview = node_with_score.node.text[:240].replace("\n", " ")
        print(f"Rank {rank}")
        print(f"Score: {node_with_score.score}")
        print(f"Text preview: {text_preview}...")
        print()

    response = query_engine.query(question)

    print()
    print("Response:")
    print(response)
    print()
    print("Note: MockLLM is used today, so the response is not a real model answer.")
    print("The goal is to understand LlamaIndex loading, indexing, and querying flow.")


if __name__ == "__main__":
    main()
