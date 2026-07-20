import importlib.util
from pathlib import Path

from conftest import FAQ_PATH


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"


def load_rag_app_module():
    spec = importlib.util.spec_from_file_location("rag_app", APP_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load app module from {APP_PATH}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_teaching_keyword_retrieval_metrics_stay_stable():
    rag_app = load_rag_app_module()
    text = FAQ_PATH.read_text(encoding="utf-8")
    chunks = rag_app.split_text_into_chunks(
        text,
        chunk_size=rag_app.DEFAULT_CHUNK_SIZE,
        chunk_overlap=rag_app.DEFAULT_CHUNK_OVERLAP,
    )

    rows = rag_app.evaluate_retrieval(
        rag_app.EVALUATION_CASES,
        chunks,
        top_k=rag_app.TOP_K,
        embedding_mode=rag_app.KEYWORD_EMBEDDING_MODE,
    )

    assert len(chunks) == 6
    assert rag_app.calculate_hit_rate(rows) == 0.6
    assert rag_app.calculate_top_k_hit_rate(rows) == 1.0
