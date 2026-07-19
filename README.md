# project002Python学习计划

这是一个围绕 Python、LLM API、RAG 和项目实战展开的学习项目。所有计划、代码、材料、复盘和成果都集中在本 WorkSpace 项目目录下。

## 当前进度

- 当前日期：2026-07-19
- 当前学习日：Day 24
- 当前阶段：第三阶段 — RAG 项目实战
- 当前成果：已完成一个可运行的 Streamlit RAG QA 原型

## 核心成果

正式项目位于：

```text
04_成果输出/rag-qa-system/
```

当前 RAG QA System 已支持：

- 上传 TXT / Markdown 文档。
- 读取并预览文档内容。
- 优先按 Markdown `##` 标题切分文档。
- 使用教学版 embedding 和 Chroma cosine 检索。
- 展示检索上下文和来源引用。
- 调用 DeepSeek 基于检索上下文生成回答。
- 使用固定问题观察检索质量。

## 运行方式

在项目根目录运行：

```powershell
python -m streamlit run "04_成果输出/rag-qa-system/app.py"
```

如需启用 DeepSeek 生成回答，先在同一个 PowerShell 设置环境变量：

```powershell
$env:DEEPSEEK_API_KEY="your_api_key"
```

不要把 API Key 写进代码或提交到 GitHub。

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

## 关键记录

- RAG 核心链路复盘：`05_复盘与沉淀/day14_rag_core_review.md`
- 检索质量评测记录：`05_复盘与沉淀/day23_retrieval_evaluation_record.md`
- 正式项目 README：`04_成果输出/rag-qa-system/README.md`

## 当前限制

- 当前 embedding 是教学版关键词向量，不是真实语义 embedding。
- 暂不支持 PDF 解析。
- Chroma 当前使用临时 collection，没有持久化知识库。
- 评测问题目前为 5 个，后续需要扩展到 10 个固定问题。

## 建议工作流

1. 每天先读当天 `python-learning/daily-plan/`。
2. 在项目目录内完成当天代码或文档任务。
3. 将总结写入 `python-learning/learning-journal/`。
4. 用固定问题验证关键功能。
5. 提交并推送当天成果。
