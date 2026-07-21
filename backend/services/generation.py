import os

from openai import OpenAI

from backend.services.retrieval import format_retrieved_context


DEEPSEEK_MODEL = "deepseek-v4-flash"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"


class MissingApiKeyError(RuntimeError):
    pass


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
        raise MissingApiKeyError("DEEPSEEK_API_KEY is not set.")

    sources = format_sources(retrieved_chunks)
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


def format_sources(retrieved_chunks: list[dict]) -> str:
    return ", ".join(f"Chunk {item['chunk_index']}" for item in retrieved_chunks)
