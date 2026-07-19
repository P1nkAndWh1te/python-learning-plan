# Day 29：中文 Embedding 依赖评估记录

**日期**：2026年7月19日  
**项目**：RAG QA System  
**目标**：评估是否进入中文 embedding 模型实验

---

## 1. 当前环境

```text
Python: 3.13.2
pip: 24.3.1
```

当前相关包状态：

| Package | Status |
|---|---|
| chromadb | installed |
| onnxruntime | installed |
| torch | missing |
| sentence_transformers | missing |
| transformers | missing |

---

## 2. dry-run 结果

执行：

```powershell
python -m pip install --dry-run sentence-transformers
```

解析结果显示，如果安装 `sentence-transformers`，会准备安装：

```text
sentence-transformers 5.6.0
torch 2.13.0
transformers 5.14.1
tokenizers 0.22.2
safetensors 0.8.0
sympy 1.14.0
mpmath 1.3.0
```

其中 `torch-2.13.0-cp313-cp313-win_amd64.whl` 约 122.1 MB。

---

## 3. 判断

这条路线在当前 Python 3.13 + Windows 环境下看起来可以解析依赖，但它不是一个轻量改动。

原因：

- 会引入 PyTorch。
- 会引入 Transformers 生态依赖。
- 模型文件本身还需要后续下载。
- 首次运行速度和下载稳定性还需要实际验证。

所以不能在未确认的情况下直接安装并改主应用。

---

## 4. 推荐下一步

建议下一步分两段走：

### Step 1：确认是否安装依赖

如果接受安装成本，执行：

```powershell
python -m pip install sentence-transformers
```

### Step 2：安装后做独立中文 embedding 实验

继续保持不改主应用，先新增独立脚本：

```text
03_执行过程/day30_bge_embedding_eval/
```

实验目标：

```text
用 BAAI/bge-small-zh-v1.5 跑同一份 FAQ 和同一组 10 题评测
```

只有当中文 embedding 的检索结果明显优于当前 baseline，才考虑把主应用切换过去。

---

## 5. 今日结论

Day29 的核心结论：

```text
中文 embedding 是正确方向，但安装和模型运行成本需要用户明确确认。
```

当前项目继续保留：

```text
教学版关键词 embedding：主应用 baseline
Chroma 默认 embedding：真实 embedding 对照实验
中文 embedding：待确认后进入实验
```

