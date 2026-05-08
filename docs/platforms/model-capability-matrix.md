---
id: platform-matrix
title: 模型能力矩阵
type: platform
level: intermediate
status: draft
evidence_level: L2
practical_rating: A
last_reviewed: "2026-05-08"
valid_until: "2026-08-08"
related:
  - platform-api-comparison
  - platform-cost-latency
  - platform-changelog
depends_on: []
tags:
  - platform
  - model-comparison
  - capability-matrix
  - reference
---

# 模型能力矩阵

以下表格对比了主流 LLM 模型在 Agent 开发中的关键能力。数据基于公开文档和社区测试，**仅供参考**，实际表现可能因版本更新而变化。

> 最后验证：2026-05-08 | 有效期至：2026-08-08

## 综合能力对比

| 模型 | Tool Calling | Structured Output | Vision | Long Context | Streaming | Batch API |
|------|:---:|:---:|:---:|:---:|:---:|:---:|
| GPT-4o | ★★★ | ★★★ | ★★★ | 128K | ✅ | ✅ |
| GPT-4o-mini | ★★★ | ★★★ | ★★☆ | 128K | ✅ | ✅ |
| GPT-4.1 | ★★★ | ★★★ | ★★★ | 1M | ✅ | ✅ |
| Claude Sonnet 4 | ★★★ | ★★★ | ★★★ | 200K | ✅ | ✅ |
| Claude Haiku 3.5 | ★★☆ | ★★☆ | ★★☆ | 200K | ✅ | ✅ |
| Gemini 2.5 Pro | ★★★ | ★★★ | ★★★ | 1M | ✅ | ✅ |
| Gemini 2.5 Flash | ★★☆ | ★★☆ | ★★☆ | 1M | ✅ | ✅ |
| DeepSeek V3 | ★★☆ | ★★☆ | ★☆☆ | 128K | ✅ | ❌ |
| Qwen-Max | ★★☆ | ★★☆ | ★★☆ | 128K | ✅ | ✅ |
| GLM-4 | ★★☆ | ★★☆ | ★★☆ | 128K | ✅ | ✅ |

**评级说明**：★★★ = 优秀（生产可用） | ★★☆ = 良好（多数场景可用） | ★☆☆ = 基础（有限支持）

## Tool Calling 详细对比

| 模型 | 并行调用 | 参数准确率 | 复杂 Schema | 选择准确率(10+工具) | 强制调用 | 错误恢复 |
|------|:---:|:---:|:---:|:---:|:---:|:---:|
| GPT-4o | ✅ | 高 | ✅ | 高 | ✅ | 良好 |
| GPT-4o-mini | ✅ | 高 | ✅ | 中高 | ✅ | 良好 |
| GPT-4.1 | ✅ | 高 | ✅ | 高 | ✅ | 良好 |
| Claude Sonnet 4 | ✅ | 高 | ✅ | 高 | ✅ | 优秀 |
| Gemini 2.5 Pro | ✅ | 中高 | ✅ | 中高 | ✅ | 良好 |
| DeepSeek V3 | ✅ | 中 | ⚠️ | 中 | ⚠️ | 一般 |
| Qwen-Max | ✅ | 中高 | ✅ | 中 | ⚠️ | 一般 |

## 工程质量对比

| 模型 | Rate Limit | SDK 质量 | Observability | 文档质量 | 稳定性 | 成本效率 |
|------|:---:|:---:|:---:|:---:|:---:|:---:|
| GPT-4o | 中 | ★★★ | ★★★ | ★★★ | ★★★ | 中 |
| GPT-4o-mini | 高 | ★★★ | ★★★ | ★★★ | ★★★ | 高 |
| GPT-4.1 | 中 | ★★★ | ★★★ | ★★★ | ★★★ | 中 |
| Claude Sonnet 4 | 中 | ★★★ | ★★☆ | ★★★ | ★★★ | 中 |
| Claude Haiku 3.5 | 高 | ★★★ | ★★☆ | ★★★ | ★★★ | 高 |
| Gemini 2.5 Pro | 中 | ★★☆ | ★★☆ | ★★☆ | ★★☆ | 中高 |
| Gemini 2.5 Flash | 高 | ★★☆ | ★★☆ | ★★☆ | ★★☆ | 高 |
| DeepSeek V3 | 低 | ★★☆ | ★☆☆ | ★★☆ | ★★☆ | 极高 |
| Qwen-Max | 中 | ★★☆ | ★☆☆ | ★★☆ | ★★☆ | 高 |
| GLM-4 | 中 | ★★☆ | ★☆☆ | ★★☆ | ★★☆ | 高 |

## 选型建议

### 按 Agent 类型推荐

| Agent 类型 | 推荐模型 | 理由 |
|-----------|---------|------|
| Tool-Using Agent (生产) | GPT-4o / Claude Sonnet 4 | Tool Calling 稳定，错误恢复好 |
| Tool-Using Agent (成本敏感) | GPT-4o-mini / Claude Haiku 3.5 | 性价比高，工具调用准确率可接受 |
| RAG Agent | GPT-4.1 / Gemini 2.5 Pro | 长上下文优势 |
| Coding Agent | GPT-4.1 / Claude Sonnet 4 | 代码生成质量高 |
| Research Agent | GPT-4.1 / Gemini 2.5 Pro | 长上下文 + 信息整合能力强 |
| 高吞吐场景 | GPT-4o-mini / Gemini 2.5 Flash | Rate Limit 高，成本低 |

### 关键决策因素

1. **Tool Calling 质量优先**：选 GPT-4o 或 Claude Sonnet 4
2. **长上下文优先**：选 GPT-4.1 (1M) 或 Gemini 2.5 Pro (1M)
3. **成本优先**：选 GPT-4o-mini 或国产模型
4. **国内合规**：选 Qwen-Max 或 GLM-4
5. **多模态需求**：选 GPT-4o 或 Gemini 2.5 Pro

## 数据说明

- 以上数据基于 2026 年 5 月的模型版本
- "高/中/低" 为相对评级，非绝对量化
- 实际表现受 Prompt 设计、工具定义质量等因素影响
- 建议在选型后用自己的场景做 A/B 测试验证

## 变更记录

| 日期 | 变更 |
|------|------|
| 2026-05-08 | 初始版本，覆盖 10 个模型 |
