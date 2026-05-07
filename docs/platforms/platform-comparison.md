---
title: API 平台综合对比
category: platforms
tags: [对比, 选型, OpenAI, Anthropic, Google, DeepSeek]
related:
  - openai-api-guide.md
  - anthropic-claude-guide.md
  - deepseek-api-guide.md
depends_on: []
verification: false
created: 2026-05-07
updated: 2026-05-07
---

<!-- related_to: docs/platforms/openai-api-guide.md, docs/platforms/anthropic-claude-guide.md, docs/platforms/deepseek-api-guide.md -->
<!-- follows: docs/workflows/api-selection-migration.md -->

# API 平台综合对比

> 📅 **本文状态**：⏳ 待验真

## 一、主流平台一览

| 平台 | 代表模型 | 上下文 | 价格区间 | 免费额度 | 申请难度 |
|------|---------|--------|---------|---------|---------|
| OpenAI | GPT-4o, o3 | 128K | $$$ | $5-10 | 中 |
| Anthropic | Claude 4 Sonnet/Opus | 200K | $$$ | $5 | 中 |
| Google | Gemini 2.5 Flash/Pro | 1M+ | $-$$ | 有免费层 | 中 |
| DeepSeek | V3, R1 | 128K | $ | $5-10 | 低 |
| 阿里 Qwen | Qwen-Max, Qwen-Plus | 128K | $-$$ | 有免费额度 | 低 |
| 百度 ERNIE | ERNIE 4.5, 4.0 Turbo | 128K | $-$$ | 有免费额度 | 低 |
| Moonshot | Kimi k1.5 | 128K | $-$$ | 有免费额度 | 中 |
| Groq | LLaMA 3, Mixtral | 视模型而定 | $ | 有免费层 | 低 |
| Together AI | 多种开源模型 | 视模型而定 | $ | $25 试用 | 低 |

## 二、模型能力对比

| 能力维度 | GPT-4o | Claude 4 Sonnet | Gemini 2.5 Pro | DeepSeek-V3 |
|---------|--------|----------------|---------------|-------------|
| 推理能力 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 代码能力 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 中文能力 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 成本效益 | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 工具调用 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 多模态 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |

## 三、选型建议

### 🎯 通用开发 → OpenAI GPT-4o
生态最成熟，文档最完善，社区最活跃。

### 🎯 复杂推理 + 工具调用 → Anthropic Claude 4
Agent 场景表现突出，Claude Code / MCP 生态领先。

### 🎯 超长上下文 → Google Gemini 2.5 Pro
百万级上下文窗口，适合处理超大文档。

### 🎯 高性价比 → DeepSeek-V3
中文能力强，价格低，开源可自部署。

### 🎯 国内合规 → 阿里 Qwen / 百度 ERNIE
符合国内监管要求，可直接访问。

## 四、相关资源

- [OpenAI API 指南](openai-api-guide.md)
- [Anthropic Claude API 指南](anthropic-claude-guide.md)
- [DeepSeek API 指南](deepseek-api-guide.md)
- [API 选型与迁移流程](../workflows/api-selection-migration.md)
