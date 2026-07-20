# Day 49：Evaluation Retrieval Modes

**日期**：2026年7月20日  
**项目**：DocuAsk v2  
**目标**：让 `/evaluation` 支持检索模式对比

---

## 1. 本次完成

`POST /evaluation` 新增：

```text
retrieval_mode
```

支持：

```text
vector
bm25
rrf
```

---

## 2. 为什么这一步重要

Day48 让 `/qa` 可以切换检索策略。

但单个问题只能说明“某次召回结果如何”。

`/evaluation` 支持 retrieval mode 后，可以用固定 10 题比较不同检索策略：

```text
vector Top-1 / Top-k
bm25 Top-1 / Top-k
rrf Top-1 / Top-k
```

这比主观判断更适合作为项目优化证据。

---

## 3. 字段变化

评估行中：

```text
best_distance
```

被泛化为：

```text
best_score
```

原因是不同检索模式的分数含义不同：

- vector：distance，越低越相似。
- bm25：score，越高越相关。
- rrf：rrf_score，越高排序越靠前。

---

## 4. 验证结果

独立脚本输出三种模式的对比表：

```text
Mode | Top-1 | Top-k
vector | ...
bm25 | ...
rrf | ...
```

pytest 覆盖：

```text
vector / bm25 / rrf / unknown mode
```

---

## 5. 下一步

下一步建议补充 API 文档和项目结构图。

当前后端已经有：

```text
/documents
/qa
/evaluation
vector / bm25 / rrf
pytest
```

这已经具备整理成项目介绍和面试讲解材料的基础。
