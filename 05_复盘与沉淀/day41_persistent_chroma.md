# Day 41：Chroma 持久化存储

**日期**：2026年7月20日  
**项目**：DocuAsk v2  
**目标**：把 Chroma 从内存存储切换成本地持久化存储

---

## 1. 本次完成

修改：

```text
04_成果输出/rag-qa-system/backend/services/retrieval.py
```

新增持久化目录：

```text
04_成果输出/rag-qa-system/backend/storage/chroma_db/
```

核心变化：

```text
chromadb.EphemeralClient()
```

改为：

```text
chromadb.PersistentClient(path=str(CHROMA_DB_PATH))
```

---

## 2. 设计取舍

当前使用“文档内容指纹”生成 collection 名。

原因：

- 当前 UI 还没有文档 ID。
- 当前系统还没有多用户隔离。
- 当前评估依赖固定 FAQ 文档和固定 chunk 编号。
- 如果所有文档共用同一个 collection，旧文档可能污染新问题的检索结果。

因此今天采用一个简单策略：

```text
同一份文档复用同一个 collection，不同文档进入不同 collection。
```

写入时使用 `upsert`，避免重复运行同一份文档时出现重复 ID 错误。

---

## 3. Git 处理

本地 Chroma 数据库目录已加入 `.gitignore`：

```text
04_成果输出/rag-qa-system/backend/storage/chroma_db/
```

原因是数据库文件属于运行产物，不属于源码。

---

## 4. 验证结果

独立验证：

```text
Storage exists: True
Query: RAG 的基本流程是什么？
Top chunk: 6
```

10 题评测保持不变：

```text
Teaching keyword embedding: Top-1 60%, Top-k 100%
BGE Chinese embedding: Top-1 80%, Top-k 100%
```

说明持久化改造没有破坏现有检索效果。

---

## 5. 下一步

下一步建议新增 FastAPI 文档上传 endpoint：

```text
POST /documents
```

目标是让后端接收文档内容，完成切分、embedding、写入 Chroma，并返回 chunk 数量和文档状态。
