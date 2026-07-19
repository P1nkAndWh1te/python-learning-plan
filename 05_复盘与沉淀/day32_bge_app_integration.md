# Day 32：主应用接入 BGE 双模式

**日期**：2026年7月19日  
**项目**：RAG QA System  
**目标**：在 Streamlit 主应用中支持真实中文 embedding

---

## 1. 本次改动

主应用新增两种 embedding 模式：

```text
Teaching keyword embedding
BGE Chinese embedding
```

用户可以在侧边栏选择当前模式。

评测和问答共用同一个模式：

```text
选择模式 -> 文档切分 -> embedding -> Chroma 检索 -> DeepSeek 生成回答
```

---

## 2. 为什么保留教学版 embedding

教学版关键词 embedding 虽然不是真实语义 embedding，但它有两个价值：

- 便于解释向量维度和关键词命中。
- 可以作为 baseline 和真实 embedding 做对照。

所以 Day32 不直接替换，而是做双模式。

---

## 3. BGE 接入方式

模型：

```text
BAAI/bge-small-zh-v1.5
```

主应用通过 `sentence-transformers` 加载模型，并用 `st.cache_resource` 缓存模型对象。

这样可以避免 Streamlit 每次重新运行脚本时都重新加载模型。

---

## 4. 当前设计取舍

本次只做最小可用接入：

- 不做 rerank。
- 不做持久化 Chroma。
- 不修改 DeepSeek 生成逻辑。
- 不调整 UI 布局。
- 不删除教学版路径。

这样可以把风险限制在 embedding 和检索层。

---

## 5. 调试记录

第一次验证时发现一个维度冲突：

```text
Collection expecting embedding with dimension of 12, got 512
```

原因：

```text
教学版关键词 embedding 是 12 维
BGE 中文 embedding 是 512 维
两种向量不能写入同一个 Chroma collection
```

修复方式：

```text
Teaching keyword embedding -> uploaded_document_chunks_keyword
BGE Chinese embedding -> uploaded_document_chunks_bge
```

不同 embedding 维度使用不同 collection。

---

## 6. 验证结果

主应用语法检查通过。

独立函数验证：

```text
Teaching keyword embedding hit rate: 60%
BGE Chinese embedding hit rate: 80%
```

说明主应用已经能用两种模式运行同一组 10 题评测。

---

## 7. 下一步

Day33 建议处理用户体验和性能：

- BGE 首次加载提示。
- 模型缓存说明。
- 是否在页面显示 top-k recall。
- 是否增加 rerank 前的失败题观察表。
