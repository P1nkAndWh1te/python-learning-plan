# Day 40：抽离 Retrieval Service

**日期**：2026年7月20日  
**项目**：DocuAsk v2  
**目标**：把 Chroma 检索逻辑从 Streamlit 页面中抽离

---

## 1. 本次完成

新增：

```text
04_成果输出/rag-qa-system/backend/services/retrieval.py
```

抽离内容：

```text
build_chunk_collection
retrieve_relevant_chunks
format_retrieved_context
```

Streamlit `app.py` 现在不再直接 import `chromadb`，而是调用 retrieval service 完成检索。

---

## 2. 设计取舍

本次仍然保留：

```text
chromadb.EphemeralClient()
```

原因是今天的目标是模块边界抽离，而不是改存储行为。

如果同时切换成 `PersistentClient`，一旦指标变化，就很难判断问题来自“服务拆分”还是“持久化存储改造”。

---

## 3. 验证结果

独立验证：

```text
Query: RAG 的基本流程是什么？
Top chunk: 6
```

10 题评测保持不变：

```text
Teaching keyword embedding: Top-1 60%, Top-k 100%
BGE Chinese embedding: Top-1 80%, Top-k 100%
```

说明抽离没有破坏现有检索效果。

---

## 4. 当前没有做什么

本次没有：

- 切换到 Chroma PersistentClient。
- 新增 FastAPI endpoint。
- 迁移 DeepSeek 生成。
- 改动 UI。
- 改动评测问题。

---

## 5. 下一步

下一步建议进入 Chroma 持久化改造：

```text
backend/storage/chroma_db/
chromadb.PersistentClient(path=...)
```

目标是让文档向量索引可以落盘保存，为后续 FastAPI endpoint 和测试用例打基础。
