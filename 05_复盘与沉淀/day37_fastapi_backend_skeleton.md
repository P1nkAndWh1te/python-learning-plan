# Day 37：FastAPI 后端服务骨架

**日期**：2026年7月20日  
**项目**：DocuAsk v2  
**目标**：建立 FastAPI 后端服务边界

---

## 1. 本次完成

新增后端目录：

```text
04_成果输出/rag-qa-system/backend/
```

新增文件：

```text
backend/__init__.py
backend/app.py
backend/README.md
```

新增接口：

```text
GET /health
```

返回：

```json
{
  "status": "ok",
  "service": "docuask-api",
  "version": "0.1.0"
}
```

---

## 2. 依赖状态

当前环境已存在：

```text
fastapi==0.139.0
uvicorn==0.51.0
```

已同步写入：

```text
requirements.txt
```

---

## 3. 为什么先做 /health

`/health` 是最小后端服务验证点。

它证明：

- FastAPI app 可以被导入。
- Uvicorn 可以启动服务。
- 本地端口可以响应 HTTP 请求。
- 后续可以在这个服务边界中继续迁移 RAG 逻辑。

---

## 4. 当前没有做什么

本次没有：

- 迁移文档切分逻辑。
- 增加上传接口。
- 增加问答接口。
- 增加评测接口。
- 改动 Streamlit 页面。
- 改动 Chroma 存储方式。

这是刻意控制范围，避免一次性重构过大。

---

## 5. 下一步

下一步进入 Step 1 的第二阶段：

```text
抽离文档切分逻辑为可复用 services/chunking.py
```

目标是让 FastAPI 和 Streamlit 后续都能复用同一套 chunking 逻辑。

