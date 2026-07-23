from io import BytesIO

from docx import Document
from pypdf import PdfReader


SUPPORTED_UPLOAD_EXTENSIONS = {".txt", ".md", ".pdf", ".docx"}


def parse_uploaded_document(raw_bytes: bytes, filename: str) -> tuple[str, str]:
    extension = get_file_extension(filename)

    if extension in {".txt", ".md"}:
        return decode_text_bytes(raw_bytes), "text"

    if extension == ".pdf":
        return extract_pdf_text(raw_bytes), "pdf"

    if extension == ".docx":
        return extract_docx_text(raw_bytes), "docx"

    raise ValueError("unsupported file type")


def get_file_extension(filename: str) -> str:
    if "." not in filename:
        return ""
    return "." + filename.rsplit(".", maxsplit=1)[-1].lower()


def decode_text_bytes(raw_bytes: bytes) -> str:
    for encoding in ("utf-8", "gbk"):
        try:
            return raw_bytes.decode(encoding)
        except UnicodeDecodeError:
            continue

    return raw_bytes.decode("utf-8", errors="replace")


def extract_pdf_text(raw_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(raw_bytes))
    page_texts = []

    for page in reader.pages:
        text = page.extract_text() or ""
        if text.strip():
            page_texts.append(text.strip())

    return "\n\n".join(page_texts)


def extract_docx_text(raw_bytes: bytes) -> str:
    document = Document(BytesIO(raw_bytes))
    paragraphs = [
        paragraph.text.strip()
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]
    return "\n\n".join(paragraphs)
