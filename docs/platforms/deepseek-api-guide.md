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

> DeepSeek 以极致性价比和开源模型著称，其 API 完全兼容 OpenAI SDK 格式。

---

## 一、平台概览

| 项目 | 内容 |
|------|------|
| 官网 | https://platform.deepseek.com |
| 核心模型 | DeepSeek-V3（通用）、DeepSeek-R1（推理增强） |
| 上下文窗口 | 128K tokens |
| 定价模式 | Pay-as-you-go（按 Token 计费） |
| 免费额度 | 新注册用户有 $5-10 额度 |
| 特色 | 极致性价比，兼容 OpenAI SDK，开源模型可自部署 |
| ⚠️ 状态 | ⏳ 待验真 |

## 二、申请流程

1. 访问 [https://platform.deepseek.com/sign_up](https://platform.deepseek.com/sign_up)
2. 注册账号（支持邮箱、手机号）
3. 登录后访问 [https://platform.deepseek.com/api_keys](https://platform.deepseek.com/api_keys)
4. 创建 API Key
5. 充值或使用免费额度

> 💡 中国区用户可直接访问，无需科学上网。

## 三、模型选择

| 模型 | 类型 | 适用场景 | 上下文 |
|------|------|---------|--------|
| `deepseek-chat` | 通用对话 | 日常问答、内容生成、代码 | 128K |
| `deepseek-reasoner` | 推理增强 | 复杂推理、数学、逻辑 | 128K |

**deepseek-chat (V3)**: 适合大多数日常使用，速度快、成本低。
**deepseek-reasoner (R1)**: 适合需要深度推理的任务（数学证明、复杂分析），响应较慢但推理能力强。

## 四、快速开始

### 4.1 基础调用

```python
from openai import OpenAI  # 兼容 OpenAI SDK

client = OpenAI(
    api_key="your-api-key",
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一位 AI 助手"},
        {"role": "user", "content": "介绍一下 DeepSeek 的主要特点"}
    ]
)

print(response.choices[0].message.content)
```

### 4.2 使用推理模型 (R1)

```python
response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=[
        {"role": "user", "content": "证明：根号2是无理数"}
    ],
    max_tokens=4096
)

print(response.choices[0].message.content)
```

### 4.3 流式传输 (Streaming)

```python
stream = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "讲个笑话"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

### 4.4 Function Calling

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名"}
                },
                "required": ["city"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "北京的天气怎么样？"}],
    tools=tools,
    tool_choice="auto"
)
```

## 五、定价参考

> ⚠️ 以下价格信息待验真。请以[官方定价页面](https://api-docs.deepseek.com/zh-cn/quick_start/pricing)为准。

| 模型 | 输入（每百万 token） | 输出（每百万 token） | 缓存命中 |
|------|---------------------|---------------------|---------|
| deepseek-chat | ~$0.27 | ~$1.10 | ~$0.07 |
| deepseek-reasoner | ~$0.55 | ~$2.19 | — |

相比 OpenAI GPT-4o（$2.50/$10.00），DeepSeek 的成本约为其 **1/10**，性价比极高。

## 六、特色亮点

1. **完全兼容 OpenAI SDK**：只需将 `base_url` 改为 `https://api.deepseek.com` 即可切换
2. **开源模型**：DeepSeek-V3 和 R1 均为开源，支持本地部署
3. **低延迟**：中国区节点响应速度快
4. **无需海外支付**：支持国内支付方式

## 七、注意事项

1. **速率限制**：免费用户和付费用户有不同的 Rate Limit，请查看[官方文档](https://api-docs.deepseek.com/zh-cn/quick_start/rate_limit)
2. **数据隐私**：API 请求数据默认不会用于模型训练，详见[隐私政策](https://platform.deepseek.com/privacy)
3. **服务稳定性**：高峰时段可能遇到限流，建议预留重试逻辑
4. **R1 模型**：推理模型不支持 streaming 模式下同时返回推理过程

## 八、相关资源

- [OpenAI API 指南](openai-api-guide.md) — 对比阅读（API 格式兼容）
- [API 平台综合对比](platform-comparison.md)
- [DeepSeek 官方文档](https://api-docs.deepseek.com/)
