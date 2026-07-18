# Python 学习 FAQ

这份文档用于 Day10 Dify RAG 体验。内容来自当前 Python 学习项目的 Day8 和 Day9。

## Day8 学了什么？

Day8 学习了 LLM API、API Key、环境变量和 DeepSeek API 调用。由于 OpenAI API 额度和 ChatGPT Plus 不互通，当前项目使用 DeepSeek API 继续学习 API 调用链路。

DeepSeek API 兼容 OpenAI SDK。代码中使用 `openai` Python 包，但需要设置 `base_url="https://api.deepseek.com"`，并从环境变量 `DEEPSEEK_API_KEY` 读取密钥。

## 为什么 API Key 不能写进代码？

API Key 类似密码，是调用模型服务的凭证。如果把 API Key 写进代码并提交到 GitHub，别人可能拿到你的密钥并消耗你的额度。

正确做法是把 API Key 放在环境变量里，例如 `DEEPSEEK_API_KEY`。Python 程序通过 `os.environ.get("DEEPSEEK_API_KEY")` 读取密钥。

## Day9 学了什么？

Day9 学习了 Embedding、向量相似度和 Chroma 向量数据库。

Embedding 是把文本转换成数字向量。检索时，系统会把用户问题和文档片段都转换成向量，然后比较它们的相似度，找出最接近的问题相关文档。

## 向量数据库在 RAG 中做什么？

向量数据库负责存储文档片段和对应的 embedding，并根据用户问题的 embedding 查找最相似的文档片段。

在当前项目中，Chroma 是首选向量数据库。Day9 已经用手写 embedding 跑通了 Chroma 最小检索示例。

## RAG 的基本流程是什么？

RAG 的基本流程是：

1. 把文档切分成较小片段。
2. 把每个片段转换成 embedding。
3. 把 embedding 存入向量数据库。
4. 用户提问时，把问题也转换成 embedding。
5. 从向量数据库中检索最相关的文档片段。
6. 把检索到的片段交给 LLM，让 LLM 根据资料生成回答。
7. 如果系统支持引用来源，回答中还会显示使用了哪些文档片段。

