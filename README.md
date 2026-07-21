# DocuAsk

DocuAsk is a local document QA system built around a Retrieval-Augmented Generation (RAG) pipeline:

```text
document upload -> chunking -> embedding -> retrieval -> context assembly -> LLM answer -> source citations
```

The application uses Streamlit for the UI, FastAPI for reusable backend endpoints, Chroma for local vector storage, BGE for Chinese embedding, BM25/RRF for retrieval comparison, and DeepSeek through an OpenAI-compatible LLM API.

## Highlights

- Upload `.txt` and `.md` documents.
- Split documents by Markdown sections or fixed-size chunks with overlap.
- Store document chunks in a local Chroma persistent collection.
- Retrieve chunks with vector search, BM25, or RRF ranking fusion.
- Generate grounded answers with source chunk citations.
- Evaluate retrieval quality with Top-1 hit and Top-k recall.
- Expose reusable FastAPI endpoints for ingestion, QA, answer generation, and evaluation.
- Cover core API behavior and retrieval metrics with pytest.

## Project Materials

- 项目展示说明：`PROJECT_BRIEF.md`
- API 文档：`API.md`
- 架构说明：`ARCHITECTURE.md`

## 技术栈

- Python
- Streamlit
- Chroma
- Sentence Transformers
- OpenAI Python SDK
- DeepSeek API
- FastAPI
- Uvicorn
- pytest
- python-multipart
- BM25
- RRF

## 运行方式

在仓库根目录运行：

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

打开：

```text
http://localhost:8501
```

## DeepSeek API Key

生成回答需要在启动 Streamlit 的同一个 PowerShell 中设置环境变量：

```powershell
$env:DEEPSEEK_API_KEY="your_api_key"
python -m streamlit run app.py
```

注意：

- 不要把 API Key 写进代码。
- 不要把 API Key 提交到 GitHub。
- 如果页面提示 key 未设置，先确认启动 Streamlit 的当前终端能读到该环境变量。

检查命令：

```powershell
python -c "import os; print('set' if os.environ.get('DEEPSEEK_API_KEY') else 'missing')"
```

## 测试文档

推荐使用：

```text
examples/rag_faq.md
```

可测试问题：

```text
RAG 的基本流程是什么？
API Key 为什么不能写进代码？
什么是 embedding？
向量数据库有什么作用？
DeepSeek API 怎么配置？
```

## 检索评测结果

当前 FAQ 样例文档的检索结果：

```text
RAG 的基本流程是什么？        -> Chunk 6
API Key 为什么不能写进代码？  -> Chunk 3
什么是 embedding？            -> Chunk 4
向量数据库有什么作用？        -> Chunk 5
DeepSeek API 怎么配置？       -> Chunk 2
```

## Embedding 模式

当前支持两种模式：

```text
Teaching keyword embedding
BGE Chinese embedding
```

教学版关键词 embedding 适合理解向量检索原理，速度快、可解释。

BGE 中文 embedding 使用 `BAAI/bge-small-zh-v1.5`，适合验证真实中文语义检索效果。首次运行可能需要加载本地模型。

当前 FAQ 的评测结果：

```text
Teaching keyword embedding: Top-1 70%, Top-k 100%
BM25 retrieval: Top-1 80%, Top-k 90%
RRF retrieval: Top-1 80%, Top-k 90%
```

## 当前限制

- 暂不支持 PDF 解析。
- Chroma 持久化目录是本地运行数据，不提交到 GitHub。
- BGE 模型首次加载需要等待。
- 当前评测重点是 top-1 hit 和 top-k recall，还没有引入 rerank。
- BGE 首次加载会比教学版关键词 embedding 慢。
- 自动化测试不调用真实 LLM API，避免依赖 API Key、网络和额度。

## 下一步

- 评估是否需要 rerank。
- 扩展 PDF / Word 文档解析。
- 扩大评测集并记录失败案例。
