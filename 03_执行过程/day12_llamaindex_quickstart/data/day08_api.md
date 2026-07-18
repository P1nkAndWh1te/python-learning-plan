# Day8：LLM API

Day8 学习了 LLM API、API Key 和环境变量。当前项目使用 DeepSeek API 作为 OpenAI-compatible LLM API。

API Key 不能写进代码，应该通过环境变量读取，例如 `DEEPSEEK_API_KEY`。

DeepSeek API 可以使用 OpenAI Python SDK 调用，但需要设置 `base_url="https://api.deepseek.com"`。

