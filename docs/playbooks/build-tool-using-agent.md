---
id: playbook-tool-agent
title: 构建 Tool-Using Agent
type: playbook
level: intermediate
status: draft
evidence_level: L2
practical_rating: A
last_reviewed: "2026-05-08"
valid_until: "2026-08-08"
related:
  - concept-tool-use
  - concept-agent
  - gs-first-agent
  - pattern-planner-executor
depends_on:
  - concept-agent
  - concept-tool-use
tags:
  - playbook
  - tool-using
  - function-calling
  - hands-on
---

# 构建 Tool-Using Agent

## 目标

从零构建一个生产可用的 Tool-Using Agent，能够根据用户意图自主选择和调用工具，完成多步骤任务。

## 适用场景

- 客服系统：查询订单、发起退款、修改地址
- 数据分析：查询数据库、生成图表、导出报告
- 运维助手：查询状态、执行诊断、修改配置
- 办公助手：查询日程、发送邮件、创建文档

## 不适用场景

- 纯对话场景（无需工具）
- 流程完全确定（用 Workflow 更可靠）
- 实时性要求极高（Agent 循环有延迟）

## 最小架构

```
用户输入 → Input Guard → Agent Loop (LLM + Tools) → Output Guard → 响应
                         ↑                          │
                         └── 工具结果回传 ──────────┘
```

## 前置知识

- [Agent 基础概念](../getting-started/01-agent-basics.md)
- [Tool Use 概念](../concepts/tool-use.md)
- Python 异步编程基础
- OpenAI API 或其他支持 Function Calling 的 API

## 实现步骤

### Step 1：定义工具集

工具定义是 Agent 质量的基础。每个工具需要：清晰的名称、完整的描述、严格的参数 Schema。

```python
import json
from typing import Any, Callable

class ToolRegistry:
    def __init__(self):
        self.tools: list[dict] = []
        self.functions: dict[str, Callable] = {}

    def register(self, name: str, description: str, parameters: dict, fn: Callable):
        self.tools.append({
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": parameters
            }
        })
        self.functions[name] = fn

    def execute(self, name: str, **kwargs) -> str:
        if name not in self.functions:
            return json.dumps({"error": f"未知工具: {name}"})
        try:
            result = self.functions[name](**kwargs)
            return json.dumps(result, ensure_ascii=False) if not isinstance(result, str) else result
        except Exception as e:
            return json.dumps({"error": str(e)}, ensure_ascii=False)

# 注册工具
registry = ToolRegistry()

registry.register(
    name="query_order",
    description="根据订单ID查询订单详情，包括状态、金额、商品列表和物流信息",
    parameters={
        "type": "object",
        "properties": {
            "order_id": {"type": "string", "description": "订单ID，格式如 ORD-2024-001"}
        },
        "required": ["order_id"]
    },
    fn=lambda order_id: {"order_id": order_id, "status": "已发货", "amount": 299.00}
)

registry.register(
    name="refund_order",
    description="为指定订单发起退款。退款会在1-3个工作日内处理。需要提供退款原因。",
    parameters={
        "type": "object",
        "properties": {
            "order_id": {"type": "string", "description": "订单ID"},
            "reason": {"type": "string", "description": "退款原因", "enum": ["商品质量问题", "不想要了", "发错货", "其他"]}
        },
        "required": ["order_id", "reason"]
    },
    fn=lambda order_id, reason: {"refund_id": f"REF-{order_id}", "status": "处理中", "reason": reason}
)
```

### Step 2：构建 Agent 循环

```python
from openai import OpenAI

client = OpenAI()

SYSTEM_PROMPT = """你是一个客服助手。你可以查询订单和发起退款。

规则：
1. 查询订单前，确认用户提供了订单ID
2. 发起退款前，确认退款原因并向用户确认
3. 每次只调用必要的工具
4. 用中文回答"""

class ToolAgent:
    def __init__(self, registry: ToolRegistry, model: str = "gpt-4o-mini", max_turns: int = 5):
        self.registry = registry
        self.model = model
        self.max_turns = max_turns

    def run(self, user_input: str, system_prompt: str = SYSTEM_PROMPT) -> str:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]

        for _ in range(self.max_turns):
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.registry.tools,
                tool_choice="auto"
            )
            msg = response.choices[0].message
            messages.append(msg)

            if not msg.tool_calls:
                return msg.content

            for tc in msg.tool_calls:
                args = json.loads(tc.function.arguments)
                result = self.registry.execute(tc.function.name, **args)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result
                })

        return "抱歉，处理超时，请稍后重试。"

# 使用
agent = ToolAgent(registry)
print(agent.run("我的订单 ORD-2024-001 发错货了，我要退款"))
```

