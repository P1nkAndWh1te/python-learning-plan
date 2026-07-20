# Day 47：RRF Baseline

**日期**：2026年7月20日  
**项目**：DocuAsk v2  
**目标**：新增独立 RRF 混合排序 baseline

---

## 1. 本次完成

新增：

```text
04_成果输出/rag-qa-system/backend/services/rrf.py
```

核心函数：

```text
reciprocal_rank_fusion
retrieve_relevant_chunks_rrf
```

---

## 2. RRF 是什么

RRF 的全称是 Reciprocal Rank Fusion。

它不直接看原始分数，而是看排名：

```text
RRF score = sum(1 / (k + rank))
```

如果一个 chunk 同时在向量检索和 BM25 中排名靠前，它的融合分数就会更高。

---

## 3. 为什么先独立验证

今天没有改 `/qa` 默认行为。

原因：

- 当前 `/qa` 已经稳定。
- RRF 还只是 baseline。
- 先独立验证可以降低回归风险。

后续要接入 `/qa`，应该增加显式参数，例如：

```text
retrieval_mode = vector | bm25 | rrf
```

---

## 4. 验证结果

独立验证：

```text
Query: RAG 的基本流程是什么？
RRF top chunk: 6
```

pytest：

```text
RRF retrieves RAG flow chunk
```

---

## 5. 下一步

下一步建议新增 retrieval mode 参数：

```text
POST /qa
retrieval_mode: vector | bm25 | rrf
```

这样后端可以显式切换检索策略，而不是隐式改变默认行为。
