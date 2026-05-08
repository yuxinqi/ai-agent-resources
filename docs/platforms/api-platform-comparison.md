---
id: platform-api-comparison
title: API 平台对比
type: platform
level: intermediate
status: draft
evidence_level: L2
practical_rating: A
last_reviewed: "2026-05-08"
valid_until: "2026-08-08"
related:
  - platform-matrix
  - platform-cost-latency
  - platform-changelog
depends_on: []
tags:
  - platform
  - api-comparison
  - provider
  - reference
---

# API 平台对比

对比主流 LLM API 平台在 Agent 开发中的关键差异，帮助选择最适合的提供商。

> 最后验证：2026-05-08 | 有效期至：2026-08-08

## 平台概览

| 特性 | OpenAI | Anthropic | Google (Vertex AI) | 阿里云 (DashScope) | 智谱 AI |
|------|--------|-----------|-------------------|-------------------|---------|
| 主要模型 | GPT-4o, 4.1, 4o-mini | Claude Sonnet 4, Haiku 3.5 | Gemini 2.5 Pro/Flash | Qwen-Max, Plus | GLM-4 |
| API 兼容性 | OpenAI 格式（事实标准） | 自有格式 | 自有格式 | OpenAI 兼容 | OpenAI 兼容 |
| 国内可访问 | ❌ (需代理) | ❌ (需代理) | ❌ (需代理) | ✅ | ✅ |
| 免费额度 | 有限 | 有限 | 有 | 有 | 有 |
| 注册难度 | 中（需海外手机号） | 中 | 中 | 低 | 低 |

## Function Calling 支持

| 特性 | OpenAI | Anthropic | Google | DashScope | 智谱 |
|------|--------|-----------|--------|-----------|------|
| 基础 Function Calling | ✅ | ✅ | ✅ | ✅ | ✅ |
| 并行工具调用 | ✅ | ✅ | ✅ | ✅ | ✅ |
| tool_choice: required | ✅ | ✅ | ✅ | ⚠️ | ⚠️ |
| tool_choice: specific | ✅ | ✅ | ✅ | ⚠️ | ⚠️ |
| 流式工具调用 | ✅ | ✅ | ✅ | ⚠️ | ❌ |
| 强制 JSON Schema | ✅ | ✅ | ✅ | ⚠️ | ⚠️ |
| 最大工具数 | 128 | 128 | 64 | 32 | 32 |

## Structured Output 支持

| 特性 | OpenAI | Anthropic | Google | DashScope | 智谱 |
|------|--------|-----------|--------|-----------|------|
| JSON Mode | ✅ | ✅ | ✅ | ✅ | ✅ |
| JSON Schema 强制 | ✅ (Strict) | ✅ | ✅ | ⚠️ | ⚠️ |
| response_format | ✅ | ✅ | ✅ | ⚠️ | ⚠️ |
| Pydantic 集成 | ✅ (Instructor) | ✅ (Instructor) | ⚠️ | ❌ | ❌ |

## Streaming 和批处理

| 特性 | OpenAI | Anthropic | Google | DashScope | 智谱 |
|------|--------|-----------|--------|-----------|------|
| SSE Streaming | ✅ | ✅ | ✅ | ✅ | ✅ |
| Batch API | ✅ | ✅ | ✅ | ⚠️ | ❌ |
| Async 客户端 | ✅ | ✅ | ✅ | ✅ | ⚠️ |
| WebSocket | ❌ | ❌ | ⚠️ | ✅ | ❌ |

## 开发者体验

| 特性 | OpenAI | Anthropic | Google | DashScope | 智谱 |
|------|--------|-----------|--------|-----------|------|
| Python SDK | ★★★ | ★★★ | ★★☆ | ★★☆ | ★★☆ |
| TypeScript SDK | ★★★ | ★★★ | ★★☆ | ★☆☆ | ★☆☆ |
| API 文档 | ★★★ | ★★★ | ★★☆ | ★★☆ | ★★☆ |
| Playground | ★★★ | ★★★ | ★★☆ | ★★☆ | ★★☆ |
| 错误信息质量 | ★★★ | ★★★ | ★★☆ | ★★☆ | ★☆☆ |
| 社区生态 | ★★★ | ★★☆ | ★★☆ | ★★☆ | ★☆☆ |

## Observability 集成

| 工具 | OpenAI | Anthropic | Google | DashScope | 智谱 |
|------|--------|-----------|--------|-----------|------|
| LangSmith | ✅ | ✅ | ✅ | ⚠️ | ⚠️ |
| Helicone | ✅ | ✅ | ⚠️ | ❌ | ❌ |
| Datadog LLM | ✅ | ✅ | ✅ | ❌ | ❌ |
| 内置 Dashboard | ★★☆ | ★☆☆ | ★★★ | ★★☆ | ★★☆ |
| Usage API | ✅ | ✅ | ✅ | ✅ | ✅ |

## 选型决策树

```
是否需要国内直连？
├── 是 → 阿里云 DashScope / 智谱 AI
│         ├── 多模态+长上下文 → Qwen-Max
│         └── 高性价比 → GLM-4
└── 否 → 需要最强 Tool Calling？
          ├── 是 → OpenAI (GPT-4o) / Anthropic (Claude Sonnet 4)
          │         ├── 生态成熟度优先 → OpenAI
          │         └── 长上下文优先 → Anthropic
          └── 否 → 需要超长上下文？
                    ├── 是 → Google (Gemini 2.5 Pro, 1M)
                    └── 否 → 成本敏感？
                              ├── 是 → GPT-4o-mini / Gemini Flash
                              └── 否 → GPT-4o (综合最佳)
```

## 变更记录

| 日期 | 变更 |
|------|------|
| 2026-05-08 | 初始版本，覆盖 5 个平台 |
