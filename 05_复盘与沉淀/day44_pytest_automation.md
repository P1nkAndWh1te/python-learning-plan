# Day 44：Pytest 自动化测试

**日期**：2026年7月20日  
**项目**：DocuAsk v2  
**目标**：把接口和检索指标验证沉淀成自动化测试

---

## 1. 本次完成

新增：

```text
pytest.ini
04_成果输出/rag-qa-system/tests/conftest.py
04_成果输出/rag-qa-system/tests/test_backend_api.py
04_成果输出/rag-qa-system/tests/test_retrieval_metrics.py
```

依赖新增：

```text
pytest==9.1.1
```

---

## 2. 测试覆盖

当前测试覆盖：

```text
POST /documents 写入 FAQ 文档
POST /qa 检索指定 collection
缺失 collection 返回 404
Teaching keyword embedding 10 题指标
```

其中检索指标断言：

```text
Top-1 hit = 60%
Top-k recall = 100%
```

---

## 3. 设计取舍

今天只把教学版 embedding 纳入自动化测试。

原因：

- 教学版 embedding 快速、稳定、无网络依赖。
- BGE 测试会加载本地模型，并可能触发 Hugging Face 网络请求。
- 自动化测试应该尽量稳定，不能依赖外部 API 或临时网络状态。

DeepSeek 生成也没有进入 pytest。

原因：

- 它依赖 `DEEPSEEK_API_KEY`。
- API 调用有额度、网络、模型服务状态等外部变量。
- 当前阶段要先固定“检索是否正确”。

---

## 4. 验证结果

运行：

```powershell
python -m pytest -q
```

结果：

```text
4 passed, 1 warning in 13.31s
```

warning 来自 FastAPI TestClient 依赖链的 Starlette 弃用提示，不影响当前测试结果。

---

## 5. 下一步

下一步建议新增 FastAPI evaluation endpoint：

```text
GET /evaluation
```

或：

```text
POST /evaluation
```

让 10 题评估不仅能在 pytest 中验证，也能通过后端接口输出。
