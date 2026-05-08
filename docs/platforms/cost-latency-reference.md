---
id: platform-cost-latency
title: 成本与延迟参考
type: platform
level: intermediate
status: draft
evidence_level: L1
practical_rating: B
last_reviewed: "2026-05-08"
valid_until: "2026-08-08"
related:
  - platform-matrix
  - platform-api-comparison
depends_on: []
tags:
  - platform
  - cost
  - latency
  - reference
---

# 成本与延迟参考

提供主流模型在 Agent 场景下的成本和延迟参考数据，帮助估算和优化。

> **重要提示**：价格和延迟随时间变化，以下数据仅供参考。实际数据请以官方定价页面为准。
> 最后验证：2026-05-08 | 有效期至：2026-08-08

## 定价参考

### 按模型定价（每百万 Token）

| 模型 | 输入价格 | 输出价格 | 缓存输入 | Batch 折扣 |
|------|---------|---------|---------|-----------|
| GPT-4o | $2.50 | $10.00 | $1.25 | 50% |
| GPT-4o-mini | $0.15 | $0.60 | $0.075 | 50% |
| GPT-4.1 | $2.00 | $8.00 | $0.50 | 50% |
| Claude Sonnet 4 | $3.00 | $15.00 | $0.30 | 50% |
| Claude Haiku 3.5 | $0.80 | $4.00 | $0.08 | 50% |
| Gemini 2.5 Pro | $1.25 | $10.00 | $0.30 | 50% |
| Gemini 2.5 Flash | $0.15 | $0.60 | $0.04 | 50% |
| DeepSeek V3 | $0.27 | $1.10 | $0.07 | N/A |
| Qwen-Max | ¥2.00 | ¥6.00 | N/A | N/A |
| GLM-4 | ¥5.00 | ¥50.00 | N/A | N/A |

> 价格可能已变更，请以官方页面为准。

### Agent 场景成本估算

典型 Agent 请求的 Token 消耗和成本：

| Agent 类型 | 平均 Input Tokens | 平均 Output Tokens | GPT-4o 成本 | GPT-4o-mini 成本 |
|-----------|:---:|:---:|---:|---:|
| 简单问答 | 500 | 200 | $0.003 | $0.0002 |
| 单步工具调用 | 1,500 | 400 | $0.008 | $0.0005 |
| 3 步 Agent | 4,000 | 800 | $0.018 | $0.001 |
| 5 步 Agent | 8,000 | 1,500 | $0.040 | $0.002 |
| RAG (5 chunks) | 6,000 | 500 | $0.020 | $0.001 |
| Research Agent | 30,000 | 3,000 | $0.105 | $0.007 |
| Coding Agent | 15,000 | 2,000 | $0.058 | $0.004 |

### 月度成本估算

| 日均请求 | 简单问答 (4o) | 3步Agent (4o) | 3步Agent (4o-mini) | 5步Agent (4o) |
|---------|:---:|:---:|:---:|:---:|
| 100 | $9 | $54 | $3 | $120 |
| 1,000 | $90 | $540 | $30 | $1,200 |
| 10,000 | $900 | $5,400 | $300 | $12,000 |
| 100,000 | $9,000 | $54,000 | $3,000 | $120,000 |

## 延迟参考

### 单次 API 调用延迟

| 模型 | TTFT P50 | TTFT P95 | Total P50 | Total P95 | 吞吐量 (tok/s) |
|------|:---:|:---:|:---:|:---:|:---:|
| GPT-4o | 0.4s | 1.0s | 1.5s | 4.0s | ~80 |
| GPT-4o-mini | 0.2s | 0.5s | 0.8s | 2.0s | ~120 |
| GPT-4.1 | 0.5s | 1.2s | 2.0s | 5.0s | ~60 |
| Claude Sonnet 4 | 0.3s | 0.8s | 1.5s | 4.0s | ~90 |
| Claude Haiku 3.5 | 0.15s | 0.4s | 0.6s | 1.5s | ~150 |
| Gemini 2.5 Pro | 0.5s | 1.5s | 2.0s | 6.0s | ~70 |
| Gemini 2.5 Flash | 0.2s | 0.5s | 0.8s | 2.0s | ~130 |
| DeepSeek V3 | 0.8s | 2.0s | 3.0s | 8.0s | ~40 |
| Qwen-Max | 0.5s | 1.5s | 2.5s | 6.0s | ~50 |
| GLM-4 | 0.6s | 1.8s | 3.0s | 7.0s | ~45 |

> TTFT = Time To First Token，Total = 完整响应时间

### Agent 端到端延迟

| Agent 类型 | GPT-4o P50 | GPT-4o-mini P50 | 优化建议 |
|-----------|:---:|:---:|------|
| 单步工具调用 | 2.5s | 1.5s | 使用 Streaming |
| 3 步 Agent | 6.0s | 3.5s | 并行工具调用 |
| 5 步 Agent | 12.0s | 7.0s | 减少步骤、使用小模型 |
| RAG (含检索) | 3.5s | 2.5s | 预计算 Embedding |
| Research Agent | 45s+ | 30s+ | 异步执行、并行搜索 |

## 成本优化策略

### 1. 模型分层

```
高价值请求 → GPT-4o / Claude Sonnet 4（高准确率）
普通请求 → GPT-4o-mini / Haiku 3.5（高性价比）
简单路由 → 规则/分类器（零 LLM 成本）
```

### 2. Caching

| 缓存类型 | 节省 | 适用场景 |
|---------|------|---------|
| Prompt Caching (API 级别) | 50% input | 重复 System Prompt |
| 语义缓存 | 30-80% | 相似问题 |
| 结果缓存 | 接近 100% | 完全相同请求 |

### 3. Token 优化

- 精简 System Prompt（每减少 100 tokens = 每百万请求省 $0.25-2.5）
- 工具描述按需加载（Router 模式只传相关工具）
- 对话历史摘要压缩（节省 60-80% context tokens）
- 使用 `max_tokens` 限制输出长度

## 变更记录

| 日期 | 变更 |
|------|------|
| 2026-05-08 | 初始版本 |
