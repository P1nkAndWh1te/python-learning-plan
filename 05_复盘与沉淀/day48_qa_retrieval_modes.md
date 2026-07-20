# Day 48：QA Retrieval Modes

**日期**：2026年7月20日  
**项目**：DocuAsk v2  
**目标**：让 `/qa` 支持显式检索模式切换

---

## 1. 本次完成

`POST /qa` 新增参数：

```text
retrieval_mode
```

支持：

```text
vector
bm25
rrf
```

默认仍然是：

```text
vector
```

---

## 2. 为什么要显式 mode

如果直接把 `/qa` 默认行为改成 RRF，会有两个问题：

- 旧测试和旧演示行为会被隐式改变。
- 出现问题时难以判断是 vector、BM25 还是 RRF 引起的。

显式 `retrieval_mode` 更适合调试和展示。

---

## 3. 返回字段变化

`retrieved_chunks` 现在支持：

```text
distance
score
rrf_score
```

不同 mode 使用不同字段：

- vector：主要看 `distance`。
- bm25：主要看 `score`。
- rrf：主要看 `rrf_score`。

---

## 4. 验证结果

独立验证：

```text
Mode: vector | Top chunk: 6
Mode: bm25 | Top chunk: 6
Mode: rrf | Top chunk: 6
Unknown mode status: 400
```

pytest 覆盖：

```text
vector / bm25 / rrf / unknown mode
```

---

## 5. 下一步

下一步建议给 `/evaluation` 也增加 retrieval mode。

这样就可以比较：

```text
vector Top-1 / Top-k
bm25 Top-1 / Top-k
rrf Top-1 / Top-k
```

这会成为项目优化效果的关键证据。
