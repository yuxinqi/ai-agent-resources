---
title: RAG 检索增强生成
category: concepts
tags: [RAG, 检索, 向量数据库, Embedding]
related:
  - llm-basics.md
  - embedding-vector-db.md
depends_on:
  - llm-basics.md
verification: false
created: 2026-05-07
updated: 2026-05-07
---

<!-- related_to: docs/concepts/llm-basics.md, docs/concepts/embedding-vector-db.md -->

# RAG 检索增强生成

## 📋 概念速览

| 项目 | 内容 |
|------|------|
| 全称 | Retrieval-Augmented Generation (检索增强生成) |
| 核心思想 | 在生成回答前，先从外部知识库检索相关信息 |
| 优势 | 解决 LLM 的知识截止、幻觉、私有数据问题 |
| 适用场景 | 客服问答、知识库、企业文档、事实密集型任务 |
| ⚠️ 状态 | ⏳ 待验真 |

---

## 一、为什么需要 RAG

LLM 的固有限制：
- **知识截止**：训练数据有时间限制
- **幻觉**：不知道的内容会"编造"
- **私有数据**：无法访问企业内部知识
- **实时性**：无法获取最新信息

**RAG 的解法**：让 LLM 在回答前先"查资料"，基于检索到的真实信息生成回答。

## 二、RAG 架构

```
用户问题
    │
    ▼
┌─────────────────────────────┐
│     查询理解与优化           │
│  • 查询重写                 │
│  • 查询扩展                 │
│  • HyDE (假设性文档编码)     │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐    ┌──────────────────┐
│    向量检索 (ANN)           │◄───│  向量数据库       │
│  • 语义相似度搜索           │    │  • 文档经 Em-    │
│  • 关键词混合搜索           │    │    bedding 后存储  │
│  • 多路召回                 │    │  • Chroma/Pine-  │
└─────────────┬───────────────┘    │    cone/Qdrant    │
              │                    └──────────────────┘
              ▼
┌─────────────────────────────┐
│     结果重排序 (Rerank)     │
│  • 精排 Top-K               │
│  • 去重与过滤               │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│     LLM 生成回答            │
│  用户问题 + 检索上下文 → 回答 │
└─────────────────────────────┘
```

## 三、RAG 的三种模式

### 3.1 朴素 RAG (Naive RAG)

最简单：每次查询都检索 → 生成

```
用户提问 → 检索相关文档 → 拼接提示词 → LLM 生成
```

✅ 简单易实现 ❌ 检索质量不稳定

### 3.2 高级 RAG (Advanced RAG)

在检索前后增加优化环节：

```
预检索优化                       检索中优化                    检索后优化
• 查询重写 (Query Rewriting)    • 多路召回                     • 重排序
• 查询分解 (Query Decomposition) • 混合搜索 (语义+关键词)       • 上下文压缩
• HyDE                          • 多轮对话上下文               • 去重
```

### 3.3 模块化 RAG (Modular RAG)

将 RAG 流程模块化，支持灵活组合和流水线编排。是当前最成熟的演进版本，支持：

- **Search-Augmented Generation** — 深入搜索引擎
- **Agentic RAG** — 基于 Agent 的自我修正检索
- **Corrective RAG** — 自动验证检索结果质量
- **Speculative RAG** — 并行推演多条路径择优

## 四、关键组件

### 4.1 文档切分 (Chunking)

| 策略 | 方法 | 适用场景 |
|------|------|---------|
| 固定大小 | 按 Token 数切分 | 通用 |
| 语义切分 | 按段落/句子边界切分 | 文档结构清晰 |
| 递归切分 | 多级递归切分 | 复杂文档 |
| Agentic 切分 | 用 LLM 决定切分点 | 高质量场景 |

### 4.2 Embedding 模型

| 模型 | 开发商 | 维度 | 最大输入 |
|------|--------|------|---------|
| text-embedding-3-small | OpenAI | 512-1536 | 8K tokens |
| text-embedding-3-large | OpenAI | 256-3072 | 8K tokens |
| embeddings-v2 | Cohere | 1024-4096 | 8K tokens |
| bge-large | BAAI | 1024 | 512 tokens |

### 4.3 向量数据库

| 数据库 | 类型 | 部署方式 | 特色 |
|--------|------|---------|------|
| Chroma | 嵌入式 | 本地 | 轻量级，适合原型 |
| Qdrant | 专用向量 DB | 本地/云 | 高性能，生产级 |
| Pinecone | 托管服务 | 云 | 全托管，免运维 |
| Milvus | 分布式 | 本地/云 | 大规模，企业级 |
| pgvector | PostgreSQL 扩展 | 本地/云 | 与关系数据库集成 |

## 五、RAG 效果评估

| 维度 | 评估指标 | 说明 |
|------|---------|------|
| 检索质量 | Recall@K, MRR | 检索到的文档是否相关 |
| 生成质量 | Faithfulness, Answer Relevance | 回答是否忠实于检索结果 |
| 端到端 | Accuracy, F1 | 整体回答正确性 |

## 六、最佳实践

1. **文档质量 > 检索算法**：输入数据越干净，效果越好
2. **Hybrid Search > 纯向量搜索**：结合关键词 BM25 提高召回
3. **Rerank 不可省略**：精排 Top-K 质量提升明显
4. **查询重写提升大**：把"它"改写为具体实体
5. **监控检索质量**：低质量检索时降级处理

## 七、相关资源

- [LLM 基础](llm-basics.md)
- [Embedding 与向量数据库](embedding-vector-db.md)
- [从零搭建 RAG 系统](../workflows/build-rag-system.md)
- [API 平台综合对比](../platforms/platform-comparison.md)
