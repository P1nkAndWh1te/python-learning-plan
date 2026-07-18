# Day 12：LlamaIndex Quick Start

本目录用于 Day12 LlamaIndex 入门练习。

## 文件

- `data/day08_api.md`：Day8 API 笔记。
- `data/day09_embedding.md`：Day9 embedding 笔记。
- `data/day10_dify.md`：Day10 Dify 笔记。
- `data/day11_sql.md`：Day11 SQL 笔记。
- `llamaindex_mock_quickstart.py`：使用 LlamaIndex 加载文档、建立索引、查询。

## 安装

确认安装新增依赖后执行：

```powershell
python -m pip install llama-index
```

## 运行

```powershell
python "03_执行过程/day12_llamaindex_quickstart/llamaindex_mock_quickstart.py"
```

## 今日重点

今天使用 `MockLLM` 和 `MockEmbedding`，只为了跑通 LlamaIndex 框架链路。

示例数据刻意拆成多个小文件，用来观察文档粒度对检索结果的影响。如果所有内容都放在一个大文件里，检索结果会很粗；拆成多个小文件后，问题更容易命中对应主题。

真实项目中后续需要替换为：

- 真实 LLM：DeepSeek 或其他 OpenAI-compatible LLM API。
- 真实 embedding：本地 BGE、Jina、Dify 可用 embedding provider 或其他低成本 embedding API。
