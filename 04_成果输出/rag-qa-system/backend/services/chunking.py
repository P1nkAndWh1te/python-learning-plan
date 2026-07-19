def split_text_into_chunks(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    cleaned_text = text.strip()
    if not cleaned_text:
        return []

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be greater than or equal to 0 and less than chunk_size"
        )

    markdown_sections = split_markdown_sections(cleaned_text)
    if len(markdown_sections) > 1:
        chunks = []
        for section in markdown_sections:
            if len(section) <= chunk_size:
                chunks.append(section)
            else:
                chunks.extend(split_by_character_count(section, chunk_size, chunk_overlap))
        return chunks

    return split_by_character_count(cleaned_text, chunk_size, chunk_overlap)


def split_markdown_sections(text: str) -> list[str]:
    lines = text.splitlines()
    sections = []
    current_lines = []

    for line in lines:
        if line.startswith("## ") and current_lines:
            sections.append("\n".join(current_lines).strip())
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines:
        sections.append("\n".join(current_lines).strip())

    return [section for section in sections if section]


def split_by_character_count(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])

        if end >= len(text):
            break

        start = end - chunk_overlap

    return chunks
