---
id: concept-tool-use
title: Tool Use（工具使用）
type: concept
level: intermediate
status: draft
evidence_level: L2
practical_rating: A
last_reviewed: "2026-05-08"
valid_until: "2026-08-08"
related:
  - concept-agent
  - concept-planning
  - pattern-planner-executor
depends_on:
  - concept-agent
tags:
  - tool-use
  - function-calling
  - core-concept
---

# Tool Use（工具使用）

## 一句话解释

Tool Use 是 LLM 通过 Function Calling 机制调用外部工具、与真实世界交互的能力，是 Agent 从"只会说话"到"能做事"的关键跃迁。

## 它解决什么问题

LLM 的知识是静态的、有限的。它不知道今天的天气、无法查询实时数据、不能操作你的系统。Tool Use 打破了这层限制，让 LLM 能够：

- **获取实时信息**：查询 API、数据库、搜索引擎
- **执行操作**：发送邮件、创建文件、调用服务
- **扩展能力**：运行代码、执行计算、处理图片

没有 Tool Use，LLM 只是一个百科全书；有了 Tool Use，LLM 变成了一个能动手的助手。

## 什么时候应该使用

- 需要获取 LLM 训练数据之外的实时信息
- 需要执行有副作用的操作（写入、发送、创建）
- 需要精确计算而非近似推理
- 需要与现有系统集成（CRM、数据库、API）

## 什么时候不应该使用

- 答案完全在 LLM 知识范围内且不需要实时更新
- 操作需要人工确认才能执行（应使用 Human-in-the-Loop 模式）
- 工具返回的信息量极大，超出上下文窗口
- 对安全性要求极高的操作（如资金转移），不应完全自动化

## 最小实践示例

```python
import json
from openai import OpenAI

client = OpenAI()

# Step 1: 定义工具
def calculate(expression: str) -> str:
    """安全地计算数学表达式"""
    try:
        # 仅允许数学运算，禁止代码执行
        allowed = set("0123456789+-*/.() ")
        if not all(c in allowed for c in expression):
            return json.dumps({"error": "表达式包含非法字符"})
        result = eval(expression)  # 生产环境应用 ast.literal_eval 或符号计算
        return json.dumps({"result": result})
    except Exception as e:
        return json.dumps({"error": str(e)}

tools = [{
    "type": "function",
    "function": {
        "name": "calculate",
        "description": "计算数学表达式的结果。支持加减乘除和括号。输入为数学表达式字符串。",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "要计算的数学表达式，如 '(120 + 30) * 0.85'"
                }
            },
            "required": ["expression"]
        }
    }
}]

# Step 2: Agent 循环
def agent_with_tools(query: str) -> str:
    messages = [{"role": "user", "content": query}]
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=messages, tools=tools
    )
    msg = response.choices[0].message

    if msg.tool_calls:
        results = []
        for tc in msg.tool_calls:
            args = json.loads(tc.function.arguments)
            result = calculate(**args)
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
        response = client.chat.completions.create(
            model="gpt-4o-mini", messages=messages
        )
        return response.choices[0].message.content
    return msg.content

# 使用
print(agent_with_tools("帮我算一下：3个商品原价120元，打85折后总价是多少？"))
```

## 常见失败模式

1. **工具描述歧义**：LLM 误解工具用途，在错误场景调用。例如将"搜索文档"理解为"搜索网页"。解法：description 必须精确，包含使用条件和边界。

2. **参数格式错误**：LLM 生成的参数不符合 Schema，如传了字符串给 integer 字段。解法：在工具端做参数校验和容错，返回清晰的错误信息。

3. **工具选择错误**：有多个相似工具时，LLM 选错了工具。解法：工具名和描述要有明确区分度，必要时在 System Prompt 中给出选择指引。

4. **幻觉工具调用**：LLM 尝试调用不存在的工具，或捏造参数。解法：严格限制 `tools` 列表，使用 `tool_choice` 控制何时可调用。

5. **链式依赖处理不当**：工具 A 的输出是工具 B 的输入，但 LLM 没有正确传递。解法：在 System Prompt 中明确步骤依赖关系，或使用 Planner-Executor 模式。

## 评估方法

| 指标 | 说明 | 目标 |
|------|------|------|
| Tool Selection Accuracy | 选择了正确工具的比率 | > 95% |
| Parameter Accuracy | 参数完全正确的比率 | > 90% |
| Unnecessary Tool Calls | 不必要的工具调用次数 | 最小化 |
| Tool Error Recovery | 工具报错后成功恢复的比率 | > 80% |

评估方法：构建 Golden Set 标注每个问题应调用的工具和参数，对比 Agent 实际行为。

## 相关概念

- [Agent](agent.md) — Tool Use 是 Agent 的核心能力
- [Planning](planning.md) — 决定何时调用哪个工具
- [Planner-Executor Pattern](../patterns/planner-executor.md) — 分离规划和执行

## 验真状态

| 结论 | 证据等级 | 来源 |
|------|---------|------|
| 工具描述质量直接影响调用准确率 | L3 | OpenAI 官方文档 + 多团队实践 |
| 并行工具调用可减少延迟 | L2 | OpenAI API 支持 parallel_tool_calls |
| 3-5 个工具时选择准确率最高 | L2 | Anthropic Tool Use 文档 |
| 工具超过 20 个时选择准确率显著下降 | L1 | 社区实验 |

## 参考来源

- OpenAI, "Function Calling" API Documentation (2024)
- Anthropic, "Tool Use" Documentation (2024)
- Schick et al., "Toolformer: Language Models Can Teach Themselves to Use Tools" (2023)
- Patil et al., "Gorilla: Connected LLMs to the Internet" (2023)
