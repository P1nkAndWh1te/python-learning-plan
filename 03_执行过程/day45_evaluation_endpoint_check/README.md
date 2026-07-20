# Day 45：Evaluation Endpoint 验证

本目录用于验证 FastAPI 后端已经支持固定问题检索评估接口。

运行：

```powershell
python "03_执行过程/day45_evaluation_endpoint_check/evaluation_endpoint_check.py"
```

期望看到：

```text
Status code: 200
Chunk count: 6
Case count: 10
Top-1 hit rate: 0.6
Top-k recall: 1.0
```

接口：

```text
POST /evaluation
```
