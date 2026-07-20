# RAG QA System 项目展示说明

## 项目定位

RAG QA System 是一个本地文档问答原型，用于验证 RAG 的核心链路：

```text
文档上传 -> 文档切分 -> embedding -> Chroma 检索 -> LLM 回答 -> 来源引用
```

项目重点不是做一个复杂平台，而是用最小可运行系统证明：

- 能从用户上传文档中检索相关片段。
- 能把检索上下文交给 LLM 生成回答。
- 能展示来源 chunk，降低幻觉风险。
- 能用固定问题集评估检索质量。

## 核心功能

- TXT / Markdown 文档上传。
- Markdown `##` 标题优先切分。
- Chroma 向量检索。
- Chroma 本地持久化存储。
- FastAPI 文档入库、检索问答和检索评测接口。
- FastAPI multipart 文件上传接口，支持 `.txt` / `.md`。
- FastAPI answer 接口，支持基于检索上下文生成最终回答。
- 双 embedding 模式：
  - `Teaching keyword embedding`
  - `BGE Chinese embedding`
- `vector`、`bm25`、`rrf` 三种检索模式。
- DeepSeek OpenAI-compatible LLM API 生成回答。
- 来源 chunk 展示。
- 10 题固定检索评测。
- Top-1 hit 和 Top-k recall 指标展示。
- pytest 自动化测试覆盖核心接口和检索指标。

## 技术栈

| Layer | Choice |
|---|---|
| UI | Streamlit |
| Vector DB | Chroma |
| Backend API | FastAPI / Uvicorn |
| File upload | python-multipart |
| Teaching embedding | 手写关键词向量 |
| Real embedding | BAAI/bge-small-zh-v1.5 |
| Retrieval | Vector / BM25 / RRF |
| LLM API | DeepSeek OpenAI-compatible API |
| SDK | OpenAI Python SDK |
| Test | pytest |

## 当前评测结果

测试文档：

```text
02_资料与素材/day10_dify_knowledge/python_learning_faq.md
```

评测问题：10 个固定问题。

| Embedding mode | Top-1 hit | Top-k recall |
|---|---:|---:|
| Teaching keyword embedding | 60% | 100% |
| BGE Chinese embedding | 80% | 100% |

结论：

```text
BGE 中文 embedding 的 Top-1 排序效果更好。
两种模式都能在 Top 3 内召回正确 chunk。
```

## 关键工程决策

### 1. API Key 使用环境变量

DeepSeek API Key 不写入代码，而是从环境变量读取：

```text
DEEPSEEK_API_KEY
```

这样可以避免把密钥提交到 GitHub。

### 2. 保留教学版 embedding

教学版关键词 embedding 不是真实语义 embedding，但它便于解释向量检索的基本原理。

所以项目没有直接删除它，而是保留为 baseline。

### 3. BGE 与关键词 embedding 分 collection

教学版关键词向量是 12 维，BGE 向量是 512 维。

不同维度不能写入同一个 Chroma collection，因此主应用使用不同 collection：

```text
uploaded_document_chunks_keyword
uploaded_document_chunks_bge
```

### 4. 评测分 Top-1 和 Top-k

Top-1 hit 评估第一名排序是否正确。

Top-k recall 评估正确资料是否进入候选集合。

这比单一命中率更能解释 RAG 检索问题。

## 如何运行

```powershell
python -m pip install -r requirements.txt
python -m streamlit run "04_成果输出/rag-qa-system/app.py"
```

如需 LLM 生成回答：

```powershell
$env:DEEPSEEK_API_KEY="your_api_key"
python -m streamlit run "04_成果输出/rag-qa-system/app.py"
```

## 可展示点

- 上传 FAQ 文档后，页面会展示文档切分结果。
- 侧边栏可以切换 embedding 模式。
- Retrieval evaluation 区域显示 Top-1 hit 和 Top-k recall。
- 提问后可以看到检索上下文、来源 chunk 和最终回答。
- BGE 模式在当前 FAQ 上 Top-1 结果优于教学版 embedding。

## 截图材料

截图已整理到：

```text
04_成果输出/rag-qa-system/screenshots/
```

当前包含：

| File | Content |
|---|---|
| `01_app_upload.png` | 首页、上传区、问题输入和 embedding 模式 |
| `02_chunks.png` | 文档上传信息和 chunk 切分结果 |
| `03_retrieval_metrics.png` | Teaching keyword embedding 的检索评测 |
| `04_bge_metrics.png` | BGE Chinese embedding 的检索评测 |
| `05_answer_context.png` | 问题、检索说明和上下文 |
| `06_answer_sources.png` | Sources 和 Final answer |

## 当前限制

- 暂不支持 PDF。
- Chroma 持久化目录是本地运行数据，不提交到 GitHub。
- 当前只验证了小型 FAQ 文档。
- 没有引入 rerank。
- BGE 首次加载需要等待。
- 自动化测试不调用真实 LLM API，避免依赖 API Key、网络和额度。

## 下一步

- 扩展更真实的测试文档。
- 评估是否加入 rerank。
- 将项目描述整理成简历项目经历。
