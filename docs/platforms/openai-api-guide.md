---
title: OpenAI API 申请与使用指南
category: platforms
tags: [OpenAI, GPT, API, 申请, 教程]
related:
  - anthropic-claude-guide.md
  - platform-comparison.md
depends_on:
  - ../concepts/llm-basics.md
verification: true
created: 2026-05-07
updated: 2026-05-07
---

<!-- related_to: docs/platforms/anthropic-claude-guide.md, docs/platforms/platform-comparison.md -->

# OpenAI API 申请与使用指南

> 📅 **本文状态**：⏳ 待验真
> 计划验真内容：注册流程可用性、免费额度、当前价格、模型列表

## 一、平台概览

| 项目 | 内容 |
|------|------|
| 官网 | https://platform.openai.com |
| 核心模型 | GPT-4o, GPT-4o-mini, GPT-4.5, o3, o4-mini |
| 定价模式 | Pay-as-you-go（按 Token 计费） |
| 免费额度 | 新注册用户有 $5-10 试用额度（有一定时效限制） |
| 支持地区 | 大部分国家和地区（部分地区受限） |

## 二、申请流程

### 步骤 1：注册 OpenAI 账号

1. 访问 [https://platform.openai.com/signup](https://platform.openai.com/signup)
2. 使用邮箱或 Google/Microsoft 账号注册
3. 验证邮箱
4. 填写个人信息

> ⚠️ **待验真提醒**：注册流程可能因地区而异，部分国家/地区可能需要手机验证。

### 步骤 2：申请 API 密钥

1. 登录后访问 [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. 点击 "Create new secret key"
3. 为密钥命名（如 "my-project"）
4. 复制并安全保存密钥（关闭弹窗后不可再次查看）

> ⚠️ **安全提示**：API Key 请保存在环境变量中，不要提交到代码仓库。

### 步骤 3：绑定支付方式

1. 访问 [https://platform.openai.com/account/billing](https://platform.openai.com/account/billing)
2. 添加信用卡信息
3. 设置每月消费限额（Usage limits）

## 三、快速开始

### Python 示例

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-api-key"  # 建议使用环境变量
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "Hello!"}
    ]
)

print(response.choices[0].message.content)
```

### 环境变量设置

```bash
# Linux/Mac
export OPENAI_API_KEY="sk-xxxx"

# 或写入 .env 文件
echo "OPENAI_API_KEY=sk-xxxx" >> .env
```

## 四、定价参考

> ⚠️ **待验真**：以下价格为整理时参考值，实际以官网为准。

| 模型 | 输入价格 (per 1M tokens) | 输出价格 (per 1M tokens) |
|------|------------------------|-------------------------|
| GPT-4o | ~$2.50 | ~$10.00 |
| GPT-4o-mini | ~$0.15 | ~$0.60 |
| GPT-4.5 | ~$75.00 | ~$150.00 |
| o3 | 见官网 | 见官网 |

## 五、重要限制

| 限制项 | 说明 |
|-------|------|
| Rate Limit | 分层限制（Free / Tier 1-5），取决于使用历史 |
| 上下文窗口 | GPT-4o: 128K tokens |
| 知识截止 | 模型训练数据截止时间因模型版本而异 |
| 数据隐私 | API 调用数据默认不被用于训练（截至最新政策） |

## 六、常见问题

**Q: API Key 泄露了怎么办？**
A: 立即在 API Keys 页面撤销该密钥并重新生成。

**Q: 免费额度用完了还能用吗？**
A: 需要绑定支付方式后才能继续使用。

**Q: 中国地区能用吗？**
A: OpenAI 目前对中国大陆地区有服务限制，可能需要通过境外服务器中转。

## 七、相关资源

- [Anthropic Claude API 指南](anthropic-claude-guide.md) — 对比阅读
- [DeepSeek API 指南](deepseek-api-guide.md) — 国产替代方案
- [API 平台综合对比](platform-comparison.md)

---

## ✅ 验真记录

| 验真项 | 状态 | 验真日期 | 验真人 |
|--------|------|---------|--------|
| 注册流程 | ⏳ 待验真 | - | - |
| 当前价格 | ⏳ 待验真 | - | - |
| 免费额度 | ⏳ 待验真 | - | - |
| 模型列表 | ⏳ 待验真 | - | - |
