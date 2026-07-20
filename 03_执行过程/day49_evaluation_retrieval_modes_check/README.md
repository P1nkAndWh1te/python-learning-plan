# Day 49：Evaluation Retrieval Modes 验证

本目录用于验证 FastAPI `/evaluation` 支持显式切换检索模式。

运行：

```powershell
python "03_执行过程/day49_evaluation_retrieval_modes_check/evaluation_retrieval_modes_check.py"
```

期望看到：

```text
Mode | Top-1 | Top-k
vector | 0.6 | 1.0
bm25 | ...
rrf | ...
Unknown mode status: 400
```
