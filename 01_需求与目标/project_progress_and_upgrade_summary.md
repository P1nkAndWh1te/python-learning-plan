# DocuAsk 项目进展与升级计划总览

**日期**：2026年7月20日
**项目名称**：DocuAsk / RAG QA System  
**当前阶段**：DocuAsk v2 工程化升级已完成 FastAPI、文件上传、持久化、自动评测、BM25/RRF、API/架构文档、answer endpoint 和多文档小样本评测
**当前最新提交**：以 GitHub `main` 分支为准

---

## 1. 项目当前定位

DocuAsk 当前是一个本地文档 RAG 问答系统原型，用于验证完整 RAG 链路和基础工程化链路：

```text
文档上传 -> 文档读取 -> 文档切分 -> embedding -> Chroma 持久化 -> 检索模式选择 -> 上下文组装 -> LLM 回答 -> 来源引用 -> 检索评测
```

当前准确描述：

```text
一个本地 RAG QA 原型，已跑通文档上传、切分、持久化入库、检索、生成、来源引用、三种检索模式和小规模固定问题评测。
```

项目现阶段的价值：

- 证明 RAG 主链路可运行。
- 证明可以从本地文档中检索相关 chunk。
- 证明可以把检索上下文交给 LLM 生成回答。
- 证明可以展示来源 chunk，提高回答可追溯性。
- 证明可以用固定问题集评估检索质量。
- 证明可以用 FastAPI 暴露文档入库、检索问答和评测接口。
- 证明可以用 pytest 对核心接口和检索指标做自动回归。

---

## 2. 当前已完成能力

### 2.1 应用功能

当前 Streamlit 主应用已经支持：

- TXT / Markdown 文档上传。
- 上传文档内容读取和预览。
- Markdown `##` 标题优先切分。
- 普通文本固定长度切分。
- chunk 展示。
- Teaching keyword embedding。
- BGE Chinese embedding。
- Chroma Top 3 检索。
- Chroma 本地 PersistentClient 持久化。
- FastAPI `/health`、`/documents`、`/documents/upload`、`/qa`、`/answer`、`/evaluation`。
- `/qa` 和 `/evaluation` 支持 `vector`、`bm25`、`rrf` 三种模式。
- DeepSeek OpenAI-compatible LLM API 回答生成。
- 来源 chunk 展示。
- 检索上下文展示。
- 10 题固定检索评测。
- 自定义 evaluation cases。
- 多文档小样本评测。
- Top-1 hit 和 Top-k recall 指标展示。
- pytest 自动化测试。

### 2.2 当前技术栈

| Layer | 当前选择 |
|---|---|
| UI | Streamlit |
| Vector DB | Chroma |
| Backend API | FastAPI / Uvicorn |
| File upload | python-multipart |
| Teaching embedding | 手写关键词向量 |
| Real embedding | BAAI/bge-small-zh-v1.5 |
| Embedding runtime | Sentence Transformers |
| Retrieval | Vector / BM25 / RRF |
| LLM API | DeepSeek OpenAI-compatible API |
| SDK | OpenAI Python SDK |
| Evaluation | 10 题固定检索评测 |
| Test | pytest |

### 2.3 当前评测结果

测试文档：

```text
02_资料与素材/day10_dify_knowledge/python_learning_faq.md
```

当前评测结果：

| Embedding mode | Top-1 hit | Top-k recall |
|---|---:|---:|
| Teaching keyword embedding | 60% | 100% |
| BGE Chinese embedding | 80% | 100% |

Day49 三种检索模式对比：

| Retrieval mode | Top-1 hit | Top-k recall |
|---|---:|---:|
| vector | 60% | 100% |
| bm25 | 80% | 100% |
| rrf | 90% | 100% |

当前结论：

```text
BGE 中文 embedding 的 Top-1 排序效果更好。
两种模式都能在 Top 3 内召回正确 chunk。
在当前 10 题 FAQ 测试集上，RRF 的 Top-1 表现最好。
```

### 2.4 当前项目材料

当前已经整理好的材料：

- 根目录 README。
- RAG 应用 README。
- `PROJECT_BRIEF.md`。
- `PROJECT_RESUME.md`。
- `API.md`。
- `ARCHITECTURE.md`。
- `SCREENSHOT_CHECKLIST.md`。
- 页面截图材料。
- Day 14 到 Day 54 的学习记录和复盘记录。
- GitHub 提交记录。

截图目录：

```text
04_成果输出/rag-qa-system/screenshots/
```

截图包括：

