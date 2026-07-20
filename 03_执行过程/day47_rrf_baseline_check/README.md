# Day 47：RRF Baseline 验证

本目录用于验证 DocuAsk 的 RRF 混合排序 baseline。

运行：

```powershell
python "03_执行过程/day47_rrf_baseline_check/rrf_baseline_check.py"
```

期望看到：

```text
Query: RAG 的基本流程是什么？
RRF top chunk: 6
```

本次只验证 RRF 独立 service，不改 `/qa` 默认行为。
