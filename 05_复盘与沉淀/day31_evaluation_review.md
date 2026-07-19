# Day 31：评测集复盘与检索指标修正

**日期**：2026年7月19日  
**项目**：RAG QA System  
**脚本**：`03_执行过程/day31_evaluation_review/evaluation_review.py`

---

## 1. 为什么要复盘评测集

Day30 的 BGE 中文 embedding 结果没有超过教学版关键词 baseline。

复盘后发现，原评测集中第 3 题的 expected chunk 标错了：

```text
问题：OpenAI API 额度和 ChatGPT Plus 互通吗？
原 expected：Chunk 3
修正后 expected：Chunk 2
```

原因是 FAQ 中“OpenAI API 额度和 ChatGPT Plus 不互通”的内容在 `Day8 学了什么？` 段落中，也就是 `Chunk 2`。

---

## 2. 指标修正

原先只看：

```text
strict top-1 hit
```

也就是第一名检索结果是否等于 expected chunk。

Day31 增加：

```text
top-k recall
```

也就是 expected chunk 是否出现在前三个检索结果里。

两者区别：

- strict top-1 hit 反映排序能力。
- top-k recall 反映相关资料是否被召回。

RAG 中通常先保证召回，再优化排序。

---

## 3. 修正后评测结果

```text
Chunks: 6
Top k: 3
```

| Method | Strict top-1 | Top-k recall |
|---|---:|---:|
| Teaching keyword embedding | 6/10 (60.0%) | 10/10 (100.0%) |
| Chroma default embedding | 5/10 (50.0%) | 7/10 (70.0%) |
| BGE Chinese embedding | 8/10 (80.0%) | 10/10 (100.0%) |

---

## 4. 失败题分析

### 4.1 教学版关键词 embedding

strict top-1 失败：

- `Day8 学了什么？`
- `OpenAI API 额度和 ChatGPT Plus 互通吗？`
- `怎么从环境变量读取 DEEPSEEK_API_KEY？`
- `Day9 学了什么？`

但 top-k recall 是 100%，说明它能召回相关 chunk，只是排序不稳定。

### 4.2 Chroma 默认 embedding

strict top-1 失败：

- `Day8 学了什么？`
- `Day9 学了什么？`
- `什么是 embedding？`
- `向量数据库有什么作用？`
- `当前项目使用哪个向量数据库？`

top-k recall 只有 70%，说明默认英文通用模型对当前中文 FAQ 的召回不够稳定。

### 4.3 BGE 中文 embedding

strict top-1 失败：

- `怎么从环境变量读取 DEEPSEEK_API_KEY？`
- `Day9 学了什么？`

但 top-k recall 是 100%，说明 BGE 已经能把相关 chunk 放进候选集合，剩下主要是排序和文档结构问题。

---

## 5. 当前结论

修正评测口径后，BGE 中文 embedding 是当前最优方案：

```text
BGE strict top-1：80%
BGE top-k recall：100%
```

这比 Day30 的初始判断更积极。

但还不建议立刻替换主应用，因为接入主应用还要处理：

- 模型加载速度。
- 首次下载和本地缓存。
- Streamlit 页面等待提示。
- 是否保留教学版 embedding 作为可切换模式。
- requirements 中新增依赖后的安装说明。

---

## 6. 下一步建议

Day32 可以进入主应用接入设计。

推荐不要直接删除教学版关键词 embedding，而是增加 embedding 模式：

```text
Teaching keyword embedding
BGE Chinese embedding
```

这样用户可以在 UI 中对比两种检索方式，学习效果也更好。

