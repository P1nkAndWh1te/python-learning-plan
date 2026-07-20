# Day 43：QA Endpoint

**日期**：2026年7月20日  
**项目**：DocuAsk v2  
**目标**：新增 FastAPI 检索问答接口

---

## 1. 本次完成

新增接口：

```text
POST /qa
```

请求体：

```json
{
  "collection_name": "...",
  "question": "RAG 的基本流程是什么？",
  "embedding_mode": "Teaching keyword embedding",
  "top_k": 3
}
```

响应体核心字段：

```text
question
embedding_mode
collection_name
top_k
retrieved_chunks
context
```

---

## 2. 接口链路

今天的后端链路是：

```text
POST /documents -> 写入 Chroma -> 返回 collection_name
POST /qa -> 根据 collection_name 查询 Chroma -> 返回 retrieved chunks
```

这说明 DocuAsk 已经从 Streamlit 单页面演示，逐步拆成了可复用的后端接口。

---

## 3. 设计取舍

今天没有接 DeepSeek 生成最终回答。

原因是 RAG 应该分层验证：

```text
文档写入 -> 检索召回 -> LLM 生成
```

如果今天同时接 LLM，一旦回答不对，就很难判断是检索问题还是生成问题。

---

## 4. 验证结果

独立验证：

```text
Document status: 200
QA status: 200
Top chunk: 6
Retrieved chunks: 3
Missing collection status: 404
```

原 10 题评估保持不变：

```text
Teaching keyword embedding: Top-1 60%, Top-k 100%
BGE Chinese embedding: Top-1 80%, Top-k 100%
```

---

## 5. 下一步

下一步建议新增 LLM answer endpoint 或在 `POST /qa` 中增加可选生成参数：

```text
generate: true
```

但建议继续分层做：先把 pytest 固定评估补上，再接生成会更稳。
