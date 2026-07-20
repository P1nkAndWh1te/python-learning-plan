# Day 45：Evaluation Endpoint

**日期**：2026年7月20日  
**项目**：DocuAsk v2  
**目标**：新增固定问题评估接口

---

## 1. 本次完成

新增 service：

```text
04_成果输出/rag-qa-system/backend/services/evaluation.py
```

新增接口：

```text
POST /evaluation
```

---

## 2. 为什么要抽 evaluation service

之前 10 题评估逻辑在 Streamlit `app.py` 中。

这会导致：

- 页面能评估。
- 后端接口不能复用。
- pytest 需要间接 import 页面。

今天抽出 service 后，同一套评估逻辑可以被三处复用：

```text
Streamlit 页面
FastAPI /evaluation
pytest
```

---

## 3. 接口输出

`POST /evaluation` 返回：

```text
chunk_count
case_count
top_1_hit_rate
top_k_recall
rows
```

其中 rows 记录每道固定问题的：

```text
question
expected_top_chunk
matched_concepts
top_chunks
best_distance
hit
top_k_hit
```

---

## 4. 验证结果

独立验证：

```text
Status code: 200
Chunk count: 6
Case count: 10
Top-1 hit rate: 0.6
Top-k recall: 1.0
```

pytest：

```text
5 passed
```

验证时发现旧的本地 Chroma 运行目录曾出现 hnsw index 损坏，且旧 collection 可能污染后续评估。为避免运行产物影响 baseline，当前代码使用新的 `chroma_db_v2` 目录，并给 collection 名加入 schema version。

---

## 5. 下一步

下一步建议进入 BM25/RRF 升级前的准备：

```text
先记录当前纯向量检索 baseline，再新增 BM25 检索实验。
```

这样后续混合检索提升是否真实有效，可以用指标比较，而不是只靠主观感觉。
