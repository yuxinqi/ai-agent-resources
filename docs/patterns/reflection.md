---
id: pattern-reflection
title: Reflection 模式
type: pattern
level: intermediate
status: draft
evidence_level: L2
practical_rating: A
last_reviewed: "2026-05-08"
valid_until: "2026-08-08"
related:
  - pattern-evaluator-optimizer
  - pattern-planner-executor
  - concept-planning
depends_on:
  - concept-agent
  - concept-planning
tags:
  - pattern
  - reflection
  - self-correction
  - iterative-refinement
---

# Reflection 模式

## 架构图

```
┌─────────────────────────────────────────────────┐
│                    用户输入                       │
└─────────────────────┬───────────────────────────┘
                      ▼
              ┌───────────────┐
              │   Generator   │ ← 生成初始输出
              │  (生成器)      │
              └───────┬───────┘
                      │ 初始输出
                      ▼
              ┌───────────────┐
              │   Reflector   │ ← 审视输出，发现问题
              │  (反思器)      │
              └───────┬───────┘
                      │ 反馈 + 改进建议
                      ▼
              ┌───────────────┐
              │  质量达标？     │
              └───────┬───────┘
                      │
            ┌─────────┴─────────┐
            ▼                   ▼
          未达标               达标
    → 回到 Generator       → 返回最终结果
      (带反思反馈)          (可能经过多轮)
```

## 适用条件

- 输出质量有明确标准可以自检（如代码能运行、文章逻辑连贯、数据计算正确）
- 初次生成容易出错，但有明确的改进方向
- 单次生成成本可接受（Reflection 意味着多次调用）
- 有客观的验证手段（测试用例、规则检查、编译运行）

## 不适用条件

- 对延迟极度敏感（每轮 Reflection 增加一次 LLM 调用）
- 没有明确的评判标准（Reflector 无法判断好坏）
- 初次生成已经足够好（Reflection 徒增成本）
- LLM 无法自我纠正的错误（如事实性错误，LLM 可能反复犯同样的错）

## 最小代码示例

```python
from openai import OpenAI

client = OpenAI()

GENERATOR_PROMPT = """你是一个代码生成器。根据需求生成 Python 代码。
如果收到反思反馈，请根据反馈改进代码。"""

REFLECTOR_PROMPT = """你是一个代码审查员。审查以下代码，判断是否有问题：

审查维度：
1. 正确性：逻辑是否正确
2. 边界处理：是否处理了边界情况
3. 代码质量：是否清晰、无冗余
4. 安全性：是否有安全隐患

如果代码没有问题，输出：PASS
如果有问题，输出具体的问题描述和改进建议。"""

def reflection_agent(task: str, max_rounds: int = 3) -> str:
    # Round 1: 生成
    messages = [
        {"role": "system", "content": GENERATOR_PROMPT},
        {"role": "user", "content": task}
    ]
    gen_response = client.chat.completions.create(
        model="gpt-4o", messages=messages
    )
    current_output = gen_response.choices[0].message.content

    for round_num in range(max_rounds):
        # Reflection
        reflect_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": REFLECTOR_PROMPT},
                {"role": "user", "content": f"代码：\n{current_output}"}
            ]
        )
        feedback = reflect_response.choices[0].message.content

        # 检查是否通过
        if "PASS" in feedback:
            return current_output

        # 未通过：带反馈重新生成
        messages.append({"role": "assistant", "content": current_output})
        messages.append({"role": "user", "content": f"审查反馈：\n{feedback}\n\n请改进代码。"})
        gen_response = client.chat.completions.create(
            model="gpt-4o", messages=messages
        )
        current_output = gen_response.choices[0].message.content

    return current_output  # 达到最大轮次，返回当前版本
```

## 失败模式

| 失败模式 | 症状 | 解法 |
|---------|------|------|
| 反复犯同一错误 | Reflector 指出问题但 Generator 修正后仍错 | 加入客观验证（如运行代码），而非仅靠 LLM 判断 |
| 过度反思 | 稍有瑕疵就反复修改，成本翻倍 | 设定明确的质量阈值，"够好即可" |
| Reflector 标准不一致 | 有时严格有时宽松 | 使用结构化的审查清单，避免主观判断 |
| 幻觉式反思 | Reflector 编造不存在的问题 | 加入可验证的检查项，减少主观判断 |
| 无限循环 | Generator 和 Reflector 意见不一致，来回修改 | 设置 max_rounds 上限 |

## 验收标准

1. Reflection 后输出质量比初始生成提升 > 20%（在 Golden Set 上）
2. 平均 Reflection 轮次 1.5-2.5（过少说明没反思，过多说明生成质量差）
3. 90% 的 Reflection 在 3 轮内收敛
4. 总 Token 消耗 < 原始生成的 3 倍
5. 事实性错误不会被"反思"修正（需要外部验证）

## 相关模式

- [Evaluator-Optimizer](evaluator-optimizer.md) — 更结构化的评估 + 优化
- [Planner-Executor](planner-executor.md) — 执行后可用 Reflection 检查结果

## 验真状态

| 结论 | 证据等级 | 来源 |
|------|---------|------|
| Reflection 能提升代码生成质量 20-40% | L2 | Reflexion 论文 |
| Reflection 对事实性错误效果有限 | L2 | Huang et al. 研究 |
| 客观验证 + LLM 反思比纯 LLM 反思更有效 | L2 | 多团队实践 |
| 超过 3 轮 Reflection 收益递减 | L1 | 社区实验 |

## 参考来源

- Shinn et al., "Reflexion: Language Agents with Verbal Reinforcement Learning" (2023)
- Madaan et al., "Self-Refine: Iterative Refinement with Self-Feedback" (2023)
- Huang et al., "Large Language Models Cannot Self-Correct Reasoning Yet" (2023)
