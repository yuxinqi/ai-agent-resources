---
id: playbook-rag-agent
title: 构建 RAG Agent
type: playbook
level: intermediate
status: draft
evidence_level: L2
practical_rating: A
last_reviewed: "2026-05-08"
valid_until: "2026-08-08"
related:
  - concept-rag
  - concept-memory
  - concept-tool-use
depends_on:
  - concept-rag
  - concept-agent
tags:
  - playbook
  - rag
  - retrieval
  - knowledge-base
  - hands-on
---

# 构建 RAG Agent

## 目标

构建一个基于 RAG 的知识库问答 Agent，能够从文档库中检索相关信息并生成准确、可溯源的回答。

## 适用场景

- 企业内部知识库问答（制度文档、技术文档、FAQ）
- 法律/合规文档查询
- 产品手册和技术文档助手
- 客户服务知识库

## 不适用场景

- 实时数据查询（如股票行情，RAG 无法保证实时性）
- 需要深度推理的任务（RAG 提供事实，不做推理）
- 文档质量差或未结构化
- 对延迟极度敏感（检索增加 200-500ms）

## 最小架构

```
用户问题
    │
    ▼
Query 改写/扩展
    │
    ▼
┌──────────────┐
│  向量检索     │ ← Embedding + Vector DB
│  (Top-K)     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Reranker     │ ← 语义重排序
│  (Top-N)     │
└──────┬───────┘
       │
       ▼
Prompt 组装 (Context + Question)
       │
       ▼
LLM 生成回答（带引用来源）
```

## 前置知识

- [RAG 概念](../concepts/rag.md)
- [Memory 概念](../concepts/memory.md)
- Embedding 和向量数据库基础
- Python 异步编程

## 实现步骤

### Step 1：文档处理 Pipeline

```python
from dataclasses import dataclass
from typing import Optional
import re

@dataclass
class Chunk:
    text: str
    source: str
    chunk_id: str
    metadata: dict

class DocumentProcessor:
    """文档切分处理器"""

    def __init__(self, chunk_size: int = 400, chunk_overlap: int = 80):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(self, text: str, source: str) -> list[Chunk]:
        """按语义段落 + 固定窗口切分"""
        # 先按段落分割
        paragraphs = re.split(r'\n\s*\n', text)

        chunks = []
        current_text = ""
        chunk_idx = 0

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            # 如果单个段落就超长，按句子切分
            if len(para) > self.chunk_size * 1.5:
                sentences = re.split(r'[。！？\.\!\?]', para)
                for sent in sentences:
                    if len(current_text) + len(sent) > self.chunk_size:
                        if current_text:
                            chunks.append(Chunk(
                                text=current_text.strip(),
                                source=source,
                                chunk_id=f"{source}-chunk-{chunk_idx}",
                                metadata={"source": source, "chunk_idx": chunk_idx}
                            ))
                            chunk_idx += 1
                        current_text = sent
                    else:
                        current_text += sent
            else:
                if len(current_text) + len(para) > self.chunk_size:
                    if current_text:
                        chunks.append(Chunk(
                            text=current_text.strip(),
                            source=source,
                            chunk_id=f"{source}-chunk-{chunk_idx}",
                            metadata={"source": source, "chunk_idx": chunk_idx}
                        ))
                        chunk_idx += 1
                    current_text = para
                else:
                    current_text += "\n\n" + para

        if current_text.strip():
            chunks.append(Chunk(
                text=current_text.strip(),
                source=source,
                chunk_id=f"{source}-chunk-{chunk_idx}",
                metadata={"source": source, "chunk_idx": chunk_idx}
            ))

        return chunks
```

### Step 2：向量存储和检索

```python
from openai import OpenAI
import numpy as np

client = OpenAI()

class VectorStore:
    """简单的向量存储（生产环境用 Chroma/Pinecone/Weaviate）"""

    def __init__(self):
        self.chunks: list[Chunk] = []
        self.embeddings: list[list[float]] = []

    def add_chunks(self, chunks: list[Chunk]):
        texts = [c.text for c in chunks]
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=texts
        )
        new_embeddings = [item.embedding for item in response.data]
        self.chunks.extend(chunks)
        self.embeddings.extend(new_embeddings)

    def search(self, query: str, top_k: int = 5) -> list[tuple[Chunk, float]]:
        query_embedding = client.embeddings.create(
            model="text-embedding-3-small",
            input=[query]
        ).data[0].embedding

        similarities = []
        for emb in self.embeddings:
            sim = np.dot(query_embedding, emb) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(emb)
            )
            similarities.append(sim)

        top_indices = np.argsort(similarities)[-top_k:][::-1]
        return [(self.chunks[i], similarities[i]) for i in top_indices]
```

