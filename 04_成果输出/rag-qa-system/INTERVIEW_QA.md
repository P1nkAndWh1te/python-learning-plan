# DocuAsk 面试追问准备

本文档用于支撑 `RESUME_FINAL_DRAFT.md` 中的项目表述。原则是：只讲已经实现和验证过的内容，不把计划中的能力说成完成。

## 60 秒项目介绍

DocuAsk 是一个本地文档 RAG 问答系统。我用它验证了从 `.txt/.md` 文档上传、文本切分、embedding、Chroma 入库、检索召回、上下文组装、LLM 生成到来源引用的完整链路。

项目最初是 Streamlit 原型，后面我把核心逻辑拆成 `chunking`、`embedding`、`retrieval`、`generation`、`evaluation` 等模块，并补了 FastAPI 接口和 pytest 测试。检索侧支持 vector、BM25、RRF 三种模式，用 Top-1 hit 和 Top-k recall 做小样本评测；在当前 FAQ 测试集中，RRF 的 Top-1 hit 是 90%，Top-k recall 是 100%。

## 3 分钟项目说明

这个项目解决的是本地知识文档问答的可追溯问题。普通 LLM 直接回答时可能不知道资料内容，容易编造；RAG 的思路是先从本地知识库检索相关片段，再把片段交给模型生成回答，并展示来源。

我实现的流程是：用户上传 `.txt` 或 `.md` 文件，系统按 Markdown 二级标题优先切分，普通文本则按固定长度和 overlap 切分；每个 chunk 会被转换成 embedding，并写入 Chroma 本地持久化库。用户提问时，系统把问题也转换成 embedding，再按 vector、BM25 或 RRF 检索相关 chunk，最后把检索上下文交给 DeepSeek OpenAI-compatible API 生成答案。

工程上，我把原先页面里的 RAG 逻辑拆到后端模块，并提供 `/documents`、`/documents/upload`、`/qa`、`/answer`、`/evaluation` 接口。评测上，我用固定问题集检查 expected top chunk 是否命中，同时区分 Top-1 hit 和 Top-k recall，避免只看“有没有召回”而忽略第一名排序质量。

## 高频追问

### 1. 这个项目和直接问大模型有什么区别？

直接问大模型依赖模型已有知识，回答可能和本地资料不一致。DocuAsk 会先从本地文档中检索相关 chunk，再让 LLM 基于这些 chunk 回答，并展示来源。这样可以把回答约束在资料范围内，也便于检查答案依据。

### 2. RAG 的完整流程是什么？

离线或入库阶段：读取文档、切分 chunk、计算 embedding、写入向量数据库。在线问答阶段：把用户问题转换成 embedding，检索相似 chunk，组装上下文，交给 LLM 生成答案，最后返回答案和来源 chunk。

### 3. 为什么要做 chunking？

文档太长时，直接整体检索会让一个结果包含多个主题，召回不够精确；切得太碎又可能把完整语义拆断。当前项目优先按 Markdown `##` 标题切分，因为 FAQ 类文档天然按问题组织；普通文本再用固定长度和 overlap 兜底。

### 4. embedding 是什么？

embedding 是把文本转换成数字向量，让程序可以用距离或相似度比较两段文本是否相关。教学版关键词 embedding 用来解释原理；BGE 中文 embedding 用来做更接近真实语义检索的验证。

### 5. Chroma 在项目里负责什么？

Chroma 负责保存 chunk、metadata 和对应 embedding，并根据用户问题的 embedding 返回最相似的文档片段。当前使用本地 PersistentClient，因此重启后索引仍能保留在本地目录中。

### 6. 为什么 collection 要带 embedding 模式、schema version 和文档 hash？

不同 embedding 模式的向量维度不同，例如教学关键词向量和 BGE 向量不能混在同一个 collection。schema version 用于隔离索引结构变化，文档 hash 用于区分不同上传文档，避免旧索引和新文档混用。

### 7. vector、BM25、RRF 有什么区别？

vector 检索更偏语义相似度，适合问题和文档表达不完全一致的场景。BM25 更偏关键词匹配，适合术语、缩写、精确词命中的场景。RRF 是排序融合方法，把 vector 和 BM25 的排序结果合并，降低单一路径失效的风险。

### 8. RRF 为什么不直接把两个分数相加？

vector distance 和 BM25 score 的尺度不同，直接相加不稳定。RRF 更关注排名位置，常见思路是根据每个结果在不同检索器里的名次累加 `1 / (k + rank)`，这样不要求不同检索器的分数可比。

### 9. Top-1 hit 和 Top-k recall 分别说明什么？

