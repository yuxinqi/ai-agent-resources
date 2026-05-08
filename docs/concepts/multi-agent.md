---
id: concept-multi-agent
title: Multi-Agent（多智能体协作）
type: concept
level: advanced
status: draft
evidence_level: L1
practical_rating: B
last_reviewed: "2026-05-08"
valid_until: "2026-08-08"
related:
  - concept-agent
  - concept-planning
  - pattern-router
  - pattern-planner-executor
depends_on:
  - concept-agent
tags:
  - multi-agent
  - collaboration
  - orchestration
  - core-concept
---

# Multi-Agent（多智能体协作）

## 一句话解释

Multi-Agent 是将复杂任务分配给多个专业化 Agent 协作完成的架构，每个 Agent 负责自己擅长的领域，通过协调机制共同产出结果。

## 它解决什么问题

单个 Agent 的能力有限——它用同一个 LLM、同一套工具、同一个 Prompt，试图处理所有类型的问题。这导致：

1. **Prompt 膨胀**：把所有指令塞进一个 System Prompt，互相干扰
2. **工具过多**：单个 Agent 管理 20+ 工具时选择准确率下降
3. **角色混乱**：同一个 Agent 既要写代码又要做 Code Review，角色冲突
4. **难以扩展**：增加新能力需要修改整个系统

Multi-Agent 通过"分而治之"解决这些问题：每个 Agent 专注于一个领域，拥有专属的工具和 Prompt，由一个协调器（Orchestrator）统一调度。

## 什么时候应该使用

- 任务涉及**多个专业领域**（如"调研 → 分析 → 写报告 → 排版"）
- 单个 Agent 的工具数量**超过 10 个**，选择准确率下降
- 需要**不同角色**协作（如"开发者 + 测试员 + 审核员"）
- 任务有**并行子任务**，可以同时执行提升效率

## 什么时候不应该使用

- 单一领域任务，一个 Agent 足够
- 任务简单，多 Agent 协调开销不值
- 团队缺乏 Multi-Agent 调试经验（调试难度指数级增长）
- 对成本敏感（多 Agent 意味着更多 API 调用）

## 最小实践示例

```python
from openai import OpenAI
import json

client = OpenAI()

class Agent:
    def __init__(self, name: str, system_prompt: str, tools: list = None):
        self.name = name
        self.system_prompt = system_prompt
        self.tools = tools or []

    def run(self, message: str) -> str:
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": message}
        ]
        response = client.chat.completions.create(
            model="gpt-4o-mini", messages=messages, tools=self.tools or None
        )
        return response.choices[0].message.content

# 专业化 Agent
researcher = Agent(
    name="researcher",
    system_prompt="你是一个调研专家。只负责收集和整理信息，不做分析。输出结构化的调研结果。"
)

analyst = Agent(
    name="analyst",
    system_prompt="你是一个分析师。基于调研结果进行深度分析，输出分析报告。不负责收集信息。"
)

writer = Agent(
    name="writer",
    system_prompt="你是一个写作专家。将分析和调研结果整理成易读的文章。注重可读性和结构。"
)

# Orchestrator 协调
def orchestrate(task: str) -> str:
    # Step 1: 调研
    research_result = researcher.run(f"请调研以下主题：{task}")
    # Step 2: 分析
    analysis_result = analyst.run(f"基于以下调研结果进行分析：\n{research_result}")
    # Step 3: 写作
    article = writer.run(f"基于以下内容撰写文章：\n调研：{research_result}\n分析：{analysis_result}")
    return article
```

## 常见失败模式

1. **Agent 间信息丢失**：下游 Agent 缺少上游 Agent 的关键信息。解法：明确定义 Agent 间的接口（输入/输出格式），Orchestrator 负责传递完整上下文。

2. **无限委托**：Agent A 把任务推给 B，B 又推回 A，形成循环。解法：限制委托深度，设置全局 max_turns。

3. **输出格式不一致**：不同 Agent 输出格式不同，下游 Agent 无法解析。解法：定义统一的输出 Schema，每个 Agent 的 System Prompt 包含输出格式要求。

4. **协调开销过大**：Orchestrator 本身消耗大量 Token，成本可能超过单 Agent。解法：只在确实需要分工的场景使用 Multi-Agent。

5. **调试困难**：多个 Agent 交互出错时，很难定位是哪个 Agent 的问题。解法：完善的 Tracing，记录每个 Agent 的完整输入输出。

## 评估方法

| 维度 | 指标 | 方法 |
|------|------|------|
| 协作效率 | Total Token Cost vs Single Agent | 对比总消耗 |
| 任务完成率 | Success Rate | Golden Set 评估 |
| 信息传递质量 | Context Preservation | 下游 Agent 是否获得足够信息 |
| 并行效率 | Wall Clock Time | 并行 vs 串行耗时对比 |

## 相关概念

- [Agent](agent.md) — Multi-Agent 的基本单元
- [Planning](planning.md) — Orchestrator 需要规划 Agent 调度
- [Router Pattern](../patterns/router.md) — 按意图路由到不同 Agent
- [Planner-Executor Pattern](../patterns/planner-executor.md) — 规划与执行分离

## 验真状态

| 结论 | 证据等级 | 来源 |
|------|---------|------|
| Multi-Agent 在多领域任务上优于单 Agent | L1 | AutoGen, CrewAI 初步实验 |
| 协调开销在 3+ Agent 时显著 | L2 | 社区基准测试 |
| 专业化 Agent 比通用 Agent 在特定任务上更准确 | L2 | Microsoft AutoGen 论文 |
| Multi-Agent 调试复杂度是单 Agent 的 3-5 倍 | L1 | 开发者调查 |

## 参考来源

- Wu et al., "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation" (2023)
- CrewAI Documentation (2024)
- Park et al., "Generative Agents: Interactive Simulacra of Human Behavior" (2023)
- Microsoft, "Multi-Agent Orchestration Patterns" (2024)
