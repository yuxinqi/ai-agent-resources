---
id: concept-agent
title: Agent（智能体）
type: concept
level: beginner
status: draft
evidence_level: L2
practical_rating: A
last_reviewed: "2026-05-08"
valid_until: "2026-08-08"
related:
  - concept-tool-use
  - concept-planning
  - concept-memory
  - concept-multi-agent
depends_on: []
tags:
  - agent
  - core-concept
---

# Agent（智能体）

## 一句话解释

Agent 是一个以 LLM 为核心、能够自主感知环境、规划步骤、调用工具并完成目标的 AI 系统。

## 它解决什么问题

传统 LLM 只能生成文本回答，无法与外部世界交互。当你需要 AI 不仅"知道"还要"做到"时——比如查询数据库、调用 API、执行代码、操作文件——就需要 Agent。

Agent 解决的核心矛盾是：**LLM 有推理能力但没有行动能力，传统自动化有行动能力但没有推理能力**。Agent 将两者结合，让系统能处理需要理解、判断和执行的复合任务。

典型场景：
- 客户服务：理解用户意图 → 查询订单 → 发起退款 → 通知用户
- 数据分析：理解分析需求 → 编写 SQL → 执行查询 → 生成图表
- 代码开发：理解需求 → 搜索代码 → 编写代码 → 运行测试 → 修复错误

## 什么时候应该使用

- 任务需要**多步推理和决策**，无法一步完成
- 任务需要**与外部系统交互**（API、数据库、文件等）
- 任务路径**不确定**，需要根据中间结果动态调整
- 任务需要**组合多种能力**（搜索 + 分析 + 生成）

## 什么时候不应该使用

- 简单的文本生成任务（直接用 LLM 即可）
- 流程完全确定的任务（用传统工作流/DAG 更可靠）
- 对延迟极度敏感的场景（Agent 的多步推理会增加延迟）
- 对确定性要求极高的场景（Agent 的输出具有非确定性）

## 最小实践示例

```python
from openai import OpenAI
import json

client = OpenAI()

def search_docs(query: str) -> str:
    """搜索文档库"""
    return json.dumps({"results": [f"关于{query}的文档内容..."]})

tools = [{
    "type": "function",
    "function": {
        "name": "search_docs",
        "description": "在文档库中搜索相关内容",
        "parameters": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"]
        }
    }
}]

def agent(user_input: str) -> str:
    messages = [
        {"role": "system", "content": "你是一个文档助手，先搜索再回答。"},
        {"role": "user", "content": user_input}
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=messages, tools=tools
    )
    msg = response.choices[0].message
    if msg.tool_calls:
        for tc in msg.tool_calls:
            result = search_docs(**json.loads(tc.function.arguments))
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
        response = client.chat.completions.create(
            model="gpt-4o-mini", messages=messages
        )
        return response.choices[0].message.content
    return msg.content
```

## 常见失败模式

1. **无限循环**：Agent 反复调用相同工具或在不同状态间循环，没有终止条件。解法：设置 max_turns 上限。
2. **目标漂移**：Agent 在多步执行中逐渐偏离原始目标。解法：在 System Prompt 中强调核心目标，定期回顾。
3. **工具调用错误**：传递错误参数或调用不相关工具。解法：完善工具描述，添加参数校验。
4. **信息丢失**：长对话中遗忘早期信息。解法：使用 Memory 机制，关键信息显式存储。
5. **过度自信**：Agent 确信错误答案是正确的。解法：引入验证步骤或 Human-in-the-Loop。

## 评估方法

| 维度 | 指标 | 方法 |
|------|------|------|
| 任务完成率 | Success Rate | Golden Set + 自动/人工判断 |
| 过程效率 | Average Steps | Trace 统计，与基线对比 |
| 成本效率 | Tokens per Task | Token 计数 |
| 稳定性 | Variance over Runs | 同一输入跑 N 次统计 |
| 安全性 | Violation Rate | 安全测试集 + 规则检查 |

## 相关概念

- [Tool Use](tool-use.md) — Agent 的行动机制
- [Planning](planning.md) — Agent 的规划能力
- [Memory](memory.md) — Agent 的记忆机制
- [Multi-Agent](multi-agent.md) — 多 Agent 协作
- [Evaluation](evaluation.md) — Agent 评估方法

## 验真状态

| 结论 | 证据等级 | 来源 |
|------|---------|------|
| Agent 比纯 LLM 在工具调用任务上更有效 | L2 | OpenAI cookbook, LangChain benchmarks |
| Agent 循环需要 max_turns 上限 | L3 | 多个生产系统经验 |
| 过度规划反而降低简单任务效率 | L1 | 社区讨论和初步实验 |

## 参考来源

- OpenAI Cookbook: How to build an Agent (2024)
- Andrew Ng, "AI Agentic Workflows" (2024)
- Harrison Chase, "LangChain and the Future of AI Agents" (2024)
- Lilian Weng, "LLM Powered Autonomous Agents" (2023)
