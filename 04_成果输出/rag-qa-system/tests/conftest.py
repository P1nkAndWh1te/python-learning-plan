import sys
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = APP_ROOT.parents[1]
FAQ_PATH = (
    PROJECT_ROOT
    / "02_资料与素材"
    / "day10_dify_knowledge"
    / "python_learning_faq.md"
)
DOCUASK_BACKEND_FAQ_PATH = (
    PROJECT_ROOT
    / "02_资料与素材"
    / "day53_multi_document_eval"
    / "docuask_backend_faq.md"
)

if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))
