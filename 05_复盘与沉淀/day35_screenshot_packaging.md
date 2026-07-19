# Day 35：截图材料整理

**日期**：2026年7月19日  
**项目**：RAG QA System  
**目标**：整理项目截图材料

---

## 1. 本次完成

已将截图整理到：

```text
04_成果输出/rag-qa-system/screenshots/
```

当前截图：

| File | Content |
|---|---|
| `01_app_upload.png` | 首页、上传区、问题输入和 embedding 模式 |
| `02_chunks.png` | 文档上传信息和 chunk 切分结果 |
| `03_retrieval_metrics.png` | Teaching keyword embedding 的检索评测 |
| `04_bge_metrics.png` | BGE Chinese embedding 的检索评测 |
| `05_answer_context.png` | 问题、检索说明和上下文 |
| `06_answer_sources.png` | Sources 和 Final answer |

---

## 2. 命名调整

原始问答截图来自：

```text
05_answer_with_sources(1).png
05_answer_with_sources(2).png
```

归档后改名为：

```text
05_answer_context.png
06_answer_sources.png
```

这样更适合 GitHub README 和项目展示。

---

## 3. 当前状态

README 已经引用截图。

`PROJECT_BRIEF.md` 已经补充截图材料说明。

`SCREENSHOT_CHECKLIST.md` 已经标记截图完成。

---

## 4. 下一步建议

下一步可以开始整理简历项目描述草稿。

注意：简历描述必须基于当前真实证据：

- 有 Streamlit 页面。
- 有真实中文 embedding。
- 有 Chroma 检索。
- 有 DeepSeek OpenAI-compatible LLM API。
- 有来源引用。
- 有 10 题评测。
- 有 Top-1 和 Top-k 指标。

不能写：

- 支持 PDF。
- 生产级系统。
- 大规模评测。
- 已接入 rerank。

