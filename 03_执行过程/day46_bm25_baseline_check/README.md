# Day 46：BM25 Baseline 验证

本目录用于验证 DocuAsk 的 BM25 关键词检索 baseline。

运行：

```powershell
python "03_执行过程/day46_bm25_baseline_check/bm25_baseline_check.py"
```

期望看到：

```text
Query: RAG 的基本流程是什么？
Top chunk: 6
```

本次只验证 BM25 独立检索，不做 RRF 融合。
