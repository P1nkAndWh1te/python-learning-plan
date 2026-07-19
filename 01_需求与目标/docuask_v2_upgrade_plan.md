# DocuAsk v2 升级计划

**日期**：2026年7月19日  
**当前项目**：RAG QA System / DocuAsk  
**目标**：从本地 RAG 原型升级为更工程化的 AI 应用系统

---

## 1. 当前项目状态

当前项目已经完成一个可运行的本地 RAG QA 原型。

当前链路：

```text
文档上传 -> 文档读取 -> 文档切分 -> embedding -> Chroma 检索 -> 上下文组装 -> DeepSeek 回答 -> 来源引用
```

当前已具备：

- Streamlit 页面。
- TXT / Markdown 文档上传。
- Markdown `##` 标题优先切分。
- 固定长度 chunk 切分。
- Teaching keyword embedding。
- BGE Chinese embedding。
- Chroma Top 3 检索。
- DeepSeek OpenAI-compatible LLM API。
- 来源 chunk 展示。
- 10 题固定检索评测。
- Top-1 hit 和 Top-k recall 指标。
- README、项目展示说明、截图材料和 Git 提交记录。

当前评测结果：

```text
Teaching keyword embedding: Top-1 60%, Top-k 100%
BGE Chinese embedding: Top-1 80%, Top-k 100%
```

当前截图材料：

```text
04_成果输出/rag-qa-system/screenshots/
```

当前最新提交：

```text
ffa4bb2 Add day 35 screenshot materials
```

---

## 2. 当前不能夸大的点

当前项目还不能写成：

- 支持 PDF。
- 生产级系统。
- 多用户系统。
- 持久化知识库。
- 大规模评测。
- 已接入 rerank。
- 使用 LlamaIndex 统一主链路。
- Chroma 持久化存储。
- 完整后端服务。

更准确的定位：

```text
一个本地 RAG QA 原型，已跑通文档上传、切分、检索、生成、来源引用和小规模固定问题评测。
```

---

## 3. 升级目标

将当前项目升级为：

```text
DocuAsk v2：具备前后端分层、持久化知识库和自动评测的本地文档 RAG 问答系统
```

目标不是堆技术名词，而是把项目从“完成作业”升级为“解决业务痛点”：

```text
解决本地文档问答中回答不可追溯、检索质量不可评估、服务不可复用的问题。
```

---

## 4. 推荐升级路线

### Step 1：FastAPI 后端服务

目标：

```text
把当前 Streamlit 单体逻辑拆出可复用后端接口。
```

计划接口：

```text
GET  /health
POST /documents/upload
POST /qa/ask
GET  /evaluation
```

预期收益：

- 从页面原型升级为后端服务。
- 后续可以接 Streamlit、React 或其他客户端。
- 便于写 pytest 和 E2E 测试。

### Step 2：Chroma 持久化

目标：

```text
使用 Chroma PersistentClient 持久化文档 chunk 和 embedding。
```

预期收益：

- 服务重启后知识库不丢失。
- 简历中可以准确写“持久化知识库”。
- 更接近真实 RAG 应用。

### Step 3：自动化评测

目标：

```text
把 10 题固定评测升级为 pytest 可执行测试。
```

计划指标：

```text
BGE Top-1 hit >= 80%
BGE Top-k recall >= 100%
```

预期收益：

- 每次改 chunk、embedding 或检索逻辑后能自动回归。
- 简历中可以写“设计 E2E 检索评测闭环”。

### Step 4：Hybrid Search

目标：

```text
BGE vector search + BM25 keyword search + RRF fusion
```

预期收益：

- 提升检索鲁棒性。
- 对关键词型问题和语义型问题都更稳。
- 项目从单一向量检索升级为混合检索。

### Step 5：工程化整理

目标：

```text
补充接口文档、架构说明、运行脚本和最终项目介绍。
```

可选内容：

- Docker Compose。
- 系统架构图。
- API 示例。
- 错误处理说明。
- 简历项目描述。

---

## 5. 升级后的简历用语原则

后续项目介绍要使用更强的动作词，但必须有证据支撑。

推荐动作词：

```text
设计
重构
优化
提升
解决
排查
构建
验证
沉淀
拆分
封装
接入
对比
评估
```

避免只写：

```text
使用
实现
编写
完成
```

升级完成后，项目描述应尽量写成：

```text
设计了 XX 方案，解决了 XX 问题
重构了 XX 模块，提升了 XX 能力
构建了 XX 评测闭环，验证了 XX 效果
排查并修复了 XX 问题，避免了 XX 风险
```

---

## 6. 升级完成后的目标项目描述方向

升级后再生成最终简历文案。

目标风格：

```text
DocuAsk｜本地文档 RAG 问答系统
技术栈：Python / FastAPI / Streamlit / Chroma / BGE Embedding / BM25 / RRF / OpenAI-compatible LLM API / pytest
```

预期亮点方向：

- 设计前后端分层 RAG 架构。
- 重构 Streamlit 单体逻辑为 FastAPI 后端服务。
- 构建 Chroma 持久化知识库。
- 接入 BGE 中文 embedding。
- 对比向量检索、关键词检索和混合检索。
- 构建 10 题 E2E 检索评测闭环。
- 用 Top-1 hit 和 Top-k recall 量化检索效果。
- 展示来源 chunk，提升回答可追溯性。

---

## 7. 当前下一步

从 Step 1 开始：

```text
新增 FastAPI 后端服务骨架
```

验收标准：

- `GET /health` 可用。
- RAG 核心逻辑开始从 Streamlit 中拆出。
- 不破坏现有 Streamlit 页面。
- 有独立运行说明和测试记录。

