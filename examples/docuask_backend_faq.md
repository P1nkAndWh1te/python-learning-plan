# DocuAsk Backend FAQ

这份文档用于多文档检索评测。它和通用 RAG FAQ 不同，重点描述 DocuAsk 后端接口、文件上传和混合检索。

## FastAPI 后端负责什么？

FastAPI 后端负责把 DocuAsk 的 RAG 能力暴露成接口。当前接口包括 `/documents`、`/documents/upload`、`/qa`、`/answer` 和 `/evaluation`。这些接口分别处理文档入库、文件上传、检索问答、LLM answer 生成和检索评测。

## documents/upload 文件上传支持什么？

`/documents/upload` 使用 multipart 文件上传，当前支持 `.txt` 和 `.md` 文件。后端会读取文件内容，按 `utf-8` 或 `gbk` 解码，然后复用文档切分、embedding 和 Chroma 入库流程。

## RRF 混合检索有什么作用？

RRF 会融合 vector 向量检索和 BM25 关键词检索的排序结果。它的作用是让语义相似问题和关键词明确的问题都能有更稳定的召回表现。
