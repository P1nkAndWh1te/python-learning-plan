import math
import sys


sys.stdout.reconfigure(encoding="utf-8")


CONCEPTS = {
    "python": ["python", "脚本", "程序"],
    "api": ["api", "接口", "调用", "请求"],
    "git": ["git", "提交", "版本", "仓库"],
    "rag": ["rag", "检索", "文档", "知识库"],
    "data": ["数据", "csv", "表格", "pandas"],
}


DOCUMENTS = [
    {
        "id": "doc_api",
        "text": "Python 可以使用 requests 或 SDK 调用 API，获取远程服务的数据。",
    },
    {
        "id": "doc_git",
        "text": "Git 用来记录代码版本，每次 commit 都是一份历史记录。",
    },
    {
        "id": "doc_rag",
        "text": "RAG 会先从知识库检索相关文档片段，再交给大模型生成回答。",
    },
    {
        "id": "doc_data",
        "text": "Pandas 可以读取 CSV 表格，并对数据进行筛选和统计。",
    },
    {
        "id": "doc_python_file",
        "text": "Python 可以读取文件，并把内容保存成 JSON 或 CSV。",

    },
]


def embed(text):
    text = text.lower()
    vector = []

    for keywords in CONCEPTS.values():
        score = 0
        for keyword in keywords:
            if keyword.lower() in text:
                score += 1
        vector.append(float(score))

    return vector


def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot / (norm_a * norm_b)


def main():
    query = "Python 怎么读取文件并保存数据？"
    query_vector = embed(query)

    print("Concept order:", list(CONCEPTS.keys()))
    print("Query:", query)
    print("Query vector:", query_vector)
    print()

    results = []
    for doc in DOCUMENTS:
        doc_vector = embed(doc["text"])
        score = cosine_similarity(query_vector, doc_vector)
        results.append((score, doc, doc_vector))

    results.sort(reverse=True, key=lambda item: item[0])

    for rank, (score, doc, doc_vector) in enumerate(results, start=1):
        print(f"Rank {rank}")
        print(f"ID: {doc['id']}")
        print(f"Score: {score:.4f}")
        print(f"Vector: {doc_vector}")
        print(f"Text: {doc['text']}")
        print()


if __name__ == "__main__":
    main()
