# project002Python学习计划

这是一个围绕 Python、LLM API、RAG 和项目实战展开的学习项目。所有计划、代码、材料、复盘和成果都集中在本 WorkSpace 项目目录下。

## 当前进度

- 当前日期：2026-07-19
- 当前学习日：Day 34
- 当前阶段：第三阶段 — RAG 项目实战与作品化整理
- 当前成果：已完成一个可运行、可评测、支持真实中文 embedding 的 Streamlit RAG QA 原型

## 核心成果

正式项目位于：

```text
04_成果输出/rag-qa-system/
```

当前 RAG QA System 已支持：

- 上传 TXT / Markdown 文档。
- 读取并预览文档内容。
- 优先按 Markdown `##` 标题切分文档。
- 支持教学版关键词 embedding 和 BGE 中文 embedding 双模式。
- 使用 Chroma cosine 距离检索 Top 3 chunks。
- 展示检索上下文和来源引用。
- 调用 DeepSeek 作为 OpenAI-compatible LLM API 生成回答。
- 使用 10 个固定问题评测检索质量。
- 分开展示 Top-1 hit 和 Top-k recall。

## 当前评测结果

测试文档：

```text
02_资料与素材/day10_dify_knowledge/python_learning_faq.md
```

当前 10 题评测结果：

```text
Teaching keyword embedding: Top-1 60%, Top-k 100%
BGE Chinese embedding: Top-1 80%, Top-k 100%
```

结论：

```text
BGE 中文 embedding 当前排序效果更好；两种模式都能在 Top 3 内召回正确 chunk。
```

## 运行方式

先安装依赖：

```powershell
python -m pip install -r requirements.txt
```

启动应用：

```powershell
python -m streamlit run "04_成果输出/rag-qa-system/app.py"
```

如需启用 DeepSeek 生成回答，先在同一个 PowerShell 设置环境变量：

```powershell
$env:DEEPSEEK_API_KEY="your_api_key"
python -m streamlit run "04_成果输出/rag-qa-system/app.py"
```

注意：

- 不要把 API Key 写进代码。
- 不要把 API Key 提交到 GitHub。
- 没有 API Key 时，仍然可以体验上传、切分、embedding 和检索评测。

## 目录结构

```text
project002Python学习计划/
  01_需求与目标/        # 项目目标、验收标准
  02_资料与素材/        # 测试文档、知识库素材
  03_执行过程/          # 每日练习代码
  04_成果输出/          # 正式项目成果
  05_复盘与沉淀/        # 阶段复盘、评测记录
  python-learning/
    daily-plan/          # 每日学习计划
    learning-journal/    # 每日学习总结
```

## 关键文档

- 正式项目 README：`04_成果输出/rag-qa-system/README.md`
- 项目展示说明：`04_成果输出/rag-qa-system/PROJECT_BRIEF.md`
- 截图清单：`04_成果输出/rag-qa-system/SCREENSHOT_CHECKLIST.md`
- RAG 核心链路复盘：`05_复盘与沉淀/day14_rag_core_review.md`
- 真实 embedding 方案研究：`05_复盘与沉淀/day27_embedding_solution_research.md`
- BGE 评测结果：`05_复盘与沉淀/day30_bge_embedding_eval_result.md`
- 评测指标复盘：`05_复盘与沉淀/day31_evaluation_review.md`

## 当前限制

- 暂不支持 PDF 解析。
- Chroma 当前使用临时 collection，没有持久化知识库。
- BGE 模型首次加载需要等待。
- 当前还没有引入 rerank。
- 当前测试文档较小，后续需要扩展到更真实的多文档场景。

## 建议工作流

1. 每天先读当天 `python-learning/daily-plan/`。
2. 在项目目录内完成当天代码或文档任务。
3. 将总结写入 `python-learning/learning-journal/`。
4. 用固定问题验证关键功能。
5. 提交并推送当天成果。
