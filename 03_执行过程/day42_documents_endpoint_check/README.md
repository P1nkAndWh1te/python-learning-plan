# Day 42：Documents Endpoint 验证

本目录用于验证 FastAPI 后端已经支持文档写入接口。

运行：

```powershell
python "03_执行过程/day42_documents_endpoint_check/documents_endpoint_check.py"
```

期望看到：

```text
Status code: 200
Chunk count: 6
Stored chunk count: 6
Bad request status: 400
```

接口：

```text
POST /documents
```

当前只接收文本内容，不做 multipart 文件上传。
