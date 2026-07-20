# Day 46：BM25 Baseline

**日期**：2026年7月20日  
**项目**：DocuAsk v2  
**目标**：新增独立 BM25 关键词检索 baseline

---

## 1. 本次完成

新增：

```text
04_成果输出/rag-qa-system/backend/services/bm25.py
```

核心函数：

```text
tokenize
retrieve_relevant_chunks_bm25
calculate_document_frequency
calculate_bm25_score
```

---

## 2. 设计取舍

本次没有引入 `jieba`。

原因：

- 今天目标是 baseline，不是中文分词优化。
- 不新增依赖可以降低环境复杂度。
- 当前 FAQ 文档短，使用英文/数字 token + 中文 bigram 已足够做第一版对比。

---

## 3. BM25 和向量检索的区别

BM25 更偏关键词匹配：

```text
词出现得多 -> 可能更相关
词越稀有 -> 权重越高
文档太长 -> 有长度惩罚
```

向量检索更偏语义相似：

```text
问题和文档不一定字面相同，但语义接近也可能召回
```

后续 RRF 的意义是把两种排序结果融合。

---

## 4. 验证结果

独立验证：

```text
Query: RAG 的基本流程是什么？
Top chunk: 6
```

pytest：

```text
BM25 retrieves RAG flow chunk
```

---

## 5. 下一步

下一步建议实现 RRF：

```text
vector ranking + bm25 ranking -> rrf ranking
```

但 RRF 也要先做独立 service，再考虑接入 `/qa` 或 `/evaluation`。
