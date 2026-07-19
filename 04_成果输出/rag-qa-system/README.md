# RAG QA System

这是 Python/RAG 学习计划的正式项目成果目录。

当前 Day19 版本实现 Streamlit 页面、TXT/Markdown 文档读取、固定长度文档切分、教学版 embedding、Chroma 检索、上下文展示和来源引用。LLM 生成会在后续学习日接入。

## 当前功能

- 上传 TXT 或 Markdown 文档。
- 读取上传文档内容。
- 显示文件名、大小、字符数和编码。
- 显示文档内容预览。
- 将文档切分为多个 chunk。
- 显示 chunk 总数、编号、长度和内容。
- 使用关键词计数生成教学版 embedding。
- 将 chunk 写入临时 Chroma collection。
- 根据用户问题检索 Top 3 相关 chunk。
- 显示问题命中的概念维度。
- 将检索结果格式化为后续 LLM 可用的上下文。
- 显示来源引用列表。
- 输入问题。
- 点击按钮提交问题。
- 显示检索到的 chunk。

## 当前限制

- 暂不支持 PDF 解析。
- 当前 embedding 是教学版关键词向量，不是真实语义 embedding。
- 暂未接入 LLM 生成。

## 运行方式

在项目根目录运行：

```powershell
python -m streamlit run "04_成果输出/rag-qa-system/app.py"
```

## 后续计划

- Day16：读取上传文档内容。
- Day17：文档切分。
- Day18：接入教学版 embedding 和 Chroma。
- Day19：优化检索结果展示和来源引用。
- Day20：接入 DeepSeek 生成回答。
