# Day 33：评测指标展示与 BGE 体验优化

**日期**：2026年7月19日  
**项目**：RAG QA System  
**目标**：改进主应用中的检索评测展示

---

## 1. 本次改动

主应用新增：

```text
calculate_top_k_hit_rate
```

页面评测区从单一 `Hit rate` 改成两个指标：

```text
Top-1 hit
Top-k recall
```

BGE 模式下，侧边栏会提示：

```text
BGE mode loads a local Chinese embedding model. The first evaluation or question may take longer.
```

---

## 2. 为什么要分开显示

`Top-1 hit` 表示第一名检索结果是否就是 expected chunk。

`Top-k recall` 表示 expected chunk 是否出现在前 k 个候选结果里。

在 RAG 中，这两个指标代表不同问题：

- Top-1 低：排序可能有问题。
- Top-k 低：召回可能有问题。

如果只显示一个命中率，会掩盖这两类问题的区别。

---

## 3. 当前验证结果

通过独立脚本验证：

```text
Teaching keyword embedding: Top-1 60%, Top-k 100%
BGE Chinese embedding: Top-1 80%, Top-k 100%
```

这说明：

- 两种模式都能召回正确 chunk。
- BGE 的第一名排序更好。
- 当前下一步更适合优化排序、体验或扩展评测集，而不是继续盲目换 embedding。

---

## 4. 当前设计取舍

本次没有引入 rerank。

原因：

- 当前 top-k recall 已经是 100%。
- 先把指标展示清楚，比立刻增加新模型链路更稳。
- 初学阶段需要先理解检索评测，而不是堆更多组件。

---

## 5. 下一步建议

Day34 可以从两个方向选一个：

```text
方向 A：优化页面体验和 README，让项目更像可展示作品
方向 B：开始引入 rerank 概念，解释为什么 top-k 召回后还需要重排序
```

当前更推荐方向 A，因为主链路已经跑通，先把作品整理清楚更有价值。

