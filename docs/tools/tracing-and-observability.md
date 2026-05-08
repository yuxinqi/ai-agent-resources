---
id: tool-tracing
title: Agent 追踪与可观测性
type: tool
level: intermediate
status: draft
evidence_level: L0
practical_rating: C
last_reviewed: 2026-05-08
valid_until: 2026-08-08
related:
  - concept-evaluation
  - tool-evaluation
depends_on:
  - concept-agent
tags:
  - agent
  - observability
  - tracing
  - debugging
---

# Agent 追踪与可观测性

## 一句话定位

帮助你看清 Agent 内部每一步在做什么、为什么这么做、花了多长时间的观测工具。

## 适合场景

- Agent 输出不符合预期，需要定位问题
- 需要监控 Agent 的延迟和成本
- 需要审计 Agent 的决策过程
- 多步骤 Agent 的调试和优化

## 不适合场景

- 单次 API 调用的简单应用
- 对可观测性无需求的项目

## 核心工具

### LangSmith

- 全链路 Trace 记录
- 每个 LLM 调用的输入/输出/延迟/Token 数
- 支持比较不同运行结果
- 人工反馈收集

### Langfuse

- 开源 LLM 可观测性平台
- 支持 Trace、Score、Dataset
- 自托管，数据不外泄
- 兼容 LangChain/非 LangChain 项目

### Helicone

- OpenAI API 代理层
- 自动记录所有 API 调用
- 成本分析、缓存、限流
- 上手极简，改一个 URL 即可

### OpenTelemetry + 自建

- 标准化可观测性协议
- 可与现有 APM 系统集成
- 灵活但需要较多开发工作

## 关键指标

| 指标 | 说明 | 重要性 |
|------|------|--------|
| 端到端延迟 | 从请求到响应的总时间 | 高 |
| 步骤耗时 | 每个 Agent 步骤的耗时 | 高 |
| Token 消耗 | 每次 LLM 调用的 Token 数 | 高 |
| 工具调用链 | Agent 调用了哪些工具、顺序如何 | 中 |
| 错误率 | 工具调用失败、LLM 异常的比例 | 高 |
| 成本趋势 | 每日/每月 API 费用变化 | 高 |

## 实践建议

1. **从简单开始**：先用日志记录核心步骤，再考虑专业工具
2. **关注成本**：可观测性本身也会产生成本（存储、API 调用）
3. **隐私合规**：Trace 数据可能包含敏感信息，注意脱敏
4. **设置告警**：延迟突增、错误率上升、成本异常

## 验真结论

- 证据等级：L0
- 推荐等级：C
- 有效期至：2026-08-08
