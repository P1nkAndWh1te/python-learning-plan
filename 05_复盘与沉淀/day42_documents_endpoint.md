# Day 42：Documents Endpoint

**日期**：2026年7月20日  
**项目**：DocuAsk v2  
**目标**：新增 FastAPI 文档写入接口

---

## 1. 本次完成

新增接口：

```text
POST /documents
```

请求体：

```json
{
  "text": "...",
  "embedding_mode": "Teaching keyword embedding",
  "chunk_size": 350,
  "chunk_overlap": 50
}
```

响应体：

```json
{
  "document_id": "...",
  "embedding_mode": "Teaching keyword embedding",
  "collection_name": "...",
  "chunk_count": 6,
  "stored_chunk_count": 6
}
```

---

## 2. 接口链路

`POST /documents` 当前做了四件事：

```text
接收文本 -> 切分 chunks -> 生成 embedding -> 写入 Chroma
```

它复用了前几天抽离出来的 service：

```text
backend/services/chunking.py
backend/services/embeddings.py
backend/services/retrieval.py
```

---

## 3. 设计取舍

今天没有做 multipart 文件上传。

原因是当前目标是先打通后端能力，不急着处理文件协议细节。

先用 JSON 文本接口有几个好处：

- 更容易测试。
- 更容易定位错误。
- 更适合后续 pytest。
- 不影响 Streamlit 当前页面。

---

## 4. 验证结果

独立验证：

```text
Status code: 200
Chunk count: 6
Stored chunk count: 6
Bad request status: 400
```

FastAPI 健康检查：

```json
{
  "status": "ok",
  "service": "docuask-api",
  "version": "0.1.0"
}
```

---

## 5. 下一步

下一步建议新增 QA endpoint：

```text
POST /qa
```

目标是让后端根据已上传文档和问题完成检索，并返回 retrieved chunks。

先只返回检索结果，不急着接 DeepSeek 生成。
