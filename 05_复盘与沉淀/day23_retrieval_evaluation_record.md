# Day 23：RAG 检索质量评测记录

**日期**：2026年7月19日  
**项目**：RAG QA System  
**评测阶段**：Day21-Day22 检索质量优化  

---

## 1. 评测目的

本记录用于沉淀一次 RAG 检索质量优化过程。

核心问题不是“系统能不能返回结果”，而是：

```text
不同问题是否能检索到不同且合理的文档片段？
```

如果所有问题都返回同一组 chunk，说明检索区分能力不足。后续 LLM 即使能生成回答，也可能基于不够准确的上下文。

---

## 2. 测试文档

测试文件：

```text
02_资料与素材/day10_dify_knowledge/python_learning_faq.md
```

文档类型：

```text
Markdown FAQ
```

主要主题：

- Day8：LLM API、API Key、DeepSeek API。
- API Key 安全。
- Day9：Embedding、向量相似度、Chroma。
- 向量数据库在 RAG 中的作用。
- RAG 基本流程。

---

## 3. 固定测试问题

```text
1. RAG 的基本流程是什么？
2. API Key 为什么不能写进代码？
3. 什么是 embedding？
4. 向量数据库有什么作用？
5. DeepSeek API 怎么配置？
```

这些问题覆盖了测试文档中的主要主题，用于观察检索是否能区分不同知识点。

---

## 4. Day21 优化前结果

Day21 结果显示，所有问题返回的 Top chunks 基本相同：

```text
RAG 的基本流程是什么？        -> Chunk 3, Chunk 1, Chunk 2
API Key 为什么不能写进代码？  -> Chunk 3, Chunk 1, Chunk 2
什么是 embedding？            -> Chunk 3, Chunk 1, Chunk 2
向量数据库有什么作用？        -> Chunk 3, Chunk 1, Chunk 2
DeepSeek API 怎么配置？       -> Chunk 3, Chunk 1, Chunk 2
```

结论：

```text
检索链路能运行，但检索区分能力不足。
```

---

## 5. 问题分析

造成结果趋同的主要原因：

1. 纯字符切分导致一个 chunk 中混入多个主题。
2. chunk size 偏大，FAQ 文档的多个问题容易被合并在同一片段中。
3. 教学版 embedding 的关键词维度较粗。
4. 部分关键词过泛，容易造成误匹配。
5. Chroma 默认距离方式受向量大小影响，短文本 chunk 可能异常靠前。

---

## 6. Day22 优化策略

Day22 进行了以下调整：

```text
chunk_size: 500 -> 350
chunk_overlap: 100 -> 50
```

切分策略：

```text
Markdown 文档优先按 ## 标题切分
普通文本继续按固定字符数切分
```

embedding 维度：

```text
增强 api / embedding / chroma / deepseek 关键词
减少 sql 等维度中的过泛关键词
```

Chroma 配置：

```text
使用 cosine 距离
```

---

## 7. Day22 优化后结果

使用同一份测试文档和同一组固定问题，优化后的 Top 1 结果为：

```text
RAG 的基本流程是什么？        -> Chunk 6
API Key 为什么不能写进代码？  -> Chunk 3
什么是 embedding？            -> Chunk 4
向量数据库有什么作用？        -> Chunk 5
DeepSeek API 怎么配置？       -> Chunk 2
```

结论：

```text
不同问题已经能检索到更有区分度的 Top chunk。
```

---

## 8. 当前结论

本轮优化证明：

- 文档切分策略会显著影响检索质量。
- FAQ 类 Markdown 文档更适合按标题切分。
- cosine 距离更符合当前教学版 embedding 的学习目标。
- 固定测试问题能帮助定位检索质量问题。
- RAG 优化应该先看 retrieval，再看 generation。

---

## 9. 当前限制

当前评测仍然有明显边界：

- embedding 仍是教学版关键词向量，不是真实语义 embedding。
- 测试文档只有一份，覆盖面有限。
- 评测问题只有 5 个，还没有达到最终项目的 10 题验收规模。
- 当前评测只记录检索结果，没有人工标注正确答案。
- 暂未计算准确率、召回率等指标。

---

## 10. 下一步

后续可以继续做：

```text
1. 扩展到 10 个固定评测问题。
2. 为每个问题标注 expected_top_chunk。
3. 记录检索是否命中预期 chunk。
4. 替换为真实语义 embedding 后重新对比。
5. 形成最终项目评测报告。
```
