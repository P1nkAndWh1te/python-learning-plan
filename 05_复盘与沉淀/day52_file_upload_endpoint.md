# Day 52：FastAPI File Upload Endpoint

**日期**：2026年7月20日  
**项目**：DocuAsk v2  
**目标**：让后端支持真实 `.txt` / `.md` 文件上传

---

## 1. 本次完成

新增：

```text
POST /documents/upload
```

该接口支持 multipart 文件上传，并复用原有文档入库逻辑。

---

## 2. 为什么这一步重要

之前的 `/documents` 接收 JSON：

```json
{
  "text": "..."
}
```

这适合脚本测试，但真实应用通常是上传文件。

Day52 后，后端链路变成：

```text
上传 .txt/.md -> 解码 -> 切分 -> embedding -> Chroma 持久化 -> 返回 collection_name
```

---

## 3. 设计选择

没有删除 `/documents`。

原因：

- `/documents` 对自动化测试和脚本调用更简单。
- `/documents/upload` 更接近真实应用。
- 两个入口复用 `create_document_from_text`，避免重复入库逻辑。

---

## 4. 当前边界

当前只支持：

```text
.txt
.md
```

暂不支持：

```text
PDF
Word
多文件上传
```

---

## 5. 下一步

下一步建议进入 Day53：

```text
扩展评测集和测试文档，从单一 FAQ 升级为多文档小样本评测。
```
