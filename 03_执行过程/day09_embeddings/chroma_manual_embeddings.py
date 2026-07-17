from manual_similarity import DOCUMENTS, embed


def main():
    try:
        import chromadb
    except ModuleNotFoundError:
        print("chromadb is not installed.")
        print("Install it with: python -m pip install chromadb")
        return

    client = chromadb.PersistentClient(path="03_执行过程/day09_embeddings/chroma_store")
    collection = client.get_or_create_collection(name="day09_manual_embeddings")

    ids = [doc["id"] for doc in DOCUMENTS]
    documents = [doc["text"] for doc in DOCUMENTS]
    embeddings = [embed(doc["text"]) for doc in DOCUMENTS]
    metadatas = [{"source": doc["id"]} for doc in DOCUMENTS]

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    query = "怎么让 Python 程序调用接口获取数据？"
    query_embedding = embed(query)

    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=2,
        include=["documents", "metadatas", "distances"],
    )

    print("Query:", query)
    print("Query embedding:", query_embedding)
    print()
    print("Top results from Chroma:")

    for index, doc in enumerate(result["documents"][0], start=1):
        metadata = result["metadatas"][0][index - 1]
        distance = result["distances"][0][index - 1]
        print(f"Rank {index}")
        print(f"Distance: {distance:.4f}")
        print(f"Metadata: {metadata}")
        print(f"Document: {doc}")
        print()


if __name__ == "__main__":
    main()
