---
id: concept-evaluation
title: Evaluation（评估）
type: concept
level: intermediate
status: draft
evidence_level: L2
practical_rating: A
last_reviewed: "2026-05-08"
valid_until: "2026-08-08"
related:
  - concept-agent
  - gs-evaluation
  - tool-evaluation
depends_on:
  - concept-agent
tags:
  - evaluation
  - metrics
  - quality
  - core-concept
---

# Evaluation（评估）

## 一句话解释

Evaluation 是系统化衡量 Agent 系统在结果正确性、过程合理性和系统可靠性方面表现的方法论和工具集，是 Agent 从实验走向生产的关键门槛。

## 它解决什么问题

Agent 系统的输出具有非确定性——同一个输入可能产生不同但都合理的输出，且中间步骤（工具调用、推理路径）同样需要评估。没有系统化的评估：

- **不知道改没改好**：修改了 Prompt 或工具，不确定效果是提升还是退化
- **不知道能不能上线**：没有客观数据支撑，只能主观感受
- **不知道边界在哪**：不知道 Agent 在什么场景下会失败
- **无法持续改进**：缺乏基线，改进无从比较

Evaluation 提供了一套**可量化、可复现、可追踪**的评估方法，让 Agent 开发从"凭感觉"变成"靠数据"。

## 什么时候应该使用

- Agent 开发的**每个迭代周期**（Prompt 修改、工具变更、模型升级后）
- Agent **上线前**的质量门禁
- **版本对比**时（A/B 测试、模型切换）
- **监控线上**表现，发现退化

## 什么时候不应该使用

- 早期快速原型阶段（评估成本 > 开发收益）
- 评估集质量差（"垃圾评估进，垃圾结论出"）
- 仅评估最终输出，忽略过程和系统指标

## 最小实践示例

### Golden Set 评估

```python
import json

# 评估集：每个用例有明确的评判标准
golden_set = [
    {
        "id": "eval-001",
        "input": "查询北京今天的天气",
        "expected_tools": [{"name": "get_weather", "args": {"city": "北京"}}],
        "expected_keywords": ["温度", "天气"],
        "should_not_contain": ["上海", "深圳"],
    },
    {
        "id": "eval-002",
        "input": "对比北京和上海的天气",
        "expected_tools": [
            {"name": "get_weather", "args": {"city": "北京"}},
            {"name": "get_weather", "args": {"city": "上海"}}
        ],
        "expected_keywords": ["北京", "上海", "对比"],
        "should_not_contain": [],
    }
]

def evaluate(agent_fn, golden_set):
    results = []
    for case in golden_set:
        output, trace = agent_fn(case["input"], return_trace=True)

        # 工具调用评估
        tool_match = len(trace.tool_calls) == len(case["expected_tools"])

        # 关键词覆盖
        keyword_coverage = sum(
            1 for kw in case["expected_keywords"] if kw in output
        ) / len(case["expected_keywords"])

        # 禁止内容检查
        violations = [kw for kw in case["should_not_contain"] if kw in output]

        results.append({
            "id": case["id"],
            "tool_match": tool_match,
            "keyword_coverage": keyword_coverage,
            "violations": violations,
            "passed": tool_match and keyword_coverage >= 0.8 and not violations
        })

    pass_rate = sum(r["passed"] for r in results) / len(results)
    return {"pass_rate": pass_rate, "details": results}
```

### LLM-as-Judge

```python
JUDGE_PROMPT = """你是一个严格的评估员。评估以下 Agent 回答的质量。

用户问题：{question}
参考答案：{reference}
Agent 回答：{answer}

评分标准：
1. 正确性(1-5)：信息是否与参考答案一致
2. 完整性(1-5)：是否覆盖了参考答案的所有要点
3. 简洁性(1-5)：是否冗余或跑题

输出 JSON：{{"correctness": N, "completeness": N, "conciseness": N, "reason": "..."}}"""

def llm_judge(question: str, answer: str, reference: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": JUDGE_PROMPT.format(
            question=question, answer=answer, reference=reference
        )}],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)
```

## 常见失败模式

1. **评估集太小**：10 个用例只能发现显而易见的问题，至少 50+ 才能覆盖主要路径。解法：渐进扩充，优先覆盖核心路径和已知失败案例。

2. **评估集污染**：Agent 在训练数据或 Prompt 中"见过"评估集答案。解法：评估集与开发集隔离，定期更换。

3. **过度依赖 LLM-as-Judge**：Judge 模型有自身偏差（倾向给高分、倾向长回答）。解法：Judge 评估 + 人工抽检，校准 Judge 偏差。

4. **忽视过程评估**：只看最终输出，不检查中间步骤。Agent 可能通过错误路径得到了正确结果。解法：记录完整 Trace，评估过程合理性。

5. **指标过多**：追踪 20+ 指标但不知道哪个重要。解法：确定 3-5 个核心指标（如 Success Rate, Latency P95, Cost/Task），其余为辅助。

## 评估方法

| 方法 | 适用场景 | 优点 | 缺点 |
|------|---------|------|------|
| Golden Set | 有标准答案的任务 | 客观、可复现 | 标注成本高 |
| LLM-as-Judge | 开放性任务 | 可扩展 | 有偏差 |
| 人工评估 | 最终验证 | 最可靠 | 昂贵、慢 |
| A/B 测试 | 线上对比 | 真实用户反馈 | 需要流量 |
| 回归测试 | 版本迭代 | 防止退化 | 需维护测试集 |

## 相关概念

- [Agent](agent.md) — 评估的对象
- [Guardrails Pattern](../patterns/guardrails.md) — 运行时安全保障
- [Evaluation Tools](../tools/evaluation-tools.md) — 评估工具推荐

## 验真状态

| 结论 | 证据等级 | 来源 |
|------|---------|------|
| Golden Set 50+ 用例才能发现主要问题 | L2 | 多团队实践经验 |
| LLM-as-Judge 与人工评估相关性约 0.8 | L2 | Zheng et al. 论文 |
| 过程评估可发现 30% 的隐蔽问题 | L1 | 初步实验 |
| 评估集需每季度更新 | L1 | 最佳实践建议 |

## 参考来源

- Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" (2023)
- RAGAS Framework (2024)
- LangSmith Evaluation Documentation (2024)
- OpenAI, "Evaluation Best Practices" (2024)
