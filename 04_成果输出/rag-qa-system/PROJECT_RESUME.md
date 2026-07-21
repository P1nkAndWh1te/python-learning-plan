# DocuAsk 项目介绍与简历版本

本文档用于整理 DocuAsk 当前可用于简历和面试讲解的项目材料。所有表述只基于当前已经完成并验证的能力。

## 1. 项目一句话

DocuAsk 是一个面向本地 `.txt/.md` 文档的 RAG 问答系统，支持文档上传、向量入库、混合检索、LLM 回答生成、来源引用和检索效果评测。

## 2. 简历短版

**DocuAsk｜本地文档 RAG 问答系统**  
**技术栈：Python / FastAPI / Streamlit / Chroma / BGE Embedding / BM25 / RRF / OpenAI-compatible LLM API / pytest**

面向本地文档知识问答场景，设计并重构了一套可复用的 RAG 问答链路，支持 `.txt/.md` 文件上传、文档切分、向量入库、检索问答、LLM 回答生成、来源引用和检索评测，提升回答可追溯性和检索质量可验证性。

- 重构 Streamlit 单体逻辑，拆分 `chunking`、`embedding`、`retrieval`、`generation`、`evaluation` 等 service，并新增 FastAPI 后端接口，覆盖文档入库、文件上传、检索问答、回答生成和评测链路。
- 构建 Chroma 本地持久化知识库，按 embedding 模式和文档 hash 管理 collection，解决服务重启后索引不可复用、不同 embedding 维度混用风险。
- 设计 vector、BM25、RRF 三种检索模式，对比语义检索、关键词检索和融合排序效果；在当前 FAQ 10 题评测中，RRF Top-1 hit 达到 90%，Top-k recall 达到 100%。
- 构建可配置 evaluation cases 的检索评测接口，支持默认 FAQ 10 题和自定义多文档小样本评测，用 Top-1 hit、Top-k recall 量化召回质量。
- 使用 pytest 覆盖 `/documents`、`/documents/upload`、`/qa`、`/answer`、`/evaluation` 及错误分支，沉淀接口文档、架构说明和验证脚本，提升项目可复现性。

## 3. 简历更短版

**DocuAsk｜本地文档 RAG 问答系统**  
**技术栈：Python / FastAPI / Streamlit / Chroma / BGE / BM25 / RRF / DeepSeek API / pytest**

- 设计并重构本地文档 RAG 问答链路，支持 `.txt/.md` 文件上传、文档切分、Chroma 向量入库、检索问答、LLM 回答生成和来源引用。
- 拆分 RAG 核心 service 并新增 FastAPI 后端接口，覆盖 `/documents`、`/documents/upload`、`/qa`、`/answer`、`/evaluation`。
- 构建 vector、BM25、RRF 三种检索模式和可配置 evaluation cases，用 Top-1 hit / Top-k recall 评估检索效果；当前小样本评测 RRF Top-1 hit 90%、Top-k recall 100%。
- 使用 pytest 覆盖核心接口和错误分支，沉淀 API 文档、架构说明和验证脚本，提升系统可测试性和可复现性。

## 4. 面试讲解版

### 背景

我做这个项目的目标不是简单调用大模型，而是解决本地文档问答里三个常见问题：

- LLM 容易脱离资料回答，来源不可追溯。
- 检索效果很难判断，只看最终回答不够。
- 早期 Streamlit 单体逻辑不便复用和测试。

所以我把项目从一个页面原型升级成了“Streamlit 页面 + FastAPI 后端 + RAG services + Chroma 持久化 + 检索评测”的结构。

### 核心链路

当前主链路是：

```text
文件上传 -> 文档解码 -> chunk 切分 -> embedding -> Chroma 持久化
-> vector / BM25 / RRF 检索 -> context 组装 -> DeepSeek answer -> sources
```

后端接口包括：

```text
GET  /health
POST /documents
POST /documents/upload
POST /qa
POST /answer
POST /evaluation
```

### 我重点做了什么

我先把切分、embedding、检索、生成、评测从页面里拆出来，避免业务逻辑都堆在 `app.py`。然后用 FastAPI 把这些能力暴露成接口。

检索层面，我没有只保留向量检索，而是补了 BM25 和 RRF。原因是本地知识问答里有些问题更偏语义，有些问题更偏关键词，比如接口名、环境变量、配置项。RRF 可以融合 vector 和 BM25 的排序，让两类问题的召回更稳定。

评测层面，我没有只靠主观看回答，而是做了 evaluation endpoint。它支持默认 FAQ 10 题，也支持自定义 evaluation cases。指标用 Top-1 hit 和 Top-k recall：前者看第一名是否正确，后者看正确 chunk 是否进入候选集合。

### 当前结果

当前小样本评测包括 2 份文档、13 个问题。

FAQ 10 题中：

```text
vector Top-1 hit: 60%, Top-k recall: 100%
bm25  Top-1 hit: 80%, Top-k recall: 100%
rrf   Top-1 hit: 90%, Top-k recall: 100%
```

新增 DocuAsk backend FAQ 3 题中：

```text
bm25 Top-1 hit: 100%, Top-k recall: 100%
```

这个结果说明当前小样本文档里，融合检索对 Top-1 排序有提升。但我不会把它说成大规模 benchmark，因为目前评测规模还比较小。

## 5. 可被追问的问题

### 为什么保留 Teaching keyword embedding？

它不是生产级 embedding，但适合做教学 baseline。通过它能解释向量维度、关键词命中和余弦相似度的关系。真实语义检索则使用 BGE Chinese embedding。

### 为什么要分 collection？

不同 embedding 维度不能混到同一个 Chroma collection。Teaching keyword embedding 和 BGE embedding 维度不同，所以必须分开存储。当前 collection 名称还包含 schema version 和文档 hash，避免历史索引冲突，并复用同一文档的 collection。

### 为什么测试不直接调用 DeepSeek？

真实 LLM API 依赖 API Key、网络、额度和模型服务状态，不适合放进稳定自动化测试。pytest 主要验证本地可控链路：文档入库、检索模式、评测指标和错误分支。真实 answer 调用通过手动脚本验证。

### 为什么做 RRF？

向量检索更适合语义相近问题，BM25 更适合关键词和专有名词问题。RRF 通过融合两个排序结果，让不同类型问题都更容易召回正确 chunk。

## 6. 不能夸大的边界

当前不能写成：

- 生产级系统。
- 多用户或权限系统。
- 支持 PDF / Word 解析。
- 已接入 rerank。
- 大规模 benchmark 或压测。
- 完整线上 LLM 稳定性验证。

当前准确边界：

```text
本地文档 RAG 原型 + FastAPI 后端化 + Chroma 持久化 + 三种检索模式 + 小样本评测 + pytest 回归。
```

## 7. 证据索引

| 证据 | 路径 |
|---|---|
| API 文档 | `04_成果输出/rag-qa-system/API.md` |
| 架构说明 | `04_成果输出/rag-qa-system/ARCHITECTURE.md` |
| 项目展示说明 | `04_成果输出/rag-qa-system/PROJECT_BRIEF.md` |
| 后端入口 | `04_成果输出/rag-qa-system/backend/app.py` |
| RAG services | `04_成果输出/rag-qa-system/backend/services/` |
| 自动化测试 | `04_成果输出/rag-qa-system/tests/` |
| 多文档评测脚本 | `03_执行过程/day53_multi_document_evaluation_check/` |
| 截图材料 | `04_成果输出/rag-qa-system/screenshots/` |
