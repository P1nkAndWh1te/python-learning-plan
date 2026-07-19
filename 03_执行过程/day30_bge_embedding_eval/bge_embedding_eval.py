from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import chromadb
from chromadb.api.types import Documents, Embeddings
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
MODEL_NAME = "BAAI/bge-small-zh-v1.5"
KEYWORD_BASELINE_HIT_RATE = 70.0
CHROMA_DEFAULT_HIT_RATE = 40.0


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


def build_collection(chunks: list[str]):
    client = chromadb.EphemeralClient()
    embedding_function = BgeEmbeddingFunction(MODEL_NAME)
    collection = client.get_or_create_collection(
        name="day30-bge-embedding-eval",
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


def print_rows(rows: list[dict]) -> None:
    print("| # | Hit | Expected | Actual top | Top chunks | Best distance | Question |")
    print("|---|---|---:|---:|---|---:|---|")
    for index, row in enumerate(rows, start=1):
        hit_mark = "yes" if row["hit"] else "no"
        top_chunks = ", ".join(f"Chunk {chunk}" for chunk in row["top_chunks"])
        print(
            f"| {index} | {hit_mark} | {row['expected']} | {row['actual_top']} | "
            f"{top_chunks} | {row['best_distance']:.4f} | {row['question']} |"
        )


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

    print("Day30 BGE Chinese embedding evaluation")
    print(f"FAQ: {FAQ_PATH}")
    print(f"Chunks: {len(chunks)}")
    print(f"Embedding: {MODEL_NAME}")
    print(f"Teaching keyword embedding hit rate: {KEYWORD_BASELINE_HIT_RATE:.1f}%")
    print(f"Chroma default embedding hit rate: {CHROMA_DEFAULT_HIT_RATE:.1f}%")
    print(f"BGE Chinese embedding hit rate: {hit_rate:.1f}%")
    print(f"Delta vs keyword baseline: {hit_rate - KEYWORD_BASELINE_HIT_RATE:+.1f}%")
    print(f"Delta vs Chroma default: {hit_rate - CHROMA_DEFAULT_HIT_RATE:+.1f}%")
    print()
    print_rows(rows)


if __name__ == "__main__":
    main()
