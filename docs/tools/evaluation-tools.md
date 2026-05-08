---
id: tool-evaluation
title: Agent 评估工具
type: tool
level: intermediate
status: draft
evidence_level: L0
practical_rating: C
last_reviewed: 2026-05-08
valid_until: 2026-08-08
related:
  - concept-evaluation
depends_on:
  - concept-evaluation
tags:
  - agent
  - evaluation
  - tools
  - benchmark
---

# Agent 评估工具

## 一句话定位

帮助你评估 Agent 性能、质量和可靠性的工具和方法。

## 适合场景

- 需要量化评估 Agent 输出质量
- 需要追踪 Agent 性能变化趋势
- 需要在不同模型/配置间做对比
- 准备将 Agent 推向生产环境

## 不适合场景

- 还在概念验证阶段
- 只需要主观判断质量

## 核心工具

### LangSmith

| 维度 | 评价 |
|------|------|
| 定位 | LangChain 官方可观测性平台 |
| 核心能力 | Trace、评估、数据集管理、人工标注 |
| 上手成本 | 低（LangChain 生态内免配置） |
| 局限性 | 与 LangChain 绑定较深 |

### Promptfoo

| 维度 | 评价 |
|------|------|
| 定位 | 开源 Prompt 评估框架 |
| 核心能力 | 多模型对比、断言测试、红队测试 |
| 上手成本 | 低（YAML 配置驱动） |
| 局限性 | 主要评估 Prompt，不适合复杂 Agent |

### OpenAI Evals

| 维度 | 评价 |
|------|------|
| 定位 | OpenAI 官方评估框架 |
| 核心能力 | 标准化评估流程、Grader 机制 |
| 上手成本 | 中 |
| 局限性 | 仅限 OpenAI 模型 |

### 自建评估方案

| 维度 | 评价 |
|------|------|
| 定位 | 基于业务指标自建评估流程 |
| 核心能力 | 完全定制化、贴合业务 |
| 上手成本 | 高（需要自己设计和实现） |
| 局限性 | 开发维护成本高 |

## 评估维度参考

| 维度 | 指标 | 工具支持 |
|------|------|---------|
| 任务完成率 | 成功完成任务的比例 | 自建 / LangSmith |
| 工具调用准确率 | 正确选择和使用工具的比例 | 自建 |
| 响应质量 | 输出的准确性、完整性、相关性 | Promptfoo / LLM-as-Judge |
| 延迟 | 端到端响应时间 | LangSmith / 自建 |
| 成本 | Token 消耗和 API 费用 | LangSmith / 自建 |
| 一致性 | 相同输入多次运行结果的稳定性 | 自建 |

## 验真结论

- 证据等级：L0（仅收集信息，未深度验证）
- 推荐等级：C（工具更新快，需要自行验证适用性）
- 有效期至：2026-08-08

## 替代方案

根据评估场景灵活选择，不必绑定单一工具。简单场景用 Promptfoo，LangChain 项目用 LangSmith，生产系统建议自建核心指标。
