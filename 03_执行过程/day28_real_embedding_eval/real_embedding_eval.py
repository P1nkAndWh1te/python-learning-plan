from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction


sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
APP_PATH = PROJECT_ROOT / "04_成果输出" / "rag-qa-system" / "app.py"
FAQ_PATH = (
    PROJECT_ROOT
    / "02_资料与素材"
    / "day10_dify_knowledge"
    / "python_learning_faq.md"
)
BASELINE_HIT_RATE = 60.0


def load_rag_app_module():
    spec = importlib.util.spec_from_file_location("rag_app", APP_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load app module from {APP_PATH}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_collection(chunks: list[str]):
    client = chromadb.EphemeralClient()
    embedding_function = DefaultEmbeddingFunction()
    collection = client.get_or_create_collection(
        name="day28-real-embedding-eval",
        embedding_function=embedding_function,
        metadata={"hnsw:space": "cosine"},
    )

    collection.add(
        ids=[f"chunk-{index}" for index in range(1, len(chunks) + 1)],
        documents=chunks,
        metadatas=[
            {"chunk_index": index}
            for index in range(1, len(chunks) + 1)
        ],
    )
    return collection


def evaluate(collection, evaluation_cases: list[dict], top_k: int) -> list[dict]:
    rows = []
    result_count = min(top_k, collection.count())

    for case in evaluation_cases:
        result = collection.query(
            query_texts=[case["question"]],
            n_results=result_count,
            include=["metadatas", "documents", "distances"],
        )

        metadatas = result["metadatas"][0]
        distances = result["distances"][0]
        actual_chunks = [
            metadata["chunk_index"]
            for metadata in metadatas
        ]
        expected = case["expected_top_chunk"]
        actual_top = actual_chunks[0]

        rows.append(
            {
                "question": case["question"],
                "expected": expected,
                "actual_top": actual_top,
                "top_chunks": actual_chunks,
                "best_distance": distances[0],
                "hit": actual_top == expected,
            }
        )

    return rows


def main() -> None:
    rag_app = load_rag_app_module()
    text = FAQ_PATH.read_text(encoding="utf-8")
    chunks = rag_app.split_text_into_chunks(
        text,
        chunk_size=rag_app.DEFAULT_CHUNK_SIZE,
        chunk_overlap=rag_app.DEFAULT_CHUNK_OVERLAP,
    )

    collection = build_collection(chunks)
    rows = evaluate(collection, rag_app.EVALUATION_CASES, top_k=rag_app.TOP_K)

    hit_count = sum(1 for row in rows if row["hit"])
    hit_rate = hit_count / len(rows) * 100
    delta = hit_rate - BASELINE_HIT_RATE

    print("Day28 real embedding evaluation")
    print(f"FAQ: {FAQ_PATH}")
    print(f"Chunks: {len(chunks)}")
    print("Embedding: Chroma DefaultEmbeddingFunction")
    print(f"Baseline hit rate: {BASELINE_HIT_RATE:.1f}%")
    print(f"Real embedding hit rate: {hit_rate:.1f}%")
    print(f"Delta: {delta:+.1f}%")
    print()
    print("| # | Hit | Expected | Actual top | Top chunks | Best distance | Question |")
    print("|---|---|---:|---:|---|---:|---|")
    for index, row in enumerate(rows, start=1):
        hit_mark = "yes" if row["hit"] else "no"
        top_chunks = ", ".join(f"Chunk {chunk}" for chunk in row["top_chunks"])
        print(
            f"| {index} | {hit_mark} | {row['expected']} | {row['actual_top']} | "
            f"{top_chunks} | {row['best_distance']:.4f} | {row['question']} |"
        )


if __name__ == "__main__":
    main()