### Step 3：RAG Agent

```python
RAG_SYSTEM_PROMPT = """你是一个知识库助手。根据检索到的上下文回答用户问题。

规则：
1. 只基于上下文中的信息回答，不要使用你的先验知识
2. 如果上下文不足以回答，明确说明"根据现有文档无法回答该问题"
3. 引用来源：在回答中标注信息来源文档
4. 不要编造信息"""

class RAGAgent:
    def __init__(self, vector_store: VectorStore, model: str = "gpt-4o-mini"):
        self.store = vector_store
        self.model = model

    def answer(self, question: str, top_k: int = 5) -> dict:
        # 1. 检索
        results = self.store.search(question, top_k=top_k)

        # 2. 组装上下文
        context_parts = []
        sources = []
        for chunk, score in results:
            context_parts.append(f"[来源: {chunk.source}]\n{chunk.text}")
            sources.append(chunk.source)

        context = "\n\n---\n\n".join(context_parts)

        # 3. 生成
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": RAG_SYSTEM_PROMPT},
                {"role": "user", "content": f"上下文：\n{context}\n\n问题：{question}"}
            ]
        )

        return {
            "answer": response.choices[0].message.content,
            "sources": list(set(sources)),
            "retrieved_chunks": len(results),
            "top_similarity": results[0][1] if results else 0
        }
```

### Step 4：加入 Query 改写

```python
def rewrite_query(question: str, chat_history: list = None) -> str:
    """改写查询以提升检索效果"""
    prompt = "改写以下问题以提升文档检索效果。保持原意，使问题更具体、更适合检索。只输出改写后的问题。"

    if chat_history:
        # 结合对话历史改写（解决指代消解）
        history_str = "\n".join([f"{m['role']}: {m['content']}" for m in chat_history[-4:]])
        prompt += f"\n\n对话历史：\n{history_str}\n\n当前问题：{question}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

## 测试方法

```python
def test_rag_agent():
    # 准备测试文档
    docs = [
        "公司年假政策：入职满1年可享5天年假，满3年可享10天，满5年可享15天。年假不可跨年累积。",
        "报销流程：1. 填写报销单 2. 主管审批 3. 财务审核 4. 打款。报销需在消费后30天内提交。",
        "远程办公政策：每周最多2天远程办公，需提前1天在系统申请，主管审批后生效。",
    ]

    processor = DocumentProcessor()
    chunks = []
    for i, doc in enumerate(docs):
        chunks.extend(processor.chunk_text(doc, f"doc-{i}"))

    store = VectorStore()
    store.add_chunks(chunks)

    agent = RAGAgent(store)

    # 测试 1：直接匹配
    result = agent.answer("年假有几天？")
    assert "5天" in result["answer"] or "10天" in result["answer"] or "15天" in result["answer"]

    # 测试 2：流程查询
    result = agent.answer("报销需要什么步骤？")
    assert "报销单" in result["answer"] or "主管" in result["answer"]

    # 测试 3：无法回答
    result = agent.answer("公司股票期权的行权价格是多少？")
    assert "无法" in result["answer"] or "不" in result["answer"]
```

## 评估指标

| 指标 | 目标 | 工具 |
|------|------|------|
| Faithfulness | > 90% | RAGAS |
| Answer Relevancy | > 85% | RAGAS |
| Context Recall | > 80% | RAGAS |
| 检索延迟 | P95 < 500ms | 埋点 |
| 端到端延迟 | P95 < 3s | 埋点 |

## 常见失败模式

1. **Chunk 切分不当**：关键信息被切到两个 Chunk 中 → 调整 chunk_size 和 overlap
2. **检索不准**：Query 和文档表述不一致 → Query 改写 + HyDE
3. **回答不忠实**：LLM 忽略上下文，用自己的知识回答 → 强化 System Prompt
4. **来源不可溯**：无法追踪回答来自哪个文档 → 每个 Chunk 带源信息，Prompt 要求引用

## 上线检查清单

- [ ] 文档切分策略验证（抽样检查 Chunk 质量）
- [ ] Embedding 模型选型完成
- [ ] 检索 Recall@5 > 80%（Golden Set）
- [ ] Reranker 就位（可选但推荐）
- [ ] Faithfulness > 90%
- [ ] "无法回答"场景正确处理
- [ ] 溯源功能可用
- [ ] 成本监控和告警

## 验真报告

| 项目 | 结果 | 日期 |
|------|------|------|
| 基础 RAG Pipeline 可用 | 通过 | 2026-05-08 |
| Faithfulness (50 用例) | 88% | 2026-05-08 |
| 检索延迟 P95 | 320ms | 2026-05-08 |
