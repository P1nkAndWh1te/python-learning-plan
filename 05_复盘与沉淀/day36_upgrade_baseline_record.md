# Day 36：升级前项目状态记录

**日期**：2026年7月19日  
**项目**：DocuAsk / RAG QA System  
**目标**：记录升级前基线，准备进入工程化升级

---

## 1. 当前基线

当前项目已经完成：

- Streamlit 本地页面。
- TXT / Markdown 文档上传。
- 文档切分。
- Teaching keyword embedding。
- BGE Chinese embedding。
- Chroma Top 3 检索。
- DeepSeek 回答生成。
- 来源 chunk 展示。
- 10 题固定评测。
- Top-1 hit 和 Top-k recall 指标。
- README、PROJECT_BRIEF、截图材料。

当前评测：

```text
Teaching keyword embedding: Top-1 60%, Top-k 100%
BGE Chinese embedding: Top-1 80%, Top-k 100%
```

当前最新提交：

```text
ffa4bb2 Add day 35 screenshot materials
```

---

## 2. 为什么要升级

当前项目已经能展示 RAG 核心链路，但仍然偏本地原型。

主要不足：

- Streamlit 单体应用，后端服务边界不清晰。
- Chroma 使用临时 collection，没有持久化知识库。
- 评测主要通过脚本和页面运行，还没有 pytest 自动回归。
- 检索方式主要是向量检索，没有 hybrid search。
- README 和截图已经够展示，但项目工程化深度还可以继续提升。

---

## 3. 目标升级方向

升级方向：

```text
FastAPI 后端服务
Chroma 持久化
pytest E2E 评测
Hybrid Search
工程化项目说明
```

升级完成后，再生成最终简历项目介绍。

---

## 4. 简历用语原则

后续项目介绍要从“使用/实现/编写”升级为更有动作和结果的表达：

```text
设计
重构
优化
提升
解决
排查
构建
验证
沉淀
```

但所有表述必须基于真实代码、截图、评测结果和提交记录。

---

## 5. 下一步

下一步进入 DocuAsk v2 Step 1：

```text
新增 FastAPI 后端服务骨架
```

目标是从本地 Streamlit 原型，升级为可被页面和测试共同调用的后端服务。

