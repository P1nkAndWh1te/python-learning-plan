# Day 8：LLM API 基础

本目录用于 Day8 练习：环境变量检查和第一个 DeepSeek API 调用。

DeepSeek API 兼容 OpenAI SDK，所以代码仍然使用 `openai` 这个 Python 包，但需要配置：

- `api_key=os.environ.get("DEEPSEEK_API_KEY")`
- `base_url="https://api.deepseek.com"`
- `model="deepseek-v4-flash"`

## 文件

- `env_check.py`：检查 `DEEPSEEK_API_KEY` 是否已经设置。
- `deepseek_first_call.py`：使用 OpenAI Python SDK + DeepSeek API 发起一次最小模型请求。

## 执行顺序

1. 设置环境变量。
2. 运行 `env_check.py`。
3. 安装 OpenAI SDK。
4. 运行 `openai_first_call.py`。

## PowerShell 示例

临时设置：

```powershell
$env:DEEPSEEK_API_KEY="你的_deepseek_api_key"
```

检查：

```powershell
python "03_执行过程/day08_api_basics/env_check.py"
```

安装 SDK：

```powershell
python -m pip install openai
```

调用 API：

```powershell
python "03_执行过程/day08_api_basics/deepseek_first_call.py"
```

## 安全规则

不要把 API Key 写进代码。不要把 `.env` 或任何包含密钥的文件提交到 GitHub。

项目描述中使用“OpenAI-compatible LLM API”或“兼容 OpenAI 接口的 LLM 服务”，不要写死为 OpenAI API。
