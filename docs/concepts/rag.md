---
id: concept-rag
title: RAG（检索增强生成）
type: concept
level: intermediate
status: draft
evidence_level: L2
practical_rating: A
last_reviewed: "2026-05-08"
valid_until: "2026-08-08"
related:
  - concept-memory
  - concept-agent
  - playbook-rag-agent
depends_on:
  - concept-agent
tags:
  - rag
  - retrieval
  - knowledge
  - core-concept
---

# RAG（检索增强生成）

## 一句话解释

RAG（Retrieval-Augmented Generation）是一种在 LLM 生成回答前先从外部知识库检索相关信息的架构，解决 LLM 知识过时和幻觉问题。

## 它解决什么问题

LLM 有三个根本性限制：
1. **知识截止**：训练数据有截止日期，不知道最新信息
2. **幻觉**：对不确定的问题会编造看似合理但错误的答案
3. **缺乏领域知识**：对企业内部文档、私有数据一无所知

RAG 通过"先检索、后生成"的范式解决这些问题：从外部知识库找到相关文档片段，将其作为上下文注入 Prompt，让 LLM 基于真实数据生成回答。

RAG 不是微调的替代品。微调改变模型的行为和能力，RAG 补充模型的即时知识。两者互补：微调教模型"怎么做"，RAG 告诉模型"知道什么"。

## 什么时候应该使用

- 需要引用准确的事实性信息（法律、医疗、财务）
- 知识频繁更新，不可能每次都微调模型
- 需要溯源，用户需要知道答案来自哪个文档
- 企业内部知识库问答

## 什么时候不应该使用

- 答案完全在 LLM 通用知识范围内（如常识问题）
- 知识库质量差，噪声多（垃圾进垃圾出）
- 需要深度推理而非信息检索（RAG 只提供事实，不做推理）
- 实时性要求极高（检索本身有延迟）

## 最小实践示例

```python
from openai import OpenAI
import numpy as np

client = OpenAI()

# 1. 文档切分
def chunk_documents(docs: list[str], chunk_size: int = 500) -> list[dict]:
    chunks = []
    for doc in docs:
        words = doc.split()
        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append({"text": chunk, "source": docs.index(doc)})
    return chunks

# 2. 向量化
def embed_texts(texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )
    return [item.embedding for item in response.data]

# 3. 检索
def retrieve(query: str, chunks: list[dict], chunk_embeddings: list[list[float]], top_k: int = 3):
    query_embedding = embed_texts([query])[0]
    similarities = [
        np.dot(query_embedding, emb) / (np.linalg.norm(query_embedding) * np.linalg.norm(emb))
        for emb in chunk_embeddings
    ]
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    return [chunks[i] for i in top_indices]

# 4. 生成
def rag_answer(query: str, retrieved_chunks: list[dict]) -> str:
    context = "\n\n".join([c["text"] for c in retrieved_chunks])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "基于以下上下文回答问题。如果上下文中没有相关信息，请说明。"},
            {"role": "user", "content": f"上下文：\n{context}\n\n问题：{query}"}
        ]
    )
    return response.choices[0].message.content
```

## 常见失败模式

1. **切分不当**：Chunk 太大导致检索不精确，太小导致上下文断裂。解法：按语义段落切分，chunk_size 300-500 tokens，overlap 50-100 tokens。

2. **检索质量差**：向量检索返回不相关文档。解法：优化 Embedding 模型选择、加入 Reranker、Query 改写。

3. **上下文过载**：塞入太多检索结果，LLM 被无关信息干扰。解法：控制 top_k（3-5 个），使用 Reranker 过滤。

4. **无法回答时硬编**：检索不到相关信息时，LLM 仍然编造答案。解法：在 Prompt 中明确"如果上下文不足以回答，请说明无法回答"。

5. **忽略检索结果**：LLM 忽略检索到的上下文，直接用自己的知识回答。解法：强调"必须基于上下文回答"，降低 temperature。

## 评估方法

| 维度 | 指标 | 方法 |
|------|------|------|
| 检索质量 | Recall@K, MRR | 标注相关文档，计算检索覆盖率 |
| 生成质量 | Faithfulness | 回答是否忠实于检索到的上下文 |
| 端到端 | Answer Accuracy | 最终回答是否正确 |
| 安全性 | Hallucination Rate | 回答中包含未在上下文中出现的事实比率 |

推荐评估框架：RAGAS（Retrieval Augmented Generation Assessment）

## 相关概念

- [Memory](memory.md) — RAG 是 Long-term Memory 的一种实现
- [Agent](agent.md) — Agent 可以用 RAG 作为知识获取手段
- [Build RAG Agent Playbook](../playbooks/build-rag-agent.md) — 端到端构建指南

## 验真状态

| 结论 | 证据等级 | 来源 |
|------|---------|------|
| RAG 比纯 LLM 在事实性问答上更准确 | L3 | 多个企业部署验证 |
| Reranker 显著提升检索质量（10-20%） | L2 | Cohere Rerank 论文 |
| Chunk 大小 300-500 tokens 在大多数场景下最优 | L1 | 社区实验 |
| Query 改写可提升检索召回率 | L2 | HyDE, Multi-Query 论文 |

## 参考来源

- Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (2020)
- Gao et al., "Retrieval-Augmented Generation for Large Language Models: A Survey" (2024)
- Es et al., "RAGAS: Automated Evaluation of Retrieval Augmented Generation" (2024)
- Cohere, "Reranker" Documentation (2024)