| 文件 | 内容 |
|---|---|
| `01_app_upload.png` | 首页、上传区、问题输入和 embedding 模式 |
| `02_chunks.png` | 文档上传信息和 chunk 切分结果 |
| `03_retrieval_metrics.png` | Teaching keyword embedding 检索评测 |
| `04_bge_metrics.png` | BGE Chinese embedding 检索评测 |
| `05_answer_context.png` | 问题、检索说明和上下文 |
| `06_answer_sources.png` | Sources 和 Final answer |

---

## 3. 当前限制与风险

当前不能在简历或项目介绍中夸大为：

- 生产级系统。
- 多用户系统。
- 支持 PDF。
- 已接入 rerank。
- 已完成大规模评测。
- 已完成生产级大规模 LLM 后端服务。
- 使用 LlamaIndex 统一主链路。
- 完整生产级 Hybrid Search。

当前真实限制：

- FastAPI 后端已支持 `/answer`，但真实 LLM 调用仍依赖 API Key、网络、额度和模型服务状态。
- Chroma 持久化目录是本地运行数据，不提交到 GitHub。
- 当前评测集是 2 份文档、13 个问题的小样本，规模仍然较小。
- 当前已做 BM25 / RRF baseline，但未做 rerank。
- 当前截图和 README 能展示项目，后续还可以补更真实的多文档材料。

---

## 4. 为什么要升级

当前项目已经能证明 RAG 主链路，但如果用于 AI 应用开发实习展示，还缺少工程化深度。

升级目标不是堆技术名词，而是解决这些实际问题：

| 当前问题 | 升级目标 |
|---|---|
| Streamlit 单体逻辑难复用 | 拆出 FastAPI 后端服务 |
| 文档向量不持久化 | 使用 Chroma PersistentClient |
| 评测依赖手动运行 | 引入 pytest E2E 自动回归 |
| 单一向量检索鲁棒性有限 | 加入 BM25 + RRF Hybrid Search |
| 项目描述偏原型 | 沉淀架构说明、接口说明和结果型项目介绍 |

升级后的目标定位：

```text
DocuAsk v2：具备前后端分层、持久化知识库和自动评测的本地文档 RAG 问答系统。
```

---

## 5. 后续升级详细计划

### Step 1：FastAPI 后端服务骨架

目标：

```text
把当前 Streamlit 单体逻辑拆出可复用后端接口。
```

计划新增目录：

```text
04_成果输出/rag-qa-system/backend/
```

计划接口：

```text
GET  /health
POST /documents/upload
POST /qa/ask
GET  /evaluation
```

第一阶段最小验收：

- `GET /health` 返回服务状态。
- 后端能独立启动。
- README 写清楚后端启动命令。
- 不破坏现有 Streamlit 页面。

第二阶段验收：

- 文档切分逻辑从 Streamlit 中抽出为可复用模块。
- 后端接口可以调用同一套 RAG 核心逻辑。
- Streamlit 后续可以选择调用后端，而不是直接包含全部业务逻辑。

预期简历表达方向：

```text
重构 Streamlit 单体逻辑，拆分 FastAPI 后端服务接口，提升 RAG 核心能力的复用性与可测试性。
```

---

### Step 2：RAG 核心逻辑模块化

目标：

```text
把切分、embedding、检索、评测、生成等逻辑从 app.py 中拆出。
```

建议模块：

```text
backend/
  app.py
  schemas.py
  services/
    chunking.py
    embeddings.py
    vector_store.py
    retrieval.py
    generation.py
    evaluation.py
```

验收标准：

- `chunking.py` 能独立测试。
- `embeddings.py` 管理 Teaching / BGE 双模式。
- `retrieval.py` 负责 Top-k 检索。
- `evaluation.py` 负责 10 题评测。
- Streamlit 和 FastAPI 尽量复用同一套 services。

预期简历表达方向：

```text
拆分 chunking、embedding、retrieval、generation 与 evaluation 模块，降低页面逻辑与 RAG 核心逻辑耦合。
```

---

### Step 3：Chroma 持久化知识库

目标：

```text
使用 Chroma PersistentClient 持久化文档 chunk 和 embedding。
```

计划路径：

```text
04_成果输出/rag-qa-system/.chroma/
```

注意：

- `.chroma/` 是否提交到 Git 需要谨慎，通常不提交。
- README 需要说明如何初始化本地知识库。
- 需要继续区分不同 embedding 维度的 collection。

验收标准：

- 文档入库后，服务重启仍可查询。
- Teaching keyword embedding 和 BGE embedding 不发生维度冲突。
- README 明确说明持久化目录和重建方式。

预期简历表达方向：

```text
构建 Chroma 持久化知识库，解决服务重启后向量索引丢失的问题。
```

---

### Step 4：pytest 自动化评测

目标：

```text
把当前 10 题固定评测升级为可自动运行的 pytest 回归测试。
```

