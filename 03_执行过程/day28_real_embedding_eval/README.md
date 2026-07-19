# Day 28: Real Embedding Evaluation

This folder is an independent experiment for replacing the teaching keyword
embedding with Chroma's default embedding function.

It does not change the Streamlit RAG app.

## Goal

Run the same FAQ document and the same 10 retrieval evaluation questions with:

```text
Chroma default embedding function
Chroma cosine search
```

Then compare the result with the current teaching baseline:

```text
Teaching keyword embedding hit rate: 70%
```

## Run

From the project root:

```powershell
python "03_执行过程/day28_real_embedding_eval/real_embedding_eval.py"
```

