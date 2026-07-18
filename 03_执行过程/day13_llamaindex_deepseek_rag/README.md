# Day 13：LlamaIndex + DeepSeek RAG

本目录用于 Day13 练习：用 LlamaIndex 检索本地文档，再用 DeepSeek 生成回答。

## 运行

先设置环境变量：

```powershell
$env:DEEPSEEK_API_KEY="你的_deepseek_api_key"
```

运行：

```powershell
python "03_执行过程/day13_llamaindex_deepseek_rag/llamaindex_deepseek_rag.py"
```

## 今日结构

```text
SimpleDirectoryReader -> VectorStoreIndex -> retriever.retrieve -> DeepSeek API
```

## 注意

今天的 embedding 仍然是本地关键词 embedding，不是最终方案。真实项目后续需要选择更可靠的 embedding 模型。

