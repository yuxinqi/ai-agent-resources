---
id: platform-changelog
title: 平台变更日志
type: platform
level: beginner
status: draft
evidence_level: L1
practical_rating: B
last_reviewed: "2026-05-08"
valid_until: "2026-08-08"
related:
  - platform-matrix
  - platform-api-comparison
  - platform-cost-latency
depends_on: []
tags:
  - platform
  - changelog
  - updates
  - reference
---

# 平台变更日志

记录影响 Agent 开发的重要平台变更，包括模型更新、API 变更、定价调整等。

> 本日志从 2026 年开始记录，仅包含对 Agent 开发有重大影响的变更。

## 2026 年

### 2026-05

| 日期 | 平台 | 变更 | 影响 |
|------|------|------|------|
| 2026-05-01 | OpenAI | GPT-4.1 正式发布，1M 上下文窗口 | 长上下文 Agent 场景可用，RAG Agent 受益 |
| 2026-05-01 | Anthropic | Claude Sonnet 4 发布，Tool Calling 增强 | 复杂工具调用场景首选更新 |

### 2026-04

| 日期 | 平台 | 变更 | 影响 |
|------|------|------|------|
| 2026-04-15 | Google | Gemini 2.5 Flash 支持 1M 上下文 | 低成本长上下文场景可选 |
| 2026-04-10 | OpenAI | GPT-4o-mini 价格下调 20% | 成本敏感场景进一步优化 |
| 2026-04-01 | 阿里云 | Qwen-Max 支持 OpenAI 兼容接口 | 迁移成本降低 |

### 2026-03

| 日期 | 平台 | 变更 | 影响 |
|------|------|------|------|
| 2026-03-20 | Anthropic | Claude Haiku 3.5 发布 | 高性价比 Agent 可选 |
| 2026-03-15 | DeepSeek | DeepSeek V3 API 开放 | 极低成本但稳定性待验证 |
| 2026-03-01 | Google | Gemini 2.5 Pro 支持 Function Calling 并行 | Agent 工具调用能力增强 |

### 2026-02

| 日期 | 平台 | 变更 | 影响 |
|------|------|------|------|
| 2026-02-20 | OpenAI | Structured Output 支持 Strict Mode | JSON 输出可靠性显著提升 |
| 2026-02-10 | 智谱 | GLM-4 Vision 能力增强 | 多模态 Agent 场景可选 |
| 2026-02-01 | Anthropic | Prompt Caching 正式 GA | 长上下文 Agent 成本降低 50% |

### 2026-01

| 日期 | 平台 | 变更 | 影响 |
|------|------|------|------|
| 2026-01-15 | OpenAI | Batch API 支持 GPT-4o | 离线处理场景成本减半 |
| 2026-01-10 | Google | Vertex AI Agent Builder 更新 | 低代码 Agent 构建选项 |
| 2026-01-01 | 阿里云 | Qwen 系列模型定价调整 | 部分模型价格下调 |

## 重要 API 变更

### OpenAI

| 版本 | 变更 | 迁移影响 |
|------|------|---------|
| v2 | `response_format` 参数变更 | 需更新 Structured Output 调用方式 |
| v2 | `tool_choice` 新增 `required` 选项 | 新功能，无需迁移 |
| v2 | Streaming 格式统一 | 需更新 SSE 解析逻辑 |

### Anthropic

| 版本 | 变更 | 迁移影响 |
|------|------|---------|
| 2024-01 | Tool Use API 格式更新 | 参数名从 `tools` 改为 `tool_use` |
| 2024-01 | 新增 `tool_choice` 参数 | 新功能 |
| 2025-01 | Message Batches API | 新功能，离线处理 |

### Google

| 版本 | 变更 | 迁移影响 |
|------|------|---------|
| v1beta | Function Calling 格式稳定 | 从 v1alpha 迁移需调整 |
| v1 | Gemini API 统一 | 从 PaLM 迁移需重写 |

## 已废弃功能

| 平台 | 功能 | 废弃日期 | 替代方案 |
|------|------|---------|---------|
| OpenAI | `code_interpreter` tool (旧版) | 2025-06 | Assistants API |
| OpenAI | GPT-3.5-turbo | 2025-09 | GPT-4o-mini |
| Anthropic | Claude 2.x 系列 | 2025-03 | Claude 3.5+ |
| Google | PaLM 2 | 2025-01 | Gemini 1.5+ |

## 订阅更新

建议关注以下渠道获取最新变更：

- OpenAI: https://platform.openai.com/docs/changelog
- Anthropic: https://docs.anthropic.com/changelog
- Google: https://ai.google.dev/changelog
- 阿里云: https://help.aliyun.com/product/610100.html
- 智谱: https://open.bigmodel.cn/dev/howuse/model

## 变更记录

| 日期 | 变更 |
|------|------|
| 2026-05-08 | 初始版本 |
