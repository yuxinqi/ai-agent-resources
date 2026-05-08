---
id: gs-evaluation
title: Agent 评估入门
type: getting-started
level: beginner
status: draft
evidence_level: L2
practical_rating: A
last_reviewed: "2026-05-08"
valid_until: "2026-08-08"
related:
  - gs-overview
  - gs-agent-basics
  - concept-evaluation
  - tool-evaluation
depends_on:
  - gs-agent-basics
tags:
  - evaluation
  - getting-started
  - metrics
---

# Agent 评估入门

构建 Agent 只是第一步，判断 Agent 是否**真的有用**才是工程化的关键。本文介绍 Agent 评估的核心思路、常用指标和实操方法。

## 为什么 Agent 评估很难？

传统软件的输出是确定性的——相同的输入必定产生相同的输出，测试只需断言结果。但 Agent 的输出具有**非确定性**：同一个问题可能得到不同但都合理的回答，且中间步骤（工具调用、推理过程）同样需要评估。

Agent 评估的三层挑战：

| 层次 | 评估对象 | 难度 |
|------|---------|------|
| 结果层 | 最终回答是否正确 | 中等——需要参考答案或 LLM-as-Judge |
| 过程层 | 中间步骤是否合理 | 困难——没有标准参考，需专家判断 |
| 系统层 | 延迟、成本、稳定性 | 简单——可量化指标 |

## 评估框架：输入-过程-输出

一个完整的 Agent 评估应覆盖三个维度：

### 1. 输出质量（Output Quality）

最终回答是否正确、完整、有用？

- **准确率**（Accuracy）：回答是否事实正确
- **完整率**（Completeness）：是否涵盖了用户问题的所有方面
- **相关性**（Relevance）：回答是否切题

评估方法：
- **Golden Set**：人工标注的正确答案集合，对比 Agent 输出与参考答案
- **LLM-as-Judge**：用另一个 LLM 评判输出质量，适合开放性问题
- **人工评估**：最可靠但最昂贵，通常用于抽检

### 2. 过程质量（Process Quality）

Agent 的中间步骤是否高效、合理？

- **工具调用准确率**：调用了正确的工具和参数吗？
- **步骤效率**：完成任务用了多少轮？是否有多余步骤？
- **错误恢复率**：遇到错误后能否成功恢复？

评估方法：
- **Trace 分析**：记录每一步的输入输出，人工审查
- **步骤计数**：统计完成任务的平均步数，与基线对比
- **路径覆盖率**：测试集覆盖了多少种不同的执行路径

### 3. 系统质量（System Quality）

系统在生产环境中的表现如何？

| 指标 | 含义 | 目标 |
|------|------|------|
| Latency P50/P95 | 首个 Token 和总完成时间 | P95 < 10s |
| Cost per Task | 每个任务的 Token 消耗和 API 费用 | < ¥0.5/task |
| Success Rate | 任务成功完成的比率 | > 90% |
| Error Rate | 工具调用失败或超时的比率 | < 5% |

## 实操：构建评估流水线

### Step 1：建立 Golden Set

```python
golden_set = [
    {
        "id": "weather-001",
        "input": "北京今天适合跑步吗？",
        "expected_tool_calls": ["get_weather"],
        "expected_answer_contains": ["温度", "天气", "建议"],
        "category": "单城市天气查询"
    },
    {
        "id": "weather-002",
        "input": "北京和上海哪个更适合今天户外活动？",
        "expected_tool_calls": ["get_weather", "get_weather"],
        "expected_answer_contains": ["北京", "上海", "对比"],
        "category": "多城市对比"
    },
]
```

### Step 2：运行评估

```python
def evaluate_agent(agent_fn, golden_set):
    results = []
    for case in golden_set:
        output = agent_fn(case["input"])

        # 简单的关键词匹配（生产环境应使用更复杂的评估）
        coverage = sum(
            1 for kw in case["expected_answer_contains"]
            if kw in output
        ) / len(case["expected_answer_contains"])

        results.append({
            "id": case["id"],
            "category": case["category"],
            "coverage": coverage,
            "output_length": len(output),
        })
    return results
```

### Step 3：LLM-as-Judge

当关键词匹配不够时，用 LLM 来评判：

```python
JUDGE_PROMPT = """你是一个评估专家。请评估以下 Agent 回答的质量。

用户问题：{question}
Agent 回答：{answer}

请从以下维度打分（1-5分）：
1. 准确性：信息是否正确
2. 完整性：是否全面回答了问题
3. 有用性：建议是否实用

输出 JSON 格式：{{"accuracy": N, "completeness": N, "helpfulness": N, "reason": "..."}}"""
```

## 评估的常见误区

1. **只看最终输出**：过程质量同样重要。Agent 可能通过 10 步完成了 3 步就能完成的任务，虽然结果正确但效率低下。
2. **Golden Set 太小**：至少 50 个测试用例才能覆盖主要场景，100+ 才能发现边界问题。
3. **忽视变异度**：同一问题跑 5 次，如果 4 次正确 1 次离谱，成功率是 80% 而非 100%。
4. **过度依赖 LLM-as-Judge**：Judge 模型本身有偏差，重要场景必须人工验证。
5. **评估集污染**：如果 Agent 的 System Prompt 或训练数据中包含了评估集的答案，评估结果不可信。

## 渐进式评估策略

不要试图一次建立完美的评估体系，而是渐进演进：

```
Level 1: 人工试用 + 主观感受（0 天）
Level 2: 10 个核心用例 + 关键词检查（1 天）
Level 3: 50 个用例 + LLM-as-Judge + 自动化（1 周）
Level 4: 100+ 用例 + 过程评估 + A/B 测试（持续）
```

## 下一步

- 阅读 [Evaluation 概念卡片](../concepts/evaluation.md) 深入理解评估方法论
- 查看 [评测工具](../tools/evaluation-tools.md) 了解可用的评估工具
- 参考 [Production Readiness Playbook](../playbooks/production-readiness.md) 了解生产级评估体系
