# DocuAsk API

本文档记录 DocuAsk 当前 FastAPI 后端已经验证的接口。

当前后端定位：为本地文档 RAG 问答系统提供可复用的文档入库、检索问答和检索评测能力。LLM 生成仍由 Streamlit 页面侧调用 DeepSeek OpenAI-compatible API，后端接口当前重点是检索链路和评测链路。

## 启动后端

在仓库根目录运行：

```powershell
python -m uvicorn backend.app:app --app-dir "04_成果输出/rag-qa-system" --host 127.0.0.1 --port 8000
```

健康检查地址：

```text
http://127.0.0.1:8000/health
```

## GET /health

用途：检查后端服务是否启动。

响应示例：

```json
{
  "status": "ok",
  "service": "docuask-api",
  "version": "0.1.0"
}
```

## POST /documents

用途：把文档文本切分成 chunks，计算 embedding，并写入本地 Chroma 持久化库。

请求体：

```json
{
  "text": "# Python 学习 FAQ\n\n## RAG 的基本流程是什么？\nRAG 会先检索资料，再让 LLM 根据资料回答。",
  "embedding_mode": "Teaching keyword embedding",
  "chunk_size": 350,
  "chunk_overlap": 50
}
```

响应字段：

```text
document_id
embedding_mode
collection_name
chunk_count
stored_chunk_count
```

说明：

- `collection_name` 是后续 `/qa` 查询的关键参数。
- 当前支持 `Teaching keyword embedding` 和 `BGE Chinese embedding`。
- Chroma 数据保存在 `04_成果输出/rag-qa-system/backend/storage/chroma_db_v2/`，该目录不提交到 Git。

## POST /qa

用途：基于已入库的 `collection_name` 检索相关 chunks，并返回可供 LLM 使用的上下文。

请求体：

```json
{
  "collection_name": "uploaded_document_chunks_keyword_v3_xxxxxxxxxxxx",
  "question": "RAG 的基本流程是什么？",
  "embedding_mode": "Teaching keyword embedding",
  "top_k": 3,
  "retrieval_mode": "vector"
}
```

`retrieval_mode` 支持：

```text
vector
bm25
rrf
```

响应字段：

```text
question
embedding_mode
collection_name
retrieval_mode
top_k
retrieved_chunks
context
```

`retrieved_chunks` 中的分数字段按模式不同而不同：

| Mode | Score field | 含义 |
|---|---|---|
| `vector` | `distance` | Chroma cosine distance，越低越相似 |
| `bm25` | `score` | BM25 关键词得分，越高越相关 |
| `rrf` | `rrf_score` | RRF 融合排序得分，越高排序越靠前 |

## POST /evaluation

用途：用固定 10 题评测当前文档切分和检索模式的召回效果。

请求体：

```json
{
  "text": "# Python 学习 FAQ\n\n## RAG 的基本流程是什么？\nRAG 会先检索资料，再让 LLM 根据资料回答。",
  "embedding_mode": "Teaching keyword embedding",
  "chunk_size": 350,
  "chunk_overlap": 50,
  "top_k": 3,
  "retrieval_mode": "rrf"
}
```

响应字段：

```text
embedding_mode
retrieval_mode
chunk_count
case_count
top_1_hit_rate
top_k_recall
rows
```

当前 FAQ 文档的 Day49 验证结果：

| Retrieval mode | Top-1 hit | Top-k recall |
|---|---:|---:|
| `vector` | 0.6 | 1.0 |
| `bm25` | 0.8 | 1.0 |
| `rrf` | 0.9 | 1.0 |

结论：在当前小型 FAQ 测试集上，RRF 的 Top-1 表现最好；但这只是 10 题固定评测结果，不能直接推断到所有文档场景。

## 错误处理

当前已覆盖的错误分支：

| 场景 | 状态码 |
|---|---:|
| 不支持的 embedding mode | 400 |
| 不支持的 retrieval mode | 400 |
| 空文档 | 400 |
| 文档没有可入库 chunk | 400 |
| 查询不存在的 collection | 404 |

## 自动化验证

运行：

```powershell
python -m pytest -q
```

当前测试覆盖：

```text
POST /documents
POST /qa: vector / bm25 / rrf
POST /evaluation: vector / bm25 / rrf
missing collection -> 404
unknown retrieval mode -> 400
Teaching keyword retrieval metrics
```
