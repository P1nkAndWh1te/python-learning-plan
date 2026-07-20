from backend.services.embeddings import KEYWORD_EMBEDDING_MODE, get_matched_concepts
from backend.services.retrieval import retrieve_relevant_chunks


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
