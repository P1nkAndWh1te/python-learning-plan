from __future__ import annotations

import sys
from pathlib import Path


sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
APP_ROOT = PROJECT_ROOT / "04_成果输出" / "rag-qa-system"
FAQ_PATH = (
    PROJECT_ROOT
    / "02_资料与素材"
    / "day10_dify_knowledge"
    / "python_learning_faq.md"
)

sys.path.insert(0, str(APP_ROOT))

from backend.services.chunking import split_text_into_chunks  # noqa: E402


def main() -> None:
    text = FAQ_PATH.read_text(encoding="utf-8")
    chunks = split_text_into_chunks(text, chunk_size=350, chunk_overlap=50)

    print("Day38 chunking service check")
    print(f"FAQ: {FAQ_PATH}")
    print(f"Chunks: {len(chunks)}")
    for index, chunk in enumerate(chunks, start=1):
        preview = chunk.replace("\n", " ")[:80]
        print(f"- Chunk {index}: {len(chunk)} chars | {preview}")

    if len(chunks) != 6:
        raise AssertionError(f"Expected 6 chunks, got {len(chunks)}")


if __name__ == "__main__":
    main()

