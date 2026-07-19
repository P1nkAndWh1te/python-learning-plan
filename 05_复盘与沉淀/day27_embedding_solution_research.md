# Day 27：真实 Embedding 替换方案研究

**日期**：2026年7月19日  
**项目**：RAG QA System  
**当前 baseline**：教学版关键词 embedding，10 题检索命中率 70%  

---

## 1. 当前问题

当前项目已经跑通完整 RAG 主链路：

```text
文档上传 -> 文档读取 -> 文档切分 -> embedding -> Chroma 检索 -> DeepSeek 生成回答 -> 来源引用
```

但 embedding 仍然是教学版关键词向量。它适合学习概念，但不适合作为最终项目能力。

Day25-Day26 的 10 题评测结果说明：

```text
总题数：10
命中数：7
命中率：70%
```

未命中问题主要来自：

- 宽泛问题缺少明确关键词。
- 相近主题互相干扰。
- 关键词向量无法理解语义意图。

结论：

```text
教学版 embedding 应保留为 baseline，但后续必须替换真实 embedding。
```

---

## 2. Dify 的定位

Dify 在本学习计划中的定位是：

```text
低代码 RAG 体验和对照组
```

它的价值：

- 帮助理解 Chatflow / Knowledge Retrieval / LLM / Answer 的完整流程。
- 作为可视化 RAG 平台体验。
- 辅助理解为什么 Hybrid Search 需要 embedding 模型。

它不是当前 Streamlit 项目的核心依赖。

当前主项目继续走：

```text
Streamlit + Chroma + OpenAI-compatible LLM API
```

---

## 3. 候选方案对比

### 3.1 继续使用教学版关键词 embedding

优点：

- 不需要新依赖。
- 便于解释 embedding 的基本原理。
- 当前已经有 10 题 baseline。

缺点：

- 不能理解语义。
- 相近主题容易混淆。
- 宽泛问题检索不稳定。
- 不适合作为最终项目能力。

结论：

```text
只保留为教学 baseline，不作为最终方案。
```

### 3.2 Chroma 默认 embedding function

Chroma 官方文档说明，默认 embedding function 使用 Sentence Transformers 的 `all-MiniLM-L6-v2` 模型，本地运行，可能会自动下载模型文件。

优点：

- 与 Chroma 集成简单。
- 本地运行，不需要 API Key。
- 适合做最小真实 embedding 验证。

缺点：

- 默认模型更偏通用英文场景。
- 对中文 FAQ 的效果不一定理想。
- 第一次运行需要下载模型。

结论：

```text
适合作为 Day28 的最小验证路线。
```

### 3.3 Sentence Transformers + BGE 中文模型

Sentence Transformers 官方支持通过 pip 安装，并提供统一的 `SentenceTransformer` 接口。BGE 中文模型 `BAAI/bge-small-zh-v1.5` 是面向中文/中英场景的 embedding 候选。

优点：

- 更适合中文检索。
- 本地运行，不需要 API Key。
- 可以和当前 10 题 baseline 做直接对比。

缺点：

- 需要安装 `sentence-transformers`、`torch` 等依赖。
- 当前环境是 Python 3.13，Windows 下大模型依赖兼容性要谨慎验证。
- 安装体积和首次下载模型成本较高。

结论：

```text
适合作为第二阶段真实 embedding 路线，但不建议今天直接安装。
```

### 3.4 云端 embedding API

可以使用外部 embedding 服务生成向量，再写入 Chroma。

优点：

- 通常效果稳定。
- 不依赖本地模型环境。
- 可以减少本地安装问题。

缺点：

- 需要额外 API Key 和费用。
- 当前已知 DeepSeek 主要用于聊天/推理，不适合作为 embedding 提供方。
- 用户当前不方便使用 OpenAI API 付费路线。

结论：

```text
暂不作为当前主路线。
```

### 3.5 ONNX / FastEmbed 路线

ONNX Runtime 当前环境中已经存在。理论上可以用 ONNX 或 FastEmbed 方式运行小型 embedding 模型。

优点：

- 更轻量。
- CPU 运行友好。
- 可能比完整 PyTorch 依赖更容易部署。

缺点：

- 需要额外调研模型兼容性和 API。
- 对初学阶段不如 Chroma 默认 embedding 路线直接。

结论：

```text
作为备选路线，主线先不走。
```

---

## 4. 推荐路线

推荐分两步走：

### Step 1：Day28 最小验证 Chroma 默认 embedding

目标：

```text
在独立脚本中使用 Chroma 默认 embedding function 跑同一份 FAQ 和同一组 10 题评测。
```

原因：

- 不直接改主应用。
- 风险较低。
- 可以先确认真实 embedding 链路能跑通。
- 与当前教学版 70% baseline 可对比。

### Step 2：再评估 BGE 中文模型

如果 Chroma 默认 embedding 对中文效果不理想，再考虑：

```text
sentence-transformers + BAAI/bge-small-zh-v1.5
```

但这一步要先确认：

- Python 3.13 环境是否兼容。
- PyTorch 安装是否顺利。
- 模型下载是否稳定。
- 本机运行速度是否可接受。

---

## 5. Day28 验证计划

Day28 建议新增独立实验脚本：

```text
03_执行过程/day28_real_embedding_eval/
```

脚本目标：

```text
读取 python_learning_faq.md
复用当前 Markdown 标题切分
使用 Chroma 默认 embedding function
运行同一组 10 题评测
输出 expected / actual / hit / hit_rate
```

验收标准：

```text
真实 embedding 链路能跑通
能得到 10 题命中率
能与教学版 70% baseline 对比
```

---

## 6. 当前决策

```text
Dify：保留为体验和对照组，不进入主项目依赖。
教学版 embedding：保留为 baseline，不作为最终方案。
Day28：优先验证 Chroma 默认 embedding function。
BGE 中文模型：作为后续更适合中文的候选方案。
云端 embedding API：当前不是主路线。
```

---

## 7. 参考资料

- Chroma embedding functions 文档：https://docs.trychroma.com/docs/embeddings/embedding-functions
- Sentence Transformers 安装文档：https://sbert.net/docs/installation.html
- Sentence Transformers 快速开始：https://www.sbert.net/docs/quickstart.html
- BAAI/bge-small-zh-v1.5 模型页：https://huggingface.co/BAAI/bge-small-zh-v1.5
