# Day 50：API 与架构文档沉淀

**日期**：2026年7月20日  
**项目**：DocuAsk v2  
**目标**：把当前后端能力整理成可展示、可复述、可验证的项目材料

---

## 1. 本次完成

新增：

```text
04_成果输出/rag-qa-system/API.md
04_成果输出/rag-qa-system/ARCHITECTURE.md
```

更新：

```text
04_成果输出/rag-qa-system/README.md
```

---

## 2. 为什么这一步重要

Day37 到 Day49 主要是在补工程能力：

```text
FastAPI
模块化 services
Chroma 持久化
pytest
BM25
RRF
retrieval_mode
evaluation
```

如果没有文档，面试表达容易退回到“我用了某某框架”。

Day50 的目标是把项目讲成：

```text
我拆分了哪些模块，解决了什么问题，用什么指标验证效果。
```

---

## 3. 当前可以准确表达的能力

当前可以说：

- 设计了 FastAPI 后端接口，提供文档入库、检索问答和检索评测能力。
- 拆分了 chunking、embedding、retrieval、evaluation、BM25、RRF 等 service。
- 构建了 Chroma 本地持久化知识库，避免服务重启后索引丢失。
- 接入了 vector、BM25、RRF 三种检索模式。
- 构建了 10 题固定检索评测，用 Top-1 hit 和 Top-k recall 量化召回质量。
- 使用 pytest 覆盖核心接口和错误分支。

---

## 4. 当前不能夸大的能力

当前仍不能说：

- 生产级系统。
- 多用户权限系统。
- PDF / Word 完整解析。
- 大规模评测。
- 已接入 rerank。
- FastAPI 后端已经完成 LLM answer 生成。

---

## 5. Day49 指标沉淀

当前 FAQ 文档上：

| Retrieval mode | Top-1 hit | Top-k recall |
|---|---:|---:|
| vector | 0.6 | 1.0 |
| bm25 | 0.8 | 1.0 |
| rrf | 0.9 | 1.0 |

这可以作为“对比和评估”的证据，但要说明数据集较小。

---

## 6. 下一步

下一步建议进入 Day51：

```text
给 FastAPI 增加可选 LLM 生成能力，或者新增独立 /answer endpoint。
```

这样后端链路可以从：

```text
documents -> qa -> retrieved context
```

升级为：

```text
documents -> qa -> answer with sources
```
