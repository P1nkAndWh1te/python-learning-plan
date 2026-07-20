# Day 41：Persistent Chroma 验证

本目录用于验证 DocuAsk 已从 Chroma 临时内存库切换到本地持久化目录。

运行：

```powershell
python "03_执行过程/day41_persistent_chroma_check/persistent_chroma_check.py"
```

期望看到：

```text
Storage exists: True
Query: RAG 的基本流程是什么？
Top chunk: 6
Teaching keyword embedding | 60% | 100%
BGE Chinese embedding | 80% | 100%
```

本地生成的 Chroma 数据库目录位于：

```text
04_成果输出/rag-qa-system/backend/storage/chroma_db/
```

该目录只用于本机运行，不提交到 Git。
