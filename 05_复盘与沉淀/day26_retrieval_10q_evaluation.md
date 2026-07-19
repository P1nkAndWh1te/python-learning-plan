# Day 26：10 题检索评测表

**日期**：2026年7月19日  
**项目**：RAG QA System  
**评测对象**：教学版关键词 embedding + Chroma cosine 检索  

---

## 1. 评测目的

本评测用于记录当前教学版 RAG 检索链路在固定问题集上的表现。

核心目标：

```text
用 10 个固定问题记录检索是否命中预期 chunk，形成后续替换真实 embedding 的对比基线。
```

---

## 2. 测试环境

测试文档：

```text
02_资料与素材/day10_dify_knowledge/python_learning_faq.md
```

切分方式：

```text
Markdown 文档优先按 ## 标题切分
普通文本按固定字符数切分
```

检索配置：

```text
chunk_size = 350
chunk_overlap = 50
top_k = 3
Chroma distance = cosine
embedding = 教学版关键词向量
```

---

## 3. Chunk 对应关系

基于当前切分结果，主要 chunk 含义如下：

| Chunk | 主题 |
|---|---|
| Chunk 1 | 文档标题和简介 |
| Chunk 2 | Day8、LLM API、DeepSeek API 配置 |
| Chunk 3 | API Key 安全和环境变量 |
| Chunk 4 | Day9、Embedding、向量相似度 |
| Chunk 5 | 向量数据库和 Chroma |
| Chunk 6 | RAG 基本流程 |

---

## 4. 10 题评测结果

| # | Question | Expected | Actual Top Chunks | Best Distance | Hit |
|---|---|---|---|---:|---|
| 1 | Day8 学了什么？ | Chunk 2 | Chunk 1, Chunk 2, Chunk 4 | 0.6220 | No |
| 2 | DeepSeek API 怎么配置？ | Chunk 2 | Chunk 2, Chunk 3, Chunk 1 | 0.1230 | Yes |
| 3 | OpenAI API 额度和 ChatGPT Plus 互通吗？ | Chunk 3 | Chunk 3, Chunk 2, Chunk 5 | 0.0494 | Yes |
| 4 | API Key 为什么不能写进代码？ | Chunk 3 | Chunk 3, Chunk 2, Chunk 5 | 0.0494 | Yes |
| 5 | 怎么从环境变量读取 DEEPSEEK_API_KEY？ | Chunk 3 | Chunk 2, Chunk 3, Chunk 6 | 0.1154 | No |
| 6 | Day9 学了什么？ | Chunk 4 | Chunk 5, Chunk 4, Chunk 1 | 0.5034 | No |
| 7 | 什么是 embedding？ | Chunk 4 | Chunk 4, Chunk 6, Chunk 5 | 0.0887 | Yes |
| 8 | 向量数据库有什么作用？ | Chunk 5 | Chunk 5, Chunk 4, Chunk 6 | 0.1877 | Yes |
| 9 | 当前项目使用哪个向量数据库？ | Chunk 5 | Chunk 5, Chunk 4, Chunk 6 | 0.1877 | Yes |
| 10 | RAG 的基本流程是什么？ | Chunk 6 | Chunk 6, Chunk 1, Chunk 5 | 0.5687 | Yes |

---

## 5. 汇总结果

```text
总题数：10
命中数：7
未命中数：3
命中率：70%
```

---

## 6. 未命中问题分析

### 6.1 Day8 学了什么？

结果：

```text
Expected: Chunk 2
Actual: Chunk 1, Chunk 2, Chunk 4
```

原因：

- 问题本身只包含 `Day8`，语义信息太少。
- 教学版 embedding 只能识别关键词，不能理解“Day8 学习内容”这种宽泛意图。
- Chunk 1 中包含文档简介，可能因项目主题词产生干扰。

结论：

```text
宽泛问题对教学版关键词 embedding 不友好。
```

### 6.2 怎么从环境变量读取 DEEPSEEK_API_KEY？

结果：

```text
Expected: Chunk 3
Actual: Chunk 2, Chunk 3, Chunk 6
```

原因：

- 问题同时包含 `DeepSeek`、`API Key`、`环境变量`。
- Chunk 2 和 Chunk 3 都包含 DeepSeek/API 相关信息。
- 教学版 embedding 无法精细区分“DeepSeek 配置”和“API Key 安全读取”。

结论：

```text
相近主题之间容易互相干扰。
```

### 6.3 Day9 学了什么？

结果：

```text
Expected: Chunk 4
Actual: Chunk 5, Chunk 4, Chunk 1
```

原因：

- 问题本身只包含 `Day9`，信息密度不足。
- Day9 同时覆盖 embedding 和 Chroma。
- Chunk 5 的 Chroma/向量数据库关键词较强，因此排到 Chunk 4 前面。

结论：

```text
主题总结型问题需要更强的语义 embedding，不能只靠关键词计数。
```

---

## 7. 当前结论

当前教学版检索链路已经能完成：

- 固定问题批量检索。
- 预期 chunk 对比。
- hit 判断。
- 命中率统计。
- 失败样本分析。

但它也暴露出明确限制：

- 宽泛问题容易检索不准。
- 相近主题容易混淆。
- 关键词向量不能理解语义意图。

这正好说明后续需要替换真实 embedding，而不是继续无限增加人工关键词。

---

## 8. 后续改进方向

下一阶段建议：

```text
1. 研究真实 embedding 的低成本方案。
2. 保留当前 10 题评测表作为 baseline。
3. 替换 embedding 后重新运行同一组问题。
4. 对比命中率是否从 70% 提升。
5. 将对比结果写入最终项目评测报告。
```
