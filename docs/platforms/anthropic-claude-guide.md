---
title: Anthropic Claude API 申请指南
category: platforms
tags: [Anthropic, Claude, API, 申请, 教程]
related:
  - openai-api-guide.md
  - platform-comparison.md
depends_on:
  - ../concepts/llm-basics.md
verification: true
created: 2026-05-07
updated: 2026-05-07
---

<!-- related_to: docs/platforms/openai-api-guide.md, docs/platforms/platform-comparison.md -->

# Anthropic Claude API 申请指南

> 📅 **本文状态**：⏳ 待验真

## 一、平台概览

| 项目 | 内容 |
|------|------|
| 官网 | https://console.anthropic.com |
| 核心模型 | Claude 4 (Opus, Sonnet), Claude 3.5 (Haiku, Sonnet) |
| 定价模式 | Pay-as-you-go（按 Token 计费） |
| 免费额度 | 新注册用户有 $5 API 试用额度 |
| 支持地区 | 大部分国家和地区 |

## 二、申请流程

### 步骤 1：注册

1. 访问 [https://console.anthropic.com](https://console.anthropic.com)
2. 使用邮箱或 Google 账号注册
3. 验证邮箱
4. 可能需要手机验证

### 步骤 2：获取 API Key

1. 登录后访问 [https://console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)
2. 点击 "Create Key"
3. 命名并复制密钥

### 步骤 3：充值

访问 Billing 页面添加支付方式。

## 三、快速开始

```python
import anthropic

client = anthropic.Anthropic(
    api_key="your-api-key"
)

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude"}
    ]
)

print(message.content)
```

## 四、特色能力

| 能力 | 说明 |
|------|------|
| 超长上下文 | Claude 4 支持 200K tokens |
| Tool Use | 原生 Function Calling 支持 |
| MCP 协议 | Anthropic 是 MCP 的发起者 |
| 多模态 | 支持图像理解 |
| Computer Use | 支持浏览器/桌面操作（Beta） |

## 五、相关资源

- [OpenAI API 指南](openai-api-guide.md)
- [MCP 协议](../concepts/mcp-protocol.md)
- [API 平台综合对比](platform-comparison.md)

---

## ✅ 验真记录

| 验真项 | 状态 | 验真日期 | 验真人 |
|--------|------|---------|--------|
| 注册流程 | ⏳ 待验真 | - | - |
| 当前价格 | ⏳ 待验真 | - | - |
| 免费额度 | ⏳ 待验真 | - | - |
| 模型列表 | ⏳ 待验真 | - | - |
