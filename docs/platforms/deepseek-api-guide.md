---
title: DeepSeek API 使用指南
category: platforms
tags: [DeepSeek, API, 国产模型, 申请, 教程]
related:
  - openai-api-guide.md
  - platform-comparison.md
depends_on: []
verification: false
created: 2026-05-07
updated: 2026-05-07
---

<!-- related_to: docs/platforms/openai-api-guide.md, docs/platforms/platform-comparison.md -->

# DeepSeek API 使用指南

> 📅 **本文状态**：⏳ 待验真

## 一、平台概览

| 项目 | 内容 |
|------|------|
| 官网 | https://platform.deepseek.com |
| 核心模型 | DeepSeek-V3, DeepSeek-R1 |
| 定价模式 | Pay-as-you-go（按 Token 计费） |
| 免费额度 | 新注册用户有 $5-10 额度 |
| 特色 | 极致性价比，开源模型 |

## 二、申请流程

1. 访问 [https://platform.deepseek.com/sign_up](https://platform.deepseek.com/sign_up)
2. 注册账号（支持邮箱、手机号）
3. 登录后访问 [https://platform.deepseek.com/api_keys](https://platform.deepseek.com/api_keys)
4. 创建 API Key

## 三、快速开始

```python
from openai import OpenAI  # 兼容 OpenAI SDK

client = OpenAI(
    api_key="your-api-key",
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "user", "content": "Hello"}
    ]
)

print(response.choices[0].message.content)
```

## 四、特色亮点

- **兼容 OpenAI SDK**：只需修改 base_url 即可切换

## 五、相关资源

- [OpenAI API 指南](openai-api-guide.md) — 对比阅读
- [API 平台综合对比](platform-comparison.md)

---

## ✅ 验真记录

| 验真项 | 状态 | 验真日期 | 验真人 |
|--------|------|---------|--------|
| 注册流程 | ⏳ 待验真 | - | - |
| 当前价格 | ⏳ 待验真 | - | - |
| 免费额度 | ⏳ 待验真 | - | - |
| API 兼容性 | ⏳ 待验真 | - | - |