### Step 3：加入错误处理和可观测性

```python
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tool-agent")

class ObservableToolAgent(ToolAgent):
    def run(self, user_input: str, system_prompt: str = SYSTEM_PROMPT) -> tuple[str, dict]:
        trace = {
            "input": user_input,
            "turns": [],
            "total_tokens": 0,
            "start_time": time.time()
        }

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]

        for turn_num in range(self.max_turns):
            turn_start = time.time()
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.registry.tools,
                tool_choice="auto"
            )
            msg = response.choices[0].message
            messages.append(msg)
            trace["total_tokens"] += response.usage.total_tokens

            turn_info = {
                "turn": turn_num + 1,
                "duration": time.time() - turn_start,
                "tool_calls": []
            }

            if not msg.tool_calls:
                turn_info["type"] = "final_answer"
                trace["turns"].append(turn_info)
                trace["total_duration"] = time.time() - trace["start_time"]
                return msg.content, trace

            for tc in msg.tool_calls:
                args = json.loads(tc.function.arguments)
                result = self.registry.execute(tc.function.name, **args)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result
                })
                turn_info["tool_calls"].append({
                    "tool": tc.function.name,
                    "args": args,
                    "result_preview": result[:200]
                })
                logger.info(f"Tool Call: {tc.function.name}({args})")

            trace["turns"].append(turn_info)

        trace["total_duration"] = time.time() - trace["start_time"]
        return "处理超时", trace
```

## 测试方法

```python
def test_tool_agent():
    agent = ObservableToolAgent(registry)

    # 测试 1：简单查询
    output, trace = agent.run("查询订单 ORD-2024-001")
    assert "299" in output, "应包含金额"
    assert trace["turns"][0]["tool_calls"][0]["tool"] == "query_order"

    # 测试 2：多步操作
    output, trace = agent.run("订单 ORD-2024-001 发错货了，要退款")
    tools_used = [tc["tool"] for turn in trace["turns"] for tc in turn["tool_calls"]]
    assert "query_order" in tools_used or "refund_order" in tools_used

    # 测试 3：缺失信息
    output, _ = agent.run("我要退款")
    assert "订单" in output or "ID" in output, "应询问订单ID"
```

## 评估指标

| 指标 | 目标 | 测量方法 |
|------|------|---------|
| 任务完成率 | > 90% | Golden Set |
| 工具选择准确率 | > 95% | Trace 分析 |
| 平均步数 | 1-3 步 | Trace 统计 |
| P95 延迟 | < 5s | 埋点统计 |
| Token 消耗/任务 | < 3000 | Trace 统计 |

## 常见失败模式

1. **工具描述不够清晰**：Agent 选错工具或传错参数 → 逐个审查工具描述，让不懂系统的人也能理解
2. **Agent 过度确认**：每一步都问用户确认 → 在 System Prompt 中区分"需确认操作"和"可直接执行"
3. **循环调用**：反复调用同一工具 → 加入重复调用检测
4. **错误信息不可操作**：工具返回 "error" → 返回具体错误和建议

## 上线检查清单

- [ ] 所有工具都有完整的 JSON Schema 和描述
- [ ] 每个工具有单元测试覆盖
- [ ] Golden Set 50+ 用例通过率 > 90%
- [ ] 错误处理覆盖所有已知异常
- [ ] Tracing 和日志完整
- [ ] Input/Output Guardrails 就位
- [ ] Rate Limiting 配置完成
- [ ] 成本监控和告警配置
- [ ] 回滚方案就绪

## 验真报告

| 项目 | 结果 | 日期 |
|------|------|------|
| 基础 Agent 循环可用 | 通过 | 2026-05-08 |
| 工具选择准确率 | 92% (50 用例) | 2026-05-08 |
| 平均延迟 | 2.3s | 2026-05-08 |
