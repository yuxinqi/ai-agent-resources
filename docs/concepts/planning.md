---
id: concept-planning
title: Planning（规划）
type: concept
level: intermediate
status: draft
evidence_level: L2
practical_rating: A
last_reviewed: "2026-05-08"
valid_until: "2026-08-08"
related:
  - concept-agent
  - concept-tool-use
  - pattern-planner-executor
  - pattern-reflection
depends_on:
  - concept-agent
tags:
  - planning
  - reasoning
  - core-concept
---

# Planning（规划）

## 一句话解释

Planning 是 Agent 将复杂目标分解为有序的、可执行的子任务步骤，并在执行过程中动态调整计划的能力。

## 它解决什么问题

没有规划的 Agent 是"反应式"的——它只根据当前输入做下一步决策，缺乏全局视野。这导致三个问题：

1. **目标漂移**：多步执行中逐渐偏离原始目标
2. **步骤冗余**：重复做已完成的步骤，或遗漏关键步骤
3. **无法回溯**：走错方向后无法识别和纠正

Planning 让 Agent 具备"先想后做"的能力：先制定整体计划，再逐步执行，遇到偏差时调整计划。这类似于人类处理复杂任务的方式——先列清单，再按序执行，遇到问题修改计划。

## 什么时候应该使用

- 任务需要 **3 步以上**才能完成
- 子任务之间有**依赖关系**（B 依赖 A 的结果）
- 执行路径**不确定**，需要根据中间结果调整
- 任务有明确的**验收标准**，可以判断是否完成

## 什么时候不应该使用

- 单步即可完成的任务（直接 Tool Call 更高效）
- 流程完全确定的任务（用 DAG/Workflow 更可靠）
- 对延迟极度敏感且任务简单的场景
- Planning 本身消耗的 Token 成本不可接受时

## 最小实践示例

### ReAct 模式（推理-行动交替）

```python
REACT_PROMPT = """你是一个分析助手。对于每个问题，按以下格式回答：

思考：分析当前情况，决定下一步
行动：调用工具或给出最终回答
观察：工具返回的结果

可以多轮思考-行动-观察，直到得出最终答案。"""

# Agent 自然地在每一步思考"我还需要做什么"
```

### Plan-and-Execute 模式（先规划后执行）

```python
PLANNER_PROMPT = """你是一个任务规划器。给定用户目标，输出一个 JSON 格式的执行计划：

{"steps": [
    {"id": 1, "action": "搜索XX资料", "tool": "search", "depends_on": []},
    {"id": 2, "action": "分析搜索结果", "tool": "analyze", "depends_on": [1]},
    {"id": 3, "action": "生成报告", "tool": "write", "depends_on": [2]}
]}

只输出计划，不执行。"""

EXECUTOR_PROMPT = """你是执行器。按计划逐步执行，每步完成后报告结果。
如果某步失败，说明原因并建议替代方案。"""
```

## 常见失败模式

1. **过度规划**：为简单任务制定复杂计划，增加延迟和出错概率。解法：根据任务复杂度选择是否规划，简单任务直接 ReAct。

2. **计划过于刚性**：制定了计划但执行中不调整，即使发现走错方向也不回头。解法：每个步骤执行后检查是否需要修正计划。

3. **计划过于模糊**：步骤描述不具体，执行器无法确定该做什么。解法：每个步骤应包含明确的动作、工具和预期输出。

4. **忽视依赖关系**：并行执行了有依赖的步骤，导致后续步骤缺少必要输入。解法：在计划中明确标注 `depends_on` 关系。

5. **无限递归规划**：Agent 不断规划而不执行，陷入"分析瘫痪"。解法：限制规划轮数，强制进入执行阶段。

## 评估方法

| 维度 | 指标 | 方法 |
|------|------|------|
| 计划质量 | Step Coverage | 计划是否覆盖所有必要步骤 |
| 执行效率 | Steps to Complete | 实际步骤数 vs 最少必要步骤数 |
| 调整能力 | Adaptation Rate | 遇到意外时成功调整的比率 |
| 规划开销 | Planning Token Cost | 规划阶段消耗的 Token 数 |

关键评估思路：**最优计划是恰好够用的计划**。过度规划和欠规划都是问题。

## 相关概念

- [Agent](agent.md) — Planning 是 Agent 的核心能力之一
- [Tool Use](tool-use.md) — 规划决定何时调用哪个工具
- [Reflection Pattern](../patterns/reflection.md) — 反思和修正执行结果
- [Planner-Executor Pattern](../patterns/planner-executor.md) — 规划与执行分离

## 验真状态

| 结论 | 证据等级 | 来源 |
|------|---------|------|
| ReAct 比纯 CoT 在工具调用任务上更有效 | L2 | Yao et al., ReAct 论文 |
| Plan-and-Execute 适合 5+ 步骤的复杂任务 | L2 | 多框架实践验证 |
| 规划开销在简单任务上不划算 | L2 | 社区基准测试 |
| Tree of Thought 在需要探索的任务上优于线性规划 | L1 | Yao et al., ToT 论文 |

## 参考来源

- Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models" (2023)
- Shinn et al., "Reflexion: Language Agents with Verbal Reinforcement Learning" (2023)
- Yao et al., "Tree of Thoughts: Deliberate Problem Solving with Large Language Models" (2023)
- Wang et al., "Plan-and-Solve Prompting" (2023)
