---
title: Embedding 与向量数据库
category: concepts
tags: [Embedding, 向量数据库, 语义搜索, RAG]
related:
  - rag-retrieval.md
depends_on:
  - llm-basics.md
verification: false
created: 2026-05-07
updated: 2026-05-07
---

<!-- related_to: docs/concepts/rag-retrieval.md -->

# Embedding 与向量数据库

## 📋 概念速览

| 项目 | 内容 |
|------|------|
| Embedding | 将文本/图像等数据转换为向量（数值数组）表示 |
| 向量数据库 | 专门存储和检索向量的数据库系统 |
| 核心能力 | 语义相似度搜索（找"意思相近"而不是"关键词匹配"） |
| 应用场景 | RAG、语义搜索、推荐系统、聚类分析 |
| ⚠️ 状态 | ⏳ 待验真 |

---

Embedding 和向量数据库的详细内容已整合到 [RAG 检索增强生成](rag-retrieval.md) 文档中，包括：

- Embedding 模型对比（text-embedding-3、Cohere、bge 等）
- 向量搜索算法（HNSW、IVF）
- 距离度量（余弦、欧几里得、点积）
- 主流向量数据库对比（Chroma、Qdrant、Pinecone、Milvus、pgvector）
- 在 RAG 中的完整应用流程

> 如需实际操作，请参考 [从零搭建 RAG 系统](../workflows/build-rag-system.md)
