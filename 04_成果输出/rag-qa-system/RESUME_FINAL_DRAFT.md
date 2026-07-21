# DocuAsk 简历最终草稿

本文档是基于 `PROJECT_RESUME.md` 压缩后的正式简历候选版本。当前版本适合继续逐句打磨，不包含未完成能力。

## 推荐版本

**DocuAsk｜本地文档 RAG 问答系统**  2026.07  
**技术栈：Python / FastAPI / Streamlit / Chroma / BGE / BM25 / RRF / DeepSeek API / pytest**

- 面向本地知识文档问答场景，设计并重构 RAG 问答链路，支持 `.txt/.md` 文件上传、文档切分、Chroma 向量入库、检索问答、LLM 回答生成和来源引用。
- 拆分 `chunking`、`embedding`、`retrieval`、`generation`、`evaluation` 等核心模块，并新增 FastAPI 接口，覆盖 `/documents`、`/documents/upload`、`/qa`、`/answer`、`/evaluation`，提升 RAG 逻辑复用性和可测试性。
- 构建 Chroma 本地持久化知识库，按 embedding 模式、schema version 和文档 hash 管理 collection，解决索引重启丢失、不同 embedding 维度混用的问题。
- 设计 vector、BM25、RRF 三种检索模式，并支持自定义 evaluation cases；使用 Top-1 hit / Top-k recall 量化检索效果，当前小样本评测中 RRF Top-1 hit 90%、Top-k recall 100%。
- 使用 pytest 覆盖文档入库、文件上传、检索问答、回答生成、检索评测和异常分支，沉淀 API 文档、架构说明和验证脚本，提升项目可复现性。

## 更短版本

**DocuAsk｜本地文档 RAG 问答系统**  2026.07  
**技术栈：Python / FastAPI / Streamlit / Chroma / BGE / BM25 / RRF / DeepSeek API / pytest**

- 设计并重构本地文档 RAG 问答链路，支持 `.txt/.md` 上传、文档切分、Chroma 向量入库、检索问答、LLM 回答生成和来源引用。
- 拆分 RAG 核心模块并新增 FastAPI 后端接口，覆盖文档入库、文件上传、检索、回答生成和评测链路，提升逻辑复用性和可测试性。
- 构建 vector、BM25、RRF 三种检索模式和自定义 evaluation cases，用 Top-1 hit / Top-k recall 评估检索效果；当前小样本评测 RRF Top-1 hit 90%、Top-k recall 100%。
- 使用 pytest 覆盖核心接口和异常分支，沉淀 API 文档、架构说明和验证脚本，提升项目可复现性。

## 证据对应

| 简历表述 | 证据 |
|---|---|
| 文件上传 | `POST /documents/upload`、Day52 验证脚本 |
| 检索问答 | `POST /qa`、`retrieval.py` |
| 回答生成 | `POST /answer`、`generation.py` |
| Chroma 持久化 | `retrieval.py`、`backend/storage/chroma_db_v2/` |
| BM25 / RRF | `bm25.py`、`rrf.py` |
| 检索评测 | `POST /evaluation`、Day49 / Day53 验证脚本 |
| 自动化测试 | `tests/test_backend_api.py`、`tests/test_retrieval_metrics.py` |

## 不能写进简历的说法

- 生产级系统。
- 多用户权限系统。
- 支持 PDF / Word。
- 已接入 rerank。
- 大规模 benchmark。
- 压测或线上稳定性验证。
