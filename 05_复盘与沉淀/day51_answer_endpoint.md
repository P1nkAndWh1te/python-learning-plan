# Day 51：FastAPI Answer Endpoint

**日期**：2026年7月20日  
**项目**：DocuAsk v2  
**目标**：让 FastAPI 后端支持 LLM answer 生成

---

## 1. 本次完成

新增：

```text
backend/services/generation.py
POST /answer
```

`/answer` 返回：

```text
question
embedding_mode
collection_name
retrieval_mode
top_k
retrieved_chunks
context
answer
sources
```

---

## 2. 设计选择

没有把 `/qa` 直接改成生成回答，而是新增 `/answer`。

原因：

- `/qa` 保持检索接口语义稳定。
- `/answer` 表示“检索 + LLM 生成”。
- 后续排查问题时，可以先看 `/qa` 检索是否正确，再看 `/answer` 生成是否正确。

---

## 3. API Key 策略

`DEEPSEEK_API_KEY` 仍然只从环境变量读取。

如果没有设置：

```text
POST /answer -> 503
```

自动化测试只验证这个错误分支，不调用真实 DeepSeek API。

---

## 4. 当前链路

现在后端已经可以表达为：

```text
POST /documents -> 写入 Chroma
POST /qa -> 检索 chunks 和 context
POST /answer -> 检索 chunks -> DeepSeek 生成 answer -> 返回 sources
POST /evaluation -> 固定问题检索评测
```

---

## 5. 下一步

下一步建议进入 Day52：

```text
给 FastAPI 增加 multipart 文件上传接口。
```

这样 `/documents` 就不只接收 text，也能接收真实 `.txt` / `.md` 文件。
