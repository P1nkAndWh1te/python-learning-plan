# Day 34：RAG 项目作品化整理

**日期**：2026年7月19日  
**项目**：RAG QA System  
**目标**：把当前项目整理成可展示材料

---

## 1. 为什么今天不继续加功能

当前主链路已经具备：

```text
文档上传 -> 文档切分 -> embedding -> Chroma 检索 -> DeepSeek 生成 -> 来源引用 -> 检索评测
```

继续加入 rerank、PDF、持久化等功能之前，先把已有成果整理清楚更重要。

原因：

- README 是别人理解项目的入口。
- 当前根 README 已经过期。
- 项目亮点和限制需要准确表达。
- 后续写简历需要基于真实证据，而不是凭印象描述。

---

## 2. 本次新增材料

新增：

```text
04_成果输出/rag-qa-system/PROJECT_BRIEF.md
04_成果输出/rag-qa-system/SCREENSHOT_CHECKLIST.md
```

更新：

```text
README.md
04_成果输出/rag-qa-system/README.md
```

---

## 3. 当前可展示能力

当前项目可以展示：

- Streamlit 文档上传页面。
- Markdown 文档切分。
- Teaching keyword embedding 和 BGE Chinese embedding 双模式。
- Chroma Top 3 检索。
- Top-1 hit 和 Top-k recall 指标。
- DeepSeek 基于检索上下文生成回答。
- 来源 chunk 展示。
- 10 题固定评测结果。

当前评测结果：

```text
Teaching keyword embedding: Top-1 60%, Top-k 100%
BGE Chinese embedding: Top-1 80%, Top-k 100%
```

---

## 4. 当前不能夸大的点

当前还不能说：

- 支持 PDF。
- 支持多用户。
- 支持持久化知识库。
- 已经达到生产级 RAG。
- 已经有大规模评测集。
- 已经使用 rerank。

更准确的说法是：

```text
这是一个本地 RAG QA 原型，已经跑通核心链路，并具备小规模固定问题评测。
```

---

## 5. 下一步建议

Day35 可以做两件事之一：

```text
方向 A：按截图清单让用户手动截取关键页面
方向 B：开始整理简历项目描述草稿
```

更推荐方向 A。

原因是简历文字最好基于截图、运行结果和提交记录，而不是先写漂亮描述。

