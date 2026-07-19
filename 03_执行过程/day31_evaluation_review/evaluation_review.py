from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import chromadb
from chromadb.api.types import Documents, Embeddings
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from sentence_transformers import SentenceTransformer


sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
APP_PATH = PROJECT_ROOT / "04_成果输出" / "rag-qa-system" / "app.py"
FAQ_PATH = (
    PROJECT_ROOT
    / "02_资料与素材"
    / "day10_dify_knowledge"
    / "python_learning_faq.md"
)
BGE_MODEL_NAME = "BAAI/bge-small-zh-v1.5"


class BgeEmbeddingFunction:
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)

    def name(self) -> str:
        return "bge-small-zh-v1.5"

    def __call__(self, input: Documents) -> Embeddings:
        return self._encode(input)

    def embed_documents(self, input: Documents) -> Embeddings:
        return self._encode(input)

    def embed_query(self, input: Documents) -> Embeddings:
        return self._encode(input)

    def _encode(self, input: Documents) -> Embeddings:
        embeddings = self.model.encode(
            list(input),
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return embeddings.tolist()


def load_rag_app_module():
    spec = importlib.util.spec_from_file_location("rag_app", APP_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load app module from {APP_PATH}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_collection(chunks: list[str], embedding_function):
    client = chromadb.EphemeralClient()
    collection = client.get_or_create_collection(
        name=f"day31-{embedding_function.name()}",
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


def evaluate_embedding(collection, evaluation_cases: list[dict], top_k: int) -> list[dict]:
    rows = []
    result_count = min(top_k, collection.count())

    for case in evaluation_cases:
        result = collection.query(
            query_texts=[case["question"]],
            n_results=result_count,
            include=["metadatas", "distances"],
        )
        actual_chunks = [
            metadata["chunk_index"]
            for metadata in result["metadatas"][0]
        ]
        expected = case["expected_top_chunk"]

        rows.append(
            {
                "question": case["question"],
                "expected": expected,
                "actual_top": actual_chunks[0],
                "top_chunks": actual_chunks,
                "best_distance": result["distances"][0][0],
                "strict_hit": actual_chunks[0] == expected,
                "top_k_hit": expected in actual_chunks,
            }
        )

    return rows


def summarize(name: str, rows: list[dict]) -> dict:
    total = len(rows)
    strict_hits = sum(1 for row in rows if row["strict_hit"])
    top_k_hits = sum(1 for row in rows if row["top_k_hit"])
    return {
        "name": name,
        "strict_hit_rate": strict_hits / total * 100,
        "top_k_hit_rate": top_k_hits / total * 100,
        "strict_hits": strict_hits,
        "top_k_hits": top_k_hits,
        "total": total,
    }


def print_summary(summaries: list[dict]) -> None:
    print("| Method | Strict top-1 | Top-k recall |")
    print("|---|---:|---:|")
    for item in summaries:
        print(
            f"| {item['name']} | "
            f"{item['strict_hits']}/{item['total']} ({item['strict_hit_rate']:.1f}%) | "
            f"{item['top_k_hits']}/{item['total']} ({item['top_k_hit_rate']:.1f}%) |"
        )


def print_failure_review(name: str, rows: list[dict]) -> None:
    print()
    print(f"{name} strict top-1 failures:")
    for row in rows:
        if row["strict_hit"]:
            continue
        top_chunks = ", ".join(f"Chunk {chunk}" for chunk in row["top_chunks"])
        print(
            f"- {row['question']} | expected Chunk {row['expected']} | "
            f"top: Chunk {row['actual_top']} | top-k: {top_chunks}"
        )


def main() -> None:
    rag_app = load_rag_app_module()
    text = FAQ_PATH.read_text(encoding="utf-8")
    chunks = rag_app.split_text_into_chunks(
        text,
        chunk_size=rag_app.DEFAULT_CHUNK_SIZE,
        chunk_overlap=rag_app.DEFAULT_CHUNK_OVERLAP,
    )

    keyword_rows = rag_app.evaluate_retrieval(
        rag_app.EVALUATION_CASES,
        chunks,
        top_k=rag_app.TOP_K,
    )
    keyword_review_rows = [
        {
            "question": row["question"],
            "expected": int(row["expected_top_chunk"].replace("Chunk ", "")),
            "actual_top": int(row["top_chunks"].split(", ")[0].replace("Chunk ", "")),
            "top_chunks": [
                int(chunk.replace("Chunk ", ""))
                for chunk in row["top_chunks"].split(", ")
            ],
            "strict_hit": row["hit"],
            "top_k_hit": row["top_k_hit"],
        }
        for row in keyword_rows
    ]

    default_collection = build_collection(chunks, DefaultEmbeddingFunction())
    bge_collection = build_collection(chunks, BgeEmbeddingFunction(BGE_MODEL_NAME))

    default_rows = evaluate_embedding(default_collection, rag_app.EVALUATION_CASES, rag_app.TOP_K)
    bge_rows = evaluate_embedding(bge_collection, rag_app.EVALUATION_CASES, rag_app.TOP_K)

    print("Day31 evaluation review")
    print(f"FAQ: {FAQ_PATH}")
    print(f"Chunks: {len(chunks)}")
    print(f"Top k: {rag_app.TOP_K}")
    print()

    print_summary(
        [
            summarize("Teaching keyword embedding", keyword_review_rows),
            summarize("Chroma default embedding", default_rows),
            summarize("BGE Chinese embedding", bge_rows),
        ]
    )
    print_failure_review("Teaching keyword embedding", keyword_review_rows)
    print_failure_review("Chroma default embedding", default_rows)
    print_failure_review("BGE Chinese embedding", bge_rows)


if __name__ == "__main__":
    main()

