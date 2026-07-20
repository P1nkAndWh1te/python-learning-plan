# Day 51：Answer Endpoint 验证

本目录用于验证 FastAPI `/answer` 接口已经接入 LLM 生成分支。

运行：

```powershell
python "03_执行过程/day51_answer_endpoint_check/answer_endpoint_check.py"
```

默认验证不依赖真实 API Key：

```text
Document status: 200
Answer without key status: 503
Unknown mode status: 400
```

如需额外尝试真实 `/answer` 调用：

```powershell
$env:RUN_REAL_ANSWER_CHECK="1"
$env:DEEPSEEK_API_KEY="your_api_key"
python "03_执行过程/day51_answer_endpoint_check/answer_endpoint_check.py"
```
