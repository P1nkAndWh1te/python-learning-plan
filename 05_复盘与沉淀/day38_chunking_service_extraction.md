# Day 38：抽离文档切分服务

**日期**：2026年7月20日  
**项目**：DocuAsk v2  
**目标**：把 chunking 从 Streamlit 页面逻辑中抽离

---

## 1. 本次完成

新增：

```text
04_成果输出/rag-qa-system/backend/services/
04_成果输出/rag-qa-system/backend/services/chunking.py
```

抽离函数：

```text
split_text_into_chunks
split_markdown_sections
split_by_character_count
```

Streamlit `app.py` 现在通过以下方式复用：

```python
from backend.services.chunking import split_text_into_chunks
```

---

## 2. 为什么先抽离 chunking

chunking 是 RAG 链路中风险较低、边界清晰的模块。

先抽离它可以验证：

- 后端 services 包结构是否合理。
- Streamlit 是否能继续复用后端 service。
- 后续 FastAPI 是否可以逐步接入同一套逻辑。

---

## 3. 验证结果

使用 FAQ 文档验证：

```text
02_资料与素材/day10_dify_knowledge/python_learning_faq.md
```

结果：

```text
Chunks: 6
```

说明抽离后切分结果保持一致。

---

## 4. 当前没有做什么

本次没有：

- 迁移 embedding。
- 迁移 Chroma 检索。
- 迁移 DeepSeek 生成。
- 新增 FastAPI upload endpoint。
- 改动 Streamlit UI。

---

## 5. 下一步

下一步建议抽离 embedding service：

```text
backend/services/embeddings.py
```

目标是统一管理：

- Teaching keyword embedding。
- BGE Chinese embedding。
- embedding mode 常量。
- collection name 映射。

