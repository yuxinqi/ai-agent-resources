---
id: pattern-planner-executor
title: Planner-Executor 模式
type: pattern
level: intermediate
status: draft
evidence_level: L2
practical_rating: A
last_reviewed: "2026-05-08"
valid_until: "2026-08-08"
related:
  - pattern-reflection
  - pattern-evaluator-optimizer
  - concept-planning
depends_on:
  - concept-planning
  - concept-tool-use
tags:
  - pattern
  - planner
  - executor
  - decomposition
---

# Planner-Executor 模式

## 架构图

```
┌─────────────────────────────────────────────────┐
│                    用户输入                       │
└─────────────────────┬───────────────────────────┘
                      ▼
              ┌───────────────┐
              │   Planner     │ ← 生成执行计划
              │  (规划器)      │
              └───────┬───────┘
                      │ 执行计划 (JSON Steps)
                      ▼
              ┌───────────────┐
              │   Executor    │ ← 逐步执行计划
              │  (执行器)      │    可调用工具
              └───────┬───────┘
                      │ 执行结果
                      ▼
              ┌───────────────┐
              │  Plan Check   │ ← 检查是否需要修正计划
              │  (计划检查)    │
              └───────┬───────┘
                      │
            ┌─────────┴─────────┐
            ▼                   ▼
      需要修正计划          计划完成
      → 回到 Planner      → 返回最终结果
```

## 适用条件

- 任务需要 **5 步以上**才能完成，且步骤间有依赖关系
- 需要全局视野来优化执行顺序和资源分配
- 执行路径不确定，需要根据中间结果调整计划
- 团队中规划能力和执行能力需要解耦（不同模型或不同 Prompt）

## 不适用条件

- 简单任务（1-3 步直接 ReAct 更高效）
- 流程完全确定的任务（用 DAG/Workflow 更可靠）
- 对延迟极度敏感（Planner 本身需要一次 LLM 调用）
- Planner 和 Executor 使用同一模型且 Prompt 差异不大（拆分意义不大）

## 最小代码示例

```python
from openai import OpenAI
import json

client = OpenAI()

PLANNER_PROMPT = """你是一个任务规划器。给定用户目标，生成一个 JSON 格式的执行计划。

输出格式：
{
    "goal": "用户目标",
    "steps": [
        {"id": 1, "action": "步骤描述", "tool": "工具名", "depends_on": [], "expected_output": "预期输出"},
        {"id": 2, "action": "步骤描述", "tool": "工具名", "depends_on": [1], "expected_output": "预期输出"}
    ]
}

注意：
- 每个步骤必须明确 action 和 tool
- depends_on 标注步骤间的依赖关系
- 只输出 JSON，不要其他内容"""

EXECUTOR_PROMPT = """你是一个任务执行器。按计划逐步执行，每步完成后报告结果。

当前计划：{plan}
已完成的步骤：{completed}

请执行下一个步骤。如果所有步骤已完成，输出 "DONE: 最终结果"。
如果某步失败，输出 "FAILED: 步骤ID 原因" """

def planner_executor(user_goal: str, max_iterations: int = 10) -> str:
    # Step 1: 生成计划
    plan_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": PLANNER_PROMPT},
            {"role": "user", "content": user_goal}
        ],
        response_format={"type": "json_object"}
    )
    plan = json.loads(plan_response.choices[0].message.content)

    # Step 2: 逐步执行
    completed = {}
    for iteration in range(max_iterations):
        # 找到可执行的步骤（依赖已满足）
        next_step = None
        for step in plan["steps"]:
            if step["id"] not in completed:
                deps_met = all(d in completed for d in step["depends_on"])
                if deps_met:
                    next_step = step
                    break

        if next_step is None:
            break  # 所有步骤完成或无法继续

        # 执行步骤
        executor_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": EXECUTOR_PROMPT.format(
                    plan=json.dumps(plan, ensure_ascii=False),
                    completed=json.dumps(completed, ensure_ascii=False)
                )
            }]
        )
        result = executor_response.choices[0].message.content
        completed[next_step["id"]] = {
            "step": next_step,
            "result": result
        }

    return completed
```

## 失败模式

| 失败模式 | 症状 | 解法 |
|---------|------|------|
| 计划过于模糊 | Executor 无法确定具体操作 | 要求 Planner 输出具体的 action + tool + params |
| 计划过于刚性 | 中间结果与预期不符但无法调整 | 加入 Plan Check 环节，允许修正计划 |
| 依赖关系遗漏 | 步骤执行顺序错误 | Planner 必须显式标注 depends_on |
| Planner 幻觉工具 | 计划中引用不存在的工具 | 验证工具名是否在可用列表中 |
| 无限修正循环 | Plan Check 不断触发重新规划 | 限制修正次数，超过后降级为 ReAct |

## 验收标准

1. 给定 5 步以上任务，成功率 > 85%
2. 步骤执行顺序满足依赖约束
3. 平均步骤数不超过最优路径的 1.5 倍
4. Planner 调用次数 ≤ 2（初始规划 + 最多一次修正）
5. Executor 每步超时 < 30s

## 相关模式

- [Reflection](reflection.md) — 在执行后反思结果质量
- [Evaluator-Optimizer](evaluator-optimizer.md) — 评估并优化输出
- [Router](router.md) — 先路由到合适的 Planner

## 验真状态

| 结论 | 证据等级 | 来源 |
|------|---------|------|
| Planner-Executor 比 ReAct 在复杂任务上更稳定 | L2 | 多框架实践 |
| 使用不同模型做 Planner 和 Executor 可降本 | L2 | GPT-4 规划 + GPT-4o-mini 执行 |
| 超过 10 步的任务必须加入计划修正机制 | L1 | 初步实验 |

## 参考来源

- Wang et al., "Plan-and-Solve Prompting" (2023)
- LangGraph Planner-Executor Template (2024)
- CrewAI Task Decomposition Pattern (2024)
