# Day 48：QA Retrieval Modes 验证

本目录用于验证 FastAPI `/qa` 支持显式切换检索模式。

运行：

```powershell
python "03_执行过程/day48_qa_retrieval_modes_check/qa_retrieval_modes_check.py"
```

期望看到：

```text
Mode: vector | Top chunk: 6
Mode: bm25 | Top chunk: 6
Mode: rrf | Top chunk: 6
Unknown mode status: 400
```
