# Day 43：QA Endpoint 验证

本目录用于验证 FastAPI 后端已经支持基于已上传文档的检索问答接口。

运行：

```powershell
python "03_执行过程/day43_qa_endpoint_check/qa_endpoint_check.py"
```

期望看到：

```text
Document status: 200
QA status: 200
Top chunk: 6
Retrieved chunks: 3
Missing collection status: 404
```

接口：

```text
POST /qa
```

当前只返回检索结果和上下文，不调用 DeepSeek 生成最终答案。
