---
id: pattern-router
title: Router 模式
type: pattern
level: beginner
status: draft
evidence_level: L2
practical_rating: A
last_reviewed: "2026-05-08"
valid_until: "2026-08-08"
related:
  - pattern-planner-executor
  - concept-multi-agent
depends_on:
  - concept-agent
  - concept-tool-use
tags:
  - pattern
  - router
  - dispatch
  - intent-classification
---

# Router 模式

## 架构图

```
┌─────────────────────────────────────────────────┐
│                    用户输入                       │
└─────────────────────┬───────────────────────────┘
                      ▼
              ┌───────────────┐
              │    Router     │ ← 意图分类 + 路由决策
              │   (路由器)     │
              └───────┬───────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
  ┌───────────┐ ┌───────────┐ ┌───────────┐
  │ Agent A   │ │ Agent B   │ │ Agent C   │
  │ (领域A)   │ │ (领域B)   │ │ (领域C)   │
  └───────────┘ └───────────┘ └───────────┘
        │             │             │
        ▼             ▼             ▼
    最终输出      最终输出      最终输出
```

## 适用条件

- 系统需要处理**多种不同类型**的请求（如天气查询 + 计算器 + 文档搜索）
- 不同请求需要**不同的工具集和 Prompt**
- 意图可以**明确分类**到有限类别中（通常 3-10 类）
- 用户请求通常是**单一意图**（不是多意图混合）

## 不适用条件

- 请求类型只有 1-2 种（直接用单个 Agent 更简单）
- 意图无法清晰分类（模糊、多意图混合）
- 路由错误代价极高（如安全敏感操作误路由）
- 类别超过 15 个（Router 准确率显著下降）

## 最小代码示例

```python
from openai import OpenAI
import json

client = OpenAI()

# Router：意图分类
ROUTER_PROMPT = """你是一个意图分类器。根据用户输入，判断应该路由到哪个 Agent。

可选 Agent：
- weather: 天气查询相关
- calculator: 数学计算相关
- search: 文档搜索相关
- fallback: 无法判断时使用

输出 JSON：{"agent": "agent名称", "confidence": 0.0-1.0, "reason": "分类原因"}"""

def router(user_input: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": ROUTER_PROMPT},
            {"role": "user", "content": user_input}
        ],
        response_format={"type": "json_object"}
    )
    result = json.loads(response.choices[0].message.content)
    if result["confidence"] < 0.7:
        result["agent"] = "fallback"
    return result

# 各领域 Agent
agents = {
    "weather": {
        "prompt": "你是天气助手，查询和对比城市天气。",
        "tools": weather_tools
    },
    "calculator": {
        "prompt": "你是计算助手，执行数学运算。",
        "tools": calculator_tools
    },
    "search": {
        "prompt": "你是文档搜索助手，查找和总结文档内容。",
        "tools": search_tools
    },
    "fallback": {
        "prompt": "你是通用助手，尝试帮助用户。",
        "tools": []
    }
}

def routed_agent(user_input: str) -> str:
    # Step 1: 路由
    route = router(user_input)
    agent_config = agents[route["agent"]]

    # Step 2: 调用目标 Agent
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": agent_config["prompt"]},
            {"role": "user", "content": user_input}
        ],
        tools=agent_config["tools"] or None
    )
    return response.choices[0].message.content
```

## 失败模式

| 失败模式 | 症状 | 解法 |
|---------|------|------|
| 路由错误 | 请求被发送到错误的 Agent | 提高置信度阈值，低于阈值走 fallback |
| 意图歧义 | 用户请求包含多意图 | 支持多标签路由或先拆分再路由 |
| 新意图遗漏 | 出现未覆盖的请求类型 | 定期审查 fallback 日志，扩展类别 |
| 路由过度细化 | 类别太多导致分类困难 | 合并相似类别，控制在 10 个以内 |
| Router 延迟 | 增加一次 LLM 调用 | 使用轻量模型（GPT-4o-mini）或规则前置 |

## 验收标准

1. 路由准确率 > 95%（在 Golden Set 上）
2. 低置信度请求正确走 fallback > 90%
3. Router 延迟 P95 < 500ms
4. Fallback 比率 < 10%（过高说明类别不全）
5. 新增类别后路由准确率不下降

## 相关模式

- [Planner-Executor](planner-executor.md) — Router 确定方向后可用 Planner-Executor 执行
- [Multi-Agent](../concepts/multi-agent.md) — Router 是 Multi-Agent 的入口

## 验真状态

| 结论 | 证据等级 | 来源 |
|------|---------|------|
| 3-7 个类别时路由准确率最高 | L2 | Semanthic Router 实验 |
| 置信度阈值 0.7 是好的起点 | L1 | 社区经验 |
| GPT-4o-mini 做 Router 足够 | L2 | 多团队实践 |
| 类别超过 15 个时准确率降至 80% 以下 | L1 | 初步实验 |

## 参考来源

- Semantic Router Library (2024)
- LangChain Router Chain Documentation (2024)
- OpenAI Function Calling for Intent Classification (2024)
