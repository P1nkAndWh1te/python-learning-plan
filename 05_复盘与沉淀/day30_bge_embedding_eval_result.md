# Day 30：BGE 中文 Embedding 评测结果

**日期**：2026年7月19日  
**项目**：RAG QA System  
**实验脚本**：`03_执行过程/day30_bge_embedding_eval/bge_embedding_eval.py`

---

## 1. 安装和环境验证

已安装：

```text
sentence-transformers 5.6.0
torch 2.13.0+cpu
transformers 5.14.1
```

安装过程中发生了一个依赖调整：

```text
tokenizers: 0.23.1 -> 0.22.2
```

原因是 `transformers 5.14.1` 要求 `tokenizers<=0.23.0,>=0.22.0`。

---

## 2. 模型加载验证

模型：

```text
BAAI/bge-small-zh-v1.5
```

最小验证结果：

```text
ok
(1, 512)
float32
```

说明模型可以在当前 Windows + Python 3.13 环境中加载并生成 512 维向量。

运行时出现两个非阻塞警告：

- 未登录 Hugging Face，下载可能较慢。
- Windows 当前缓存不支持符号链接，模型缓存会多占一些磁盘空间。

---

## 3. 评测结果

```text
Chunks: 6
Embedding: BAAI/bge-small-zh-v1.5
Teaching keyword embedding hit rate: 70.0%
Chroma default embedding hit rate: 40.0%
BGE Chinese embedding hit rate: 70.0%
Delta vs keyword baseline: +0.0%
Delta vs Chroma default: +30.0%
```

| # | Hit | Expected | Actual top | Top chunks | Best distance | Question |
|---|---|---:|---:|---|---:|---|
| 1 | yes | 2 | 2 | Chunk 2, Chunk 1, Chunk 4 | 0.3722 | Day8 学了什么？ |
| 2 | yes | 2 | 2 | Chunk 2, Chunk 3, Chunk 1 | 0.2897 | DeepSeek API 怎么配置？ |
| 3 | no | 3 | 2 | Chunk 2, Chunk 3, Chunk 4 | 0.3475 | OpenAI API 额度和 ChatGPT Plus 互通吗？ |
| 4 | yes | 3 | 3 | Chunk 3, Chunk 2, Chunk 1 | 0.1488 | API Key 为什么不能写进代码？ |
| 5 | no | 3 | 2 | Chunk 2, Chunk 3, Chunk 4 | 0.2796 | 怎么从环境变量读取 DEEPSEEK_API_KEY？ |
| 6 | no | 4 | 1 | Chunk 1, Chunk 4, Chunk 2 | 0.3989 | Day9 学了什么？ |
| 7 | yes | 4 | 4 | Chunk 4, Chunk 5, Chunk 6 | 0.3651 | 什么是 embedding？ |
| 8 | yes | 5 | 5 | Chunk 5, Chunk 4, Chunk 6 | 0.3096 | 向量数据库有什么作用？ |
| 9 | yes | 5 | 5 | Chunk 5, Chunk 4, Chunk 2 | 0.3244 | 当前项目使用哪个向量数据库？ |
| 10 | yes | 6 | 6 | Chunk 6, Chunk 1, Chunk 5 | 0.1992 | RAG 的基本流程是什么？ |

---

## 4. 结论

BGE 中文 embedding 明显优于 Chroma 默认 embedding，但没有超过当前教学版关键词 embedding baseline。

当前不能直接得出“应该替换主应用 embedding”的结论。

更准确的判断是：

```text
BGE 路线工程上可行，中文效果优于 Chroma 默认模型，但当前 10 题结果还不足以证明它应该替换主应用 baseline。
```

---

## 5. 下一步建议

下一步不要继续盲目换模型，而应该检查评测集和文档本身：

- `Day8 学了什么？`、`Day9 学了什么？` 这类问题依赖标题和日期标记，不完全是语义问题。
- `OpenAI API 额度和 ChatGPT Plus 互通吗？` 与 `DeepSeek API 怎么配置？` 都和 API 主题接近，容易竞争同一 chunk。
- `怎么从环境变量读取 DEEPSEEK_API_KEY？` 更像代码操作问题，但当前 chunk 里 API 配置和 API Key 安全混在相邻主题中。

推荐 Day31 做：

```text
评测集复盘 + 文档 chunk 结构优化
```

目标不是让分数变好看，而是让评测问题、文档结构和真实用户查询更一致。