Top-1 hit 看第一名是不是期望 chunk，反映排序质量。Top-k recall 看期望 chunk 是否进入前 k 个候选，反映是否召回到正确资料。RAG 中 Top-k recall 高但 Top-1 hit 低，说明资料找到了，但排序还可以优化。

### 10. 当前 90% / 100% 的评测结果怎么来的？

这是在当前 FAQ 小样本测试集上的检索评测结果。Day49 的对比里，RRF 在 10 个固定问题上 Top-1 hit 为 90%，Top-k recall 为 100%。这个结果可以证明当前样例下 RRF 比单一路径更稳，但不能说成大规模 benchmark。

### 11. 为什么 pytest 不直接调用真实 DeepSeek？

真实 LLM API 依赖 API Key、网络、额度和模型输出稳定性。自动化测试应该尽量可重复，所以当前测试重点覆盖文档入库、上传、检索、评测和异常分支；生成链路会验证缺少 API Key 等可控错误，真实回答通过手动运行验证。

### 12. 你处理了哪些异常？

已覆盖的异常包括：不支持的 embedding 模式、不支持的 retrieval mode、collection 不存在、不支持的上传文件类型、缺少 `DEEPSEEK_API_KEY` 等。这些异常能帮助定位问题发生在认证、检索还是生成阶段。

### 13. 这个项目目前最大的不足是什么？

当前仍是本地 RAG 原型，不是生产级系统。限制包括：只支持 `.txt/.md`，没有 PDF/Word 解析；评测集规模较小；没有 rerank；没有多用户权限；没有线上压测和监控。

### 14. 如果继续优化，你会先做什么？

优先做三件事：扩大评测集并沉淀失败案例；接入 rerank 改善 Top-1 排序；增加 PDF/Word 解析能力。之后再考虑 Docker 部署、鉴权、多用户隔离和更完整的日志监控。

## 简历逐条追问

### 简历点 1：完整 RAG 链路

可解释为：我不是只调了一个 LLM API，而是实现了从文档入库到检索生成的端到端流程。

证据：Streamlit 页面、`POST /documents`、`POST /qa`、`POST /answer`、来源 chunk 展示截图。

### 简历点 2：模块拆分和 FastAPI

可解释为：早期逻辑集中在页面里，不利于测试和复用；后面拆成服务模块，并通过 FastAPI 暴露接口。

证据：`backend/services/`、`backend/app.py`、`API.md`、pytest 接口测试。

### 简历点 3：Chroma 持久化和 collection 管理

可解释为：为了避免重启丢索引、不同 embedding 维度混用，我使用 PersistentClient，并把 collection 命名和 embedding 模式、schema version、文档 hash 绑定。

证据：`retrieval.py`、本地 `backend/storage/chroma_db_v2/`、相关测试。

### 简历点 4：vector / BM25 / RRF 和评测指标

可解释为：我没有只看页面能不能回答，而是把检索质量拆成可量化指标，并比较不同检索策略。

证据：`bm25.py`、`rrf.py`、`evaluation.py`、Day49 / Day53 评测记录。

### 简历点 5：pytest 和可复现材料

可解释为：我把核心接口和异常分支写成自动化测试，同时整理 API 文档、架构说明和截图清单，让项目可以被复现和检查。

证据：`tests/`、`API.md`、`ARCHITECTURE.md`、`SCREENSHOT_CHECKLIST.md`。

## 面试回答结构

回答项目追问时优先使用这个顺序：

1. 背景：为什么要做这个功能。
2. 问题：原来有什么缺陷或风险。
3. 行动：你具体改了什么。
4. 结果：用测试、指标或截图证明效果。
5. 边界：哪些能力还没做，不能夸大。

示例：

```text
早期版本只能在页面里跑通 RAG 演示，但逻辑不利于复用和测试。
我把文档切分、embedding、检索、生成和评测拆成独立模块，并补了 FastAPI 接口。
这样同一套 RAG 能力既能被 Streamlit 页面调用，也能通过 API 验证。
目前 pytest 覆盖了文档入库、上传、检索、评测和异常分支，检索侧用 Top-1 hit / Top-k recall 做了小样本评测。
边界是它还不是生产系统，暂不支持 PDF/Word、多用户权限和线上压测。
```

## 不能说的过度包装

- 不能说生产级 RAG 平台。
- 不能说支持 PDF / Word。
- 不能说已经上线或经过压测。
- 不能说做了大规模 benchmark。
- 不能说已经接入 rerank。
- 不能说解决了所有幻觉问题，只能说通过检索和来源引用降低幻觉风险。
