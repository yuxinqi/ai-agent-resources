---
id: gs-first-agent
title: 构建你的第一个 Agent
type: getting-started
level: beginner
status: draft
evidence_level: L2
practical_rating: A
last_reviewed: "2026-05-08"
valid_until: "2026-08-08"
related:
  - gs-overview
  - gs-agent-basics
  - concept-tool-use
  - playbook-tool-agent
depends_on:
  - gs-agent-basics
tags:
  - getting-started
  - hands-on
  - tool-calling
---

# 构建你的第一个 Agent

本文将带你从零构建一个简单的 Tool-Calling Agent。完成后，你将拥有一个能调用工具、多步推理、自主完成任务的 Agent。

## 目标

构建一个"天气助手"Agent，它能：
1. 查询城市天气
2. 根据天气给出穿衣建议
3. 支持多城市对比

## 前置条件

- Python 3.10+
- OpenAI API Key（或其他支持 Function Calling 的模型）
- 基本理解 [Agent 基础概念](01-agent-basics.md)

## Step 1：定义工具

工具是 Agent 的"手和脚"。我们先定义两个工具：

```python
import json
from datetime import datetime

# 模拟天气数据
WEATHER_DATA = {
    "北京": {"temp": 22, "condition": "晴", "humidity": 45, "wind": "微风"},
    "上海": {"temp": 26, "condition": "多云", "humidity": 72, "wind": "东南风3级"},
    "深圳": {"temp": 30, "condition": "阵雨", "humidity": 85, "wind": "南风2级"},
    "成都": {"temp": 20, "condition": "阴", "humidity": 68, "wind": "微风"},
}

def get_weather(city: str) -> str:
    """获取指定城市的当前天气信息"""
    data = WEATHER_DATA.get(city)
    if not data:
        return json.dumps({"error": f"未找到城市 {city} 的天气数据"}, ensure_ascii=False)
    return json.dumps({
        "city": city,
        "temp": data["temp"],
        "condition": data["condition"],
        "humidity": data["humidity"],
        "wind": data["wind"],
        "queried_at": datetime.now().isoformat()
    }, ensure_ascii=False)

# 工具的 JSON Schema 定义（LLM 需要这个来理解工具）
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的当前天气信息，包括温度、天气状况、湿度和风力",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，如'北京'、'上海'、'深圳'、'成都'"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

# 工具名到函数的映射
tool_map = {
    "get_weather": get_weather,
}
```

**要点**：工具的 `description` 必须清晰完整——LLM 完全依赖它来决定何时调用。

## Step 2：构建 Agent 循环

Agent 的核心是一个**循环**：LLM 思考 → 调用工具 → 获取结果 → 再思考，直到任务完成。

```python
from openai import OpenAI

client = OpenAI()

SYSTEM_PROMPT = """你是一个天气助手。你可以查询城市的天气信息，并根据天气给出实用的建议。
当用户问多个城市的天气时，逐一查询后给出对比分析。
回答时使用中文。"""

def run_agent(user_message: str, max_turns: int = 5) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ]

    for turn in range(max_turns):
        # 1. LLM 思考
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        assistant_message = response.choices[0].message
        messages.append(assistant_message)

        # 2. 检查是否需要调用工具
        if not assistant_message.tool_calls:
            # LLM 认为任务完成，返回最终回答
            return assistant_message.content

        # 3. 执行所有工具调用
        for tool_call in assistant_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            print(f"  [Tool Call] {function_name}({function_args})")

            # 执行工具
            result = tool_map[function_name](**function_args)

            # 4. 将结果回传给 LLM
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

    return "Agent 达到最大轮次限制，未能完成任务。"
```

## Step 3：运行 Agent

```python
# 单城市查询
result = run_agent("北京今天天气怎么样？适合出门吗？")
print(result)

# 多城市对比
result = run_agent("帮我对比北京和上海的天气，我要出差该穿什么？")
print(result)
```

预期输出类似：

```
  [Tool Call] get_weather({"city": "北京"})

北京今天天气晴朗，气温22°C，湿度45%，微风。非常适合出门！建议穿薄外套或长袖衫...

  [Tool Call] get_weather({"city": "北京"})
  [Tool Call] get_weather({"city": "上海"})

北京和上海天气对比：北京晴22°C，上海多云26°C。去上海更暖和但湿度高。建议北京穿薄外套，上海穿短袖带伞...
```

## 理解 Agent 循环

回顾刚才的流程：

```
用户输入 → LLM 思考 → 需要工具？ → 是 → 调用工具 → 结果回传 → LLM 再思考 → ...
                                        → 否 → 返回最终回答
```

这就是最简单的 Agent 循环（ReAct 模式的简化版）。LLM 在每一步都自主决定下一步做什么——是调用工具还是直接回答。

## 关键学习点

1. **工具定义是关键**：LLM 的决策质量直接取决于工具描述的清晰度
2. **循环要有上限**：`max_turns` 防止 Agent 无限循环
3. **System Prompt 定调**：通过 System Prompt 控制 Agent 的行为边界和风格
4. **工具结果要结构化**：JSON 格式的结果让 LLM 更容易理解和推理

## 常见问题

**Q: Agent 一直调用同一个工具怎么办？**
A: 检查工具描述是否让 LLM 误以为需要重复调用。在 System Prompt 中明确"每个城市只需查询一次"。

**Q: Agent 调用了不存在的参数？**
A: 确保 JSON Schema 定义完整，`required` 字段正确，description 中列举了合法值。

**Q: 如何让 Agent 在错误时重试？**
A: 工具返回错误信息后，LLM 通常会自动调整。如果不行，在 System Prompt 中加入"如果工具返回错误，请尝试其他方式"。

## 下一步

- 学习 [Agent 评估入门](03-agent-evaluation-basics.md) 来判断你的 Agent 是否真的好用
- 阅读 [Tool Use 概念卡片](../concepts/tool-use.md) 深入理解工具使用的最佳实践
- 尝试 [Tool Agent Playbook](../playbooks/build-tool-using-agent.md) 构建更复杂的 Agent
