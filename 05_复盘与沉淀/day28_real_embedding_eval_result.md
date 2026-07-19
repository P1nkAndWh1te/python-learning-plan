# Day 28：Chroma 默认 Embedding 评测结果

**日期**：2026年7月19日  
**项目**：RAG QA System  
**实验脚本**：`03_执行过程/day28_real_embedding_eval/real_embedding_eval.py`

---

## 1. 实验目标

验证 Chroma 默认 embedding function 能否替换当前教学版关键词 embedding。

实验要求：

- 使用同一份 FAQ 文档。
- 使用同一套 Markdown 标题切分逻辑。
- 使用同一组 10 个检索评测问题。
- 与教学版关键词 embedding 的 70% baseline 对比。

---

## 2. 运行结果

```text
Chunks: 6
Embedding: Chroma DefaultEmbeddingFunction
Baseline hit rate: 70.0%
Real embedding hit rate: 40.0%
Delta: -30.0%
```

| # | Hit | Expected | Actual top | Top chunks | Best distance | Question |
|---|---|---:|---:|---|---:|---|
| 1 | no | 2 | 1 | Chunk 1, Chunk 4, Chunk 6 | 0.3670 | Day8 学了什么？ |
| 2 | yes | 2 | 2 | Chunk 2, Chunk 3, Chunk 1 | 0.2412 | DeepSeek API 怎么配置？ |
| 3 | no | 3 | 2 | Chunk 2, Chunk 6, Chunk 3 | 0.3606 | OpenAI API 额度和 ChatGPT Plus 互通吗？ |
| 4 | yes | 3 | 3 | Chunk 3, Chunk 2, Chunk 6 | 0.3466 | API Key 为什么不能写进代码？ |
| 5 | yes | 3 | 3 | Chunk 3, Chunk 2, Chunk 1 | 0.1547 | 怎么从环境变量读取 DEEPSEEK_API_KEY？ |
| 6 | no | 4 | 1 | Chunk 1, Chunk 4, Chunk 6 | 0.3427 | Day9 学了什么？ |
| 7 | no | 4 | 5 | Chunk 5, Chunk 4, Chunk 6 | 0.3873 | 什么是 embedding？ |
| 8 | no | 5 | 1 | Chunk 1, Chunk 6, Chunk 4 | 0.5814 | 向量数据库有什么作用？ |
| 9 | no | 5 | 1 | Chunk 1, Chunk 6, Chunk 4 | 0.5462 | 当前项目使用哪个向量数据库？ |
| 10 | yes | 6 | 6 | Chunk 6, Chunk 1, Chunk 5 | 0.4306 | RAG 的基本流程是什么？ |

---

## 3. 结论

Chroma 默认 embedding function 可以在当前环境中正常运行，说明真实 embedding 的本地链路已经打通。

但在当前中文 FAQ 和 10 题评测上，它的命中率只有 40%，低于教学版关键词 embedding 的 70% baseline。

这说明：

- 真实 embedding 不等于一定更好。
- 模型是否适合中文语料非常关键。
- 检索系统不能只凭主观感觉判断效果，必须用固定问题集评测。

---

## 4. 对项目路线的影响

当前不建议把 Streamlit 主应用直接切到 Chroma 默认 embedding。

推荐路线：

```text
保留教学版关键词 embedding 作为 baseline
保留 Day28 默认 embedding 实验作为对照组
下一步评估中文 embedding 模型
```

优先候选：

```text
sentence-transformers + BAAI/bge-small-zh-v1.5
```

但在安装前需要先确认 Python 3.13、Windows、PyTorch、模型下载和运行速度是否可接受。

---

## 5. 今日收获

Day28 的重点不是追求更高分，而是完成了一次真实工程评估：

```text
提出候选方案 -> 独立实验 -> 固定问题集评测 -> 和 baseline 对比 -> 得出是否迁移的决策
```

这是 RAG 项目中非常重要的能力。

