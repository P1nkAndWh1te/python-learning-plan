# RAG QA System

这是 Python/RAG 学习计划的正式项目成果目录。

当前 Day15 版本只实现 Streamlit 最小页面，用于确认应用入口和交互结构。RAG 后端会在后续学习日逐步接入。

## 当前功能

- 上传本地文档。
- 输入问题。
- 点击按钮提交问题。
- 显示占位回答。

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
