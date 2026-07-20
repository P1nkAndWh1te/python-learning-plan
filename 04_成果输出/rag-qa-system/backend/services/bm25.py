import math
import re
from collections import Counter


TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9_]+|[\u4e00-\u9fff]")


def tokenize(text: str) -> list[str]:
    raw_tokens = TOKEN_PATTERN.findall(text.lower())
    tokens = []
    chinese_buffer = []

    for token in raw_tokens:
        if re.fullmatch(r"[\u4e00-\u9fff]", token):
            chinese_buffer.append(token)
            continue

        tokens.extend(build_chinese_terms(chinese_buffer))
        chinese_buffer = []
        tokens.append(token)

    tokens.extend(build_chinese_terms(chinese_buffer))
    return tokens


def build_chinese_terms(characters: list[str]) -> list[str]:
    if not characters:
        return []

    terms = characters[:]
    if len(characters) == 1:
        return terms

    terms.extend(
        "".join(characters[index:index + 2])
        for index in range(len(characters) - 1)
    )
    return terms


def retrieve_relevant_chunks_bm25(
    question: str,
    chunks: list[str],
    top_k: int,
    k1: float = 1.5,
    b: float = 0.75,
) -> list[dict]:
    if not question.strip() or not chunks:
        return []

    query_terms = tokenize(question)
    if not query_terms:
        return []

    documents = [tokenize(chunk) for chunk in chunks]
    document_lengths = [len(document) for document in documents]
    average_document_length = (
        sum(document_lengths) / len(document_lengths)
        if document_lengths
        else 0.0
    )
    document_frequency = calculate_document_frequency(documents)

    results = []
    for index, document_terms in enumerate(documents, start=1):
        score = calculate_bm25_score(
            query_terms=query_terms,
            document_terms=document_terms,
            document_count=len(documents),
            document_frequency=document_frequency,
            document_length=document_lengths[index - 1],
            average_document_length=average_document_length,
            k1=k1,
            b=b,
        )
        if score > 0:
            results.append(
                {
                    "text": chunks[index - 1],
                    "chunk_index": index,
                    "score": score,
                }
            )

    results.sort(key=lambda item: (-item["score"], item["chunk_index"]))
    return results[:top_k]


def calculate_document_frequency(documents: list[list[str]]) -> Counter:
    document_frequency = Counter()

    for document_terms in documents:
        document_frequency.update(set(document_terms))

    return document_frequency


def calculate_bm25_score(
    query_terms: list[str],
    document_terms: list[str],
    document_count: int,
    document_frequency: Counter,
    document_length: int,
    average_document_length: float,
    k1: float,
    b: float,
) -> float:
    term_frequency = Counter(document_terms)
    score = 0.0

    for term in query_terms:
        if term_frequency[term] == 0:
            continue

        idf = math.log(
            1
            + (
                document_count
                - document_frequency[term]
                + 0.5
            )
            / (document_frequency[term] + 0.5)
        )
        denominator = term_frequency[term] + k1 * (
            1
            - b
            + b * document_length / average_document_length
        )
        score += idf * (
            term_frequency[term] * (k1 + 1)
        ) / denominator

    return score
