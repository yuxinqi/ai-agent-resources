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

## 一、什么是 Embedding

Embedding 是将非结构化数据（文本、图像、音频等）映射到**高维向量空间**的技术。语义相似的内容在向量空间中距离更近。

```python
"猫"     → [0.12, -0.34, 0.56, ...]  # 3072 维向量
"狗"     → [0.15, -0.30, 0.52, ...]  # 与"猫"距离近
"汽车"   → [0.89, 0.12, -0.45, ...]  # 与"猫"距离远
```

**核心性质**：向量之间的距离（余弦相似度/欧氏距离）反映了语义相似度。

## 二、RAG 中的 Embedding 流程

详见 [RAG 检索增强生成](rag-retrieval.md)。

## 三、相关资源

- [RAG 检索增强生成](rag-retrieval.md)
- [从零搭建 RAG 系统](../workflows/build-rag-system.md)
