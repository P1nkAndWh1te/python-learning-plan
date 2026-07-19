from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
APP_PATH = PROJECT_ROOT / "04_成果输出" / "rag-qa-system" / "app.py"
FAQ_PATH = (
    PROJECT_ROOT
    / "02_资料与素材"
    / "day10_dify_knowledge"
    / "python_learning_faq.md"
)


def load_rag_app_module():
    spec = importlib.util.spec_from_file_location("rag_app", APP_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load app module from {APP_PATH}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    rag_app = load_rag_app_module()
    text = FAQ_PATH.read_text(encoding="utf-8")
    chunks = rag_app.split_text_into_chunks(
        text,
        chunk_size=rag_app.DEFAULT_CHUNK_SIZE,
        chunk_overlap=rag_app.DEFAULT_CHUNK_OVERLAP,
    )

    print("Day33 app metric check")
    print(f"Chunks: {len(chunks)}")
    print()
    print("| Embedding mode | Top-1 hit | Top-k recall |")
    print("|---|---:|---:|")

    for embedding_mode in (
        rag_app.KEYWORD_EMBEDDING_MODE,
        rag_app.BGE_EMBEDDING_MODE,
    ):
        rows = rag_app.evaluate_retrieval(
            rag_app.EVALUATION_CASES,
            chunks,
            top_k=rag_app.TOP_K,
            embedding_mode=embedding_mode,
        )
        hit_rate = rag_app.calculate_hit_rate(rows)
        top_k_hit_rate = rag_app.calculate_top_k_hit_rate(rows)
        print(
            f"| {embedding_mode} | {hit_rate:.0%} | {top_k_hit_rate:.0%} |"
        )


if __name__ == "__main__":
    main()

