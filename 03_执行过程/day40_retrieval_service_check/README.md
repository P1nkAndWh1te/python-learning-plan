# Day 40：Retrieval Service 验证

本目录用于验证 DocuAsk 的检索逻辑已经从 Streamlit 页面抽离到 service。

运行：

```powershell
python "03_执行过程/day40_retrieval_service_check/retrieval_service_check.py"
```

期望看到：

```text
Query: RAG 的基本流程是什么？
Top chunk: 6
Teaching keyword embedding | 60% | 100%
BGE Chinese embedding | 80% | 100%
```
