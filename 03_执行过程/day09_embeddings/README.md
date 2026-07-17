# Day 9：Embedding 和向量数据库

本目录用于 Day9 练习：用最小代码理解 embedding、余弦相似度和 Chroma 向量检索。

## 文件

- `manual_similarity.py`：纯 Python 实现文本到向量、余弦相似度、Top-K 检索。
- `chroma_manual_embeddings.py`：用 Chroma 存储手动生成的向量并查询。

## 今日路线

先跑纯 Python：

```powershell
python "03_执行过程/day09_embeddings/manual_similarity.py"
```

再决定是否安装 Chroma：

```powershell
python -m pip install chromadb
```

安装后运行：

```powershell
python "03_执行过程/day09_embeddings/chroma_manual_embeddings.py"
```

## 注意

今天先不接真实 embedding API。原因：

- Day8 使用 DeepSeek 负责聊天生成。
- DeepSeek 目前不是我们今天的 embedding 主线。
- 先用手写向量理解 RAG 检索链路，后续再替换成真实 embedding 模型。