建议目录：

```text
tests/
  test_retrieval_eval.py
```

建议断言：

```text
BGE Top-1 hit >= 0.8
BGE Top-k recall >= 1.0
```

验收标准：

- `python -m pytest` 可以运行。
- 评测失败时能指出失败问题。
- 每次修改 chunk、embedding、检索逻辑后都能回归。

预期简历表达方向：

```text
构建 10 题 E2E 检索评测闭环，使用 Top-1 hit 与 Top-k recall 量化检索质量并支持回归验证。
```

---

### Step 5：Hybrid Search

目标：

```text
BGE vector search + BM25 keyword search + RRF fusion
```

推荐先做本地轻量版，不急着上 Elasticsearch。

计划能力：

- BGE 向量召回。
- BM25 关键词召回。
- RRF 融合排序。
- 对比三种模式：
  - Vector only
  - BM25 only
  - Hybrid RRF

验收标准：

- 页面或脚本能选择检索模式。
- 10 题评测能对比不同检索模式。
- 记录 Hybrid 是否提升 Top-1 或失败题稳定性。

预期简历表达方向：

```text
设计 BGE 向量检索、BM25 关键词检索与 RRF 融合方案，提升中文文档问答在关键词型与语义型问题上的召回稳定性。
```

---

### Step 6：接口文档与工程化说明

目标：

```text
补充后端 API 文档、架构说明和运行说明。
```

建议新增：

```text
04_成果输出/rag-qa-system/API.md
04_成果输出/rag-qa-system/ARCHITECTURE.md
```

内容：

- 服务启动方式。
- API 请求/响应示例。
- RAG 模块架构。
- 数据流说明。
- 当前限制。
- 后续扩展方向。

验收标准：

- 别人可以按 README 跑起来。
- 面试时能清楚讲出模块边界。
- 项目介绍不依赖口头补充。

---

### Step 7：最终项目介绍与简历版本

目标：

```text
升级完成后生成最终项目介绍。
```

技术栈目标：

```text
Python / FastAPI / Streamlit / Chroma / BGE Embedding / BM25 / RRF / OpenAI-compatible LLM API / pytest
```

用语原则：

多使用：

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

最终项目介绍必须基于真实完成项，不能提前写尚未实现的能力。

---

## 6. 升级顺序建议

推荐顺序：

```text
FastAPI 骨架
-> RAG 核心逻辑模块化
-> Chroma 持久化
-> pytest E2E 评测
-> Hybrid Search
-> API / 架构文档
-> 最终简历项目描述
```

不建议一开始就做：

- Docker Compose。
- React 前端。
- PDF 解析。
- 大规模多文档语料。
- rerank 模型。

原因：

```text
当前最缺的是服务化、持久化和自动评测，不是继续堆模型或 UI。
```

---

## 7. 下一步执行任务

下一步从 Step 1 开始：

```text
新增 FastAPI 后端服务骨架
```

最小任务拆解：

1. 确认是否新增 `fastapi` 和 `uvicorn` 依赖。
2. 新增后端目录。
3. 新增 `GET /health`。
4. 新增后端 README。
5. 本地运行验证。
6. 提交并推送。

验收标准：

```text
python -m uvicorn backend.app:app --reload
GET /health 返回 ok
不影响现有 Streamlit 应用
git status clean
```

---

## 8. 当前证据索引

代码与文档：

- `04_成果输出/rag-qa-system/app.py`
- `04_成果输出/rag-qa-system/README.md`
- `04_成果输出/rag-qa-system/PROJECT_BRIEF.md`
- `04_成果输出/rag-qa-system/SCREENSHOT_CHECKLIST.md`
- `01_需求与目标/docuask_v2_upgrade_plan.md`

截图：

- `04_成果输出/rag-qa-system/screenshots/01_app_upload.png`
- `04_成果输出/rag-qa-system/screenshots/02_chunks.png`
- `04_成果输出/rag-qa-system/screenshots/03_retrieval_metrics.png`
- `04_成果输出/rag-qa-system/screenshots/04_bge_metrics.png`
- `04_成果输出/rag-qa-system/screenshots/05_answer_context.png`
- `04_成果输出/rag-qa-system/screenshots/06_answer_sources.png`

关键复盘：

- `05_复盘与沉淀/day31_evaluation_review.md`
- `05_复盘与沉淀/day32_bge_app_integration.md`
- `05_复盘与沉淀/day33_app_metric_display.md`
- `05_复盘与沉淀/day34_project_showcase_packaging.md`
- `05_复盘与沉淀/day35_screenshot_packaging.md`
- `05_复盘与沉淀/day36_upgrade_baseline_record.md`
