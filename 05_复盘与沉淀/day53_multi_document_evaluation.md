# Day 53：Multi-document Evaluation

**日期**：2026年7月20日  
**项目**：DocuAsk v2  
**目标**：把固定问题评测扩展为多文档小样本评测

---

## 1. 本次完成

`POST /evaluation` 新增可选字段：

```text
evaluation_cases
```

如果不传，继续使用默认 10 题 FAQ 评测。

如果传入，则按自定义问题和 expected top chunk 评测。

---

## 2. 新增样本文档

新增：

```text
02_资料与素材/day53_multi_document_eval/docuask_backend_faq.md
```

这份文档用于评测：

- FastAPI 后端接口。
- `/documents/upload` 文件上传。
- RRF 混合检索。

---

## 3. 为什么这一步重要

之前的评测只证明：

```text
当前 FAQ 文档上的 10 题表现
```

Day53 后，可以表达为：

```text
构建了支持自定义问题集的检索评测接口，可对不同文档配置不同 evaluation cases。
```

这比只写一个固定 FAQ 更接近真实项目。

---

## 4. 当前边界

当前仍然只是小样本评测：

```text
2 份文档
13 个问题
```

不能夸大为大规模 benchmark。

---

## 5. 下一步

下一步建议进入 Day54：

```text
整理最终项目介绍和简历版本。
```

因为当前项目已经具备：

```text
FastAPI / Streamlit / Chroma / BGE / BM25 / RRF / Answer / Upload / Evaluation / pytest
```
