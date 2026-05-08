---
id: pattern-evaluator-optimizer
title: Evaluator-Optimizer 模式
type: pattern
level: intermediate
status: draft
evidence_level: L1
practical_rating: B
last_reviewed: "2026-05-08"
valid_until: "2026-08-08"
related:
  - pattern-reflection
  - pattern-planner-executor
depends_on:
  - concept-agent
  - concept-evaluation
tags:
  - pattern
  - evaluator
  - optimizer
  - iterative
---

# Evaluator-Optimizer 模式

## 架构图

```
┌─────────────────────────────────────────────────┐
│                    用户输入                       │
└─────────────────────┬───────────────────────────┘
                      ▼
              ┌───────────────┐
              │   Optimizer   │ ← 生成/改进输出
              │  (优化器)      │
              └───────┬───────┘
                      │ 候选输出
                      ▼
              ┌───────────────┐
              │   Evaluator   │ ← 量化评估 + 具体反馈
              │  (评估器)      │    输出评分和改进方向
              └───────┬───────┘
                      │ 评分 + 反馈
                      ▼
              ┌───────────────┐
              │  评分达标？     │
              └───────┬───────┘
                      │
            ┌─────────┴─────────┐
            ▼                   ▼
          未达标               达标
    → Optimizer 改进        → 返回最终结果
      (带评估反馈)
```

## 适用条件

- 有**可量化的评估标准**（评分 1-5、通过/不通过、具体指标）
- 输出质量可以通过**迭代改进**逐步提升
- Evaluator 能给出**具体改进方向**，而非仅"好/不好"
- 每轮改进的成本可接受

## 不适用条件

- 评估标准主观且难以量化
- 一次生成即可满足需求
- 改进空间有限（如格式转换类任务）
- 评估本身不可靠（Evaluator 质量差）

## 最小代码示例

```python
from openai import OpenAI
import json

client = OpenAI()

OPTIMIZER_PROMPT = """你是一个文案优化器。根据评估反馈改进文案。

原始需求：{requirement}
当前版本：{current_version}
评估反馈：{feedback}
当前评分：{score}/5

请改进文案，输出改进后的版本。"""

EVALUATOR_PROMPT = """你是一个文案评估器。评估以下文案质量。

需求：{requirement}
文案：{content}

评分维度（1-5分）：
1. 吸引力：标题和开头是否引人注意
2. 信息量：是否传达了关键信息
3. 可读性：是否易于阅读和理解
4. 行动引导：是否有明确的 CTA

输出 JSON：
{
    "scores": {"attractiveness": N, "information": N, "readability": N, "cta": N},
    "overall": N,
    "feedback": "具体改进建议",
    "passed": true/false
}

passed 条件：overall >= 4 且所有维度 >= 3"""

def evaluator_optimizer(task: str, max_rounds: int = 3) -> tuple[str, dict]:
    # Round 1: 初始生成
    current = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": f"根据以下需求生成文案：{task}"}]
    ).choices[0].message.content

    eval_history = []
    for _ in range(max_rounds):
        # Evaluate
        eval_result = client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": EVALUATOR_PROMPT.format(requirement=task, content=current)
            }],
            response_format={"type": "json_object"}
        )
        evaluation = json.loads(eval_result.choices[0].message.content)
        eval_history.append(evaluation)

        if evaluation["passed"]:
            return current, evaluation

        # Optimize
        current = client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": OPTIMIZER_PROMPT.format(
                    requirement=task,
                    current_version=current,
                    feedback=evaluation["feedback"],
                    score=evaluation["overall"]
                )
            }]
        ).choices[0].message.content

    return current, eval_history[-1]
```

## 失败模式

| 失败模式 | 症状 | 解法 |
|---------|------|------|
| Evaluator 标准漂移 | 不同轮次评估标准不一致 | 使用固定评分 Rubric，结构化评估维度 |
| Optimizer 过度迎合 Evaluator | 优化后满足评分但偏离原始需求 | Evaluator 维度包含"需求匹配度" |
| 评分通胀 | Evaluator 越来越宽松 | 交叉评估或使用多个 Evaluator |
| 评估反馈过于模糊 | Optimizer 不知道怎么改进 | 要求 Evaluator 给出具体改进示例 |
| 收益递减 | 3 轮后评分提升不明显 | 设置改进阈值，提升 < 0.3 分则停止 |

## 验收标准

1. 经过优化后 overall 评分提升 > 1 分（5 分制）
2. 80% 的任务在 3 轮内达到 passed
3. Optimizer 每轮改进确实响应了 Evaluator 的反馈
4. 最终输出与原始需求一致（不偏移）
5. 总 Token 消耗 < 初始生成的 4 倍

## 相关模式

- [Reflection](reflection.md) — 更轻量的自我修正（无量化评分）
- [Planner-Executor](planner-executor.md) — Evaluator 可在执行后触发

## 验真状态

| 结论 | 证据等级 | 来源 |
|------|---------|------|
| 量化评分比"好/不好"更有效指导优化 | L1 | 初步实验 |
| 3 轮迭代后收益显著递减 | L1 | 社区经验 |
| Evaluator 和 Optimizer 使用不同 Prompt 很重要 | L2 | Madaan et al. Self-Refine |

## 参考来源

- Madaan et al., "Self-Refine: Iterative Refinement with Self-Feedback" (2023)
- Google DeepMind, "Generative AI for Iterative Design" (2024)
- LangGraph Evaluator-Optimizer Template (2024)
