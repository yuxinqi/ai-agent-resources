---
title: Function Calling 机制
category: concepts
tags: [Function Calling, 工具调用, API, JSON Schema]
related:
  - agent-architecture.md
  - mcp-protocol.md
depends_on:
  - llm-basics.md
verification: false
created: 2026-05-07
updated: 2026-05-07
---

<!-- related_to: docs/concepts/agent-architecture.md, docs/concepts/mcp-protocol.md -->
<!-- depends_on: docs/concepts/llm-basics.md -->

# Function Calling 机制

## 📋 概念速览

| 项目 | 内容 |
|------|------|
| 定义 | LLM 根据用户指令，自动选择并生成调用外部工具的请求 |
| 首次提出 | OpenAI GPT-3.5 Turbo (2023 年 6 月) |
| 实现方式 | 在 API 请求中声明可用函数，模型返回调用意图 |
| 当前支持 | 所有主流 LLM 平台均支持 |
| ⚠️ 状态 | ⏳ 待验真 |

---

## 一、什么是 Function Calling

Function Calling（函数调用）是 LLM API 提供的一种能力：**开发者预定义一组函数（名称、描述、参数 Schema），LLM 在理解用户意图后，决定是否需要调用某个函数，并结构化地返回调用参数。**

### 与"LLM 生成代码执行"的区别

```
Function Calling:                LLM 生成代码:
LLM 返回 JSON 格式的函数调用      LLM 生成 Python/JS 代码
↓                                ↓
由客户端执行函数                  由沙箱执行代码
↓                                ↓
结果返回给 LLM 继续推理           结果返回给 LLM
✅ 安全、可控                    ⚠️ 有安全风险
```

## 二、工作原理

### 请求示例

```
用户: "北京的天气怎么样？"

API 请求:
- model: gpt-4o
- messages: [用户消息]
- tools: [
    {
      type: "function",
      function: {
        name: "get_weather",
        description: "获取指定城市的天气信息",
        parameters: {
          type: "object",
          properties: {
            city: { type: "string", description: "城市名称" }
          },
          required: ["city"]
        }
      }
    }
  ]

API 响应:
- 模型不直接回复文本
- 而是返回: tool_calls=[{name: "get_weather", args: {city: "北京"}}]
```

### 完整调用循环

```
用户请求 ──→ LLM 分析意图 ──→ 函数调用请求
                                  │
                                  ▼
                            执行函数（开发者侧）
                                  │
                                  ▼
                            返回函数结果 ──→ LLM 结合结果生成最终回复
```

## 三、主流平台对比

| 平台 | 接口名称 | Schema 格式 | 并行调用 | 特色 |
|------|---------|-----------|---------|------|
| OpenAI | `tools` | JSON Schema | ✅ | 最成熟 |
| Anthropic | `tools` | JSON Schema | ✅ | 可指定哪个工具必须用 |
| Google | `tools` | JSON Schema | ✅ | 支持递归 Schema |
| DeepSeek | `tools` | JSON Schema | ✅ | 兼容 OpenAI 格式 |
| 阿里 Qwen | `tools` | JSON Schema | ⚠️ | 兼容 OpenAI 格式 |

## 四、最佳实践

1. **函数名要语义化**：`get_weather` 好于 `func_1`
2. **描述要详细**：让模型理解何时该调用此函数
3. **参数 Schema 要精确**：枚举值用 enum，类型用 proper type
4. **错误处理**：函数返回结构化的错误信息
5. **限制调用次数**：设置 max_tool_calls 防止无限循环

## 五、相关资源

- [Agent 架构](agent-architecture.md) — Function Calling 是 Agent 的核心能力
- [MCP 协议](mcp-protocol.md) — 比 Function Calling 更进化的工具集成方案
- [OpenAI API 申请指南](../platforms/openai-api-guide.md)
