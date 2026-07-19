# RAG QA System 截图清单

这份清单用于后续整理 GitHub README、作品集或简历材料。

## 必需截图

### 1. 应用首页和上传区

需要展示：

- 页面标题 `RAG QA System`
- 侧边栏 embedding 模式选择
- 文档上传组件

建议文件名：

```text
01_app_upload.png
```

### 2. 文档切分结果

需要展示：

- 上传 `python_learning_faq.md`
- Chunks 数量
- 至少一个展开的 chunk 内容

建议文件名：

```text
02_chunks.png
```

### 3. 检索评测指标

需要展示：

- `Top-1 hit`
- `Top-k recall`
- 10 题评测表
- 当前 embedding mode

建议文件名：

```text
03_retrieval_metrics.png
```

### 4. BGE 模式评测

需要展示：

- 侧边栏选择 `BGE Chinese embedding`
- Top-1 结果为 80%
- Top-k 结果为 100%

建议文件名：

```text
04_bge_metrics.png
```

### 5. 问答结果和来源引用

需要展示：

- 用户问题
- 检索上下文
- Sources
- Final answer

建议文件名：

```text
05_answer_with_sources.png
```

## 截图注意事项

- 不要截到任何 API Key。
- 如果 DeepSeek key 没有设置，可以只截检索和来源展示。
- 如果要截最终回答，确认回答来自上传文档。
- 截图前尽量使用同一份测试文档，避免展示结果不一致。

