# Day 39：抽离 Embedding Service

**日期**：2026年7月20日  
**项目**：DocuAsk v2  
**目标**：把 embedding 逻辑从 Streamlit 页面中抽离

---

## 1. 本次完成

新增：

```text
04_成果输出/rag-qa-system/backend/services/embeddings.py
```

抽离内容：

```text
CONCEPTS
BGE_MODEL_NAME
KEYWORD_EMBEDDING_MODE
BGE_EMBEDDING_MODE
COLLECTION_NAMES
embed_text
embed_text_with_bge
embed_for_mode
get_matched_concepts
```

Streamlit `app.py` 现在导入并复用 embedding service。

---

## 2. 设计取舍

原来的 BGE 模型缓存使用 `st.cache_resource`。

抽离到 service 后，不能让 service 依赖 Streamlit，否则 FastAPI 后端也会间接依赖页面框架。

因此改为：

```text
functools.lru_cache(maxsize=1)
```

这样 embedding service 可以被 Streamlit 和 FastAPI 共同复用。

---

## 3. 验证结果

独立验证：

```text
Keyword embedding dimension: 12
BGE embedding dimension: 512
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

- 迁移 Chroma 检索。
- 迁移 DeepSeek 生成。
- 新增 FastAPI endpoint。
- 改动 UI。
- 改动评测问题。

---

## 5. 下一步

下一步建议抽离 vector store / retrieval service：

```text
backend/services/vector_store.py
backend/services/retrieval.py
```

目标是让 Chroma collection 构建和 Top-k 检索从 Streamlit 中拆出来。

