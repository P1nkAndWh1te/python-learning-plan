import os
import sys
from pathlib import Path

from openai import OpenAI, OpenAIError


sys.stdout.reconfigure(encoding="utf-8")


CONCEPTS = {
    "api": ["api", "key", "环境变量", "deepseek", "base_url", "sdk"],
    "embedding": ["embedding", "向量", "chroma", "相似度"],
    "dify": ["dify", "chatflow", "knowledge", "retrieval", "知识库"],
    "sql": ["sql", "select", "where", "order by", "group by", "join", "结构化", "表格", "学生表", "课程表"],
}


def keyword_vector(text):
    text = text.lower()
    vector = []

    for keywords in CONCEPTS.values():
        score = 0.0
        for keyword in keywords:
            if keyword.lower() in text:
                score += 1.0
        vector.append(score)

    return vector


def build_index(data_dir):
    from llama_index.core import Settings
    from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
    from llama_index.core.embeddings import BaseEmbedding
    from llama_index.core.llms import MockLLM

    class LocalKeywordEmbedding(BaseEmbedding):
        def _get_text_embedding(self, text):
            return keyword_vector(text)

        def _get_query_embedding(self, query):
            return keyword_vector(query)

        async def _aget_query_embedding(self, query):
            return self._get_query_embedding(query)

    Settings.llm = MockLLM(max_tokens=128)
    Settings.embed_model = LocalKeywordEmbedding()

    documents = SimpleDirectoryReader(str(data_dir)).load_data()
    return VectorStoreIndex.from_documents(documents)


def ask_deepseek(question, context):
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        print("DEEPSEEK_API_KEY is not set.")
        print('PowerShell temporary setup: $env:DEEPSEEK_API_KEY="your_api_key"')
        return None

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
    )

    prompt = f"""
请只根据下面的资料回答问题。
如果资料中没有相关信息，就回答：资料中没有找到相关信息。

问题：
{question}

资料：
{context}
""".strip()

    try:
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[
                {"role": "system", "content": "你是一个严谨的 RAG 问答助手。"},
                {"role": "user", "content": prompt},
            ],
            stream=False,
        )
    except OpenAIError as exc:
        print("DeepSeek request failed.")
        print(f"Error: {exc}")
        return None

    return response.choices[0].message.content


def main():
    current_dir = Path(__file__).resolve().parent
    data_dir = current_dir.parent / "day12_llamaindex_quickstart" / "data"
    question = "SQL 适合查询什么类型的数据？"

    print("Building LlamaIndex index...")
    index = build_index(data_dir)
    retriever = index.as_retriever(similarity_top_k=2)

    print(f"Question: {question}")
    print()

    nodes = retriever.retrieve(question)

    print("Retrieved context:")
    context_parts = []
    for rank, node_with_score in enumerate(nodes, start=1):
        text = node_with_score.node.text
        context_parts.append(text)
        print(f"Rank {rank}")
        print(f"Score: {node_with_score.score}")
        print(text[:400].replace("\n", " "))
        print()

    context = "\n\n---\n\n".join(context_parts)

    print("DeepSeek answer:")
    answer = ask_deepseek(question, context)
    if answer:
        print(answer)


if __name__ == "__main__":
    main()

