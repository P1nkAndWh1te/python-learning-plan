# Day14 RAG 核心链路复盘

## 1. 一句话定义 RAG

RAG 是 Retrieval-Augmented Generation，意思是“检索增强生成”。

它不是让大模型凭空回答，而是先从知识库里检索相关资料，再让大模型基于资料生成回答。

## 2. 完整链路

```text
原始文档
  -> 文档解析
  -> 文档分块
  -> 生成 embedding
  -> 存入向量数据库
  -> 用户提问
  -> 问题生成 embedding
  -> 检索相关片段
  -> LLM 根据片段生成回答
  -> 返回回答和引用来源
```

## 3. 各组件职责

| 组件 | 职责 | 当前项目选择 |
|---|---|---|
| LLM | 根据资料生成自然语言回答 | DeepSeek |
| Embedding 模型 | 把文本转换成向量 | 暂未最终确定 |
| 向量数据库 | 存储向量并按相似度检索 | Chroma |
| RAG 框架 | 组织文档加载、索引、检索、查询链路 | LlamaIndex |
| UI | 给用户上传文档和提问 | 后续用 Streamlit |

## 4. Day8-Day13 对应关系

| Day | 学到的部分 | 对应 RAG 环节 |
|---|---|---|
| Day8 | DeepSeek API、环境变量、API Key | LLM 调用 |
| Day9 | Embedding、相似度、Chroma | 向量化和向量检索 |
| Day10 | Dify Chatflow | 可视化 RAG 全流程 |
| Day11 | SQL | 结构化数据查询补课 |
| Day12 | LlamaIndex Quick Start | 文档加载、索引、检索 |
| Day13 | LlamaIndex + DeepSeek | 检索 + 生成闭环 |

## 5. 文档切分为什么重要

如果所有内容都放在一个大文档里，检索时只能返回一个很大的片段，结果不够精确。

如果文档拆成更小的主题块，例如：

```text
day08_api.md
day09_embedding.md
day10_dify.md
day11_sql.md
```

每个节点主题更单一，问题更容易命中对应内容。

但也不是越碎越好。如果切得太碎，LLM 可能拿不到足够上下文。后续项目中需要调：

```text
chunk_size
chunk_overlap
top_k
embedding_model
```

## 6. 当前技术取舍

### DeepSeek

DeepSeek 继续作为生成模型使用。

原因：

- API 已跑通。
- 兼容 OpenAI SDK。
- 当前成本和可用性更适合学习。

### Embedding

Embedding 后续单独选择。

原因：

- DeepSeek 当前主要用于聊天/推理模型。
- Hybrid Search 和真实向量检索需要可靠 embedding 模型。

候选方案：

- 本地 BGE。
- Jina Embeddings。
- Dify 可用 embedding provider。
- 以后如果 OpenAI API 计费解决，再考虑 OpenAI embedding。

## 7. 下一阶段项目目标

第三阶段从 Day15 开始，目标是做一个最小可演示 RAG 系统：

```text
上传文档 -> 提问 -> 检索相关片段 -> DeepSeek 回答 -> 显示来源
```

Day15 第一目标：

```text
搭建 Streamlit 最小页面和项目骨架。
```

