# RAG QA System

这是 Python/RAG 学习计划的正式项目成果目录。

当前 Day17 版本实现 Streamlit 最小页面、TXT/Markdown 文档读取和固定长度文档切分。RAG 后端会在后续学习日逐步接入。

## 当前功能

- 上传 TXT 或 Markdown 文档。
- 读取上传文档内容。
- 显示文件名、大小、字符数和编码。
- 显示文档内容预览。
- 将文档切分为多个 chunk。
- 显示 chunk 总数、编号、长度和内容。
- 输入问题。
- 点击按钮提交问题。
- 显示占位回答。

## 当前限制

- 暂不支持 PDF 解析。
- 暂未接入 embedding、向量检索和 LLM 生成。

## 运行方式

在项目根目录运行：

```powershell
python -m streamlit run "04_成果输出/rag-qa-system/app.py"
```

## 后续计划

- Day16：读取上传文档内容。
- Day17：文档切分。
- Day18：接入 embedding 和 Chroma。
- Day19：接入 LlamaIndex 检索。
- Day20：接入 DeepSeek 生成回答。
