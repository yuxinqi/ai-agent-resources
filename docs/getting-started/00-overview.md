---
id: gs-overview
title: AI Agent 知识体系总览
type: getting-started
level: beginner
status: draft
evidence_level: L1
practical_rating: A
last_reviewed: "2026-05-08"
valid_until: "2026-08-08"
related:
  - gs-agent-basics
  - gs-first-agent
  - gs-evaluation
depends_on: []
tags:
  - overview
  - getting-started
  - knowledge-layer
---

# AI Agent 知识体系总览

## 什么是 Agent？

Agent（智能体）是一种能够**自主感知环境、做出决策并采取行动**的 AI 系统。与传统的 LLM 对话不同，Agent 不仅生成文本，还能调用工具、访问外部数据、执行多步推理，并根据中间结果动态调整策略。简而言之，Agent = LLM + Tools + Memory + Planning。

传统聊天机器人只能回答问题，而 Agent 能**完成任务**。例如，一个客服 Agent 不仅能解释退货政策，还能查询订单状态、发起退款流程、通知仓库——这一切无需人工介入。

## 这个项目帮你做什么？

本项目是一个 **AI Agent 知识库**，旨在帮助工程师从零到一构建可靠的 Agent 系统。我们将知识组织为三层结构：

- **Knowledge Layer（知识层）**：你正在阅读的部分。提供概念解释、设计模式、实战 Playbook 和平台比较，帮助你理解和选型。
- **Evidence Layer（证据层）**：每个知识条目都附带验证状态（L0-L4），从理论推测到生产验证，让你知道哪些结论可靠、哪些还需要验证。
- **Practice Layer（实践层）**：可运行的代码示例和测试套件，让你动手验证每个概念。

## 如何导航三层结构

### 知识层（Knowledge Layer）

按角色和阶段组织：

| 路径 | 适合谁 | 内容 |
|------|--------|------|
| `getting-started/` | 新手入门 | Agent 基础概念、第一个 Agent、评估入门 |
| `concepts/` | 所有人 | 每个核心概念的深度解析卡片 |
| `patterns/` | 架构师 | 常见设计模式：Planner-Executor、Router、Reflection 等 |
| `playbooks/` | 工程师 | 端到端构建指南：RAG Agent、Research Agent 等 |
| `platforms/` | 选型决策 | 模型能力矩阵、API 平台对比、成本参考 |
| `tools/` | 工程师 | 框架对比、评测工具、Tracing、部署工具 |
| `case-studies/` | 所有人 | 真实案例分析，包含失败教训 |

### 证据层（Evidence Layer）

每个文档都包含 `evidence_level` 和 `practical_rating` 字段：

- **evidence_level**（L0-L4）：L0 = 理论推测，L1 = 小规模验证，L2 = 社区验证，L3 = 企业验证，L4 = 多企业复现验证
- **practical_rating**（A-D）：A = 可直接使用，B = 需适配，C = 仅参考，D = 不推荐

### 实践层（Practice Layer）

知识层中引用的所有代码示例都可以在 `examples/` 目录下找到对应项目，包含完整测试和运行说明。

## 开始之前

如果你是第一次接触 Agent 开发，建议按以下顺序阅读：

1. **[Agent 基础概念](01-agent-basics.md)** — 理解 Agent、Tool Use、Memory、Planning、RAG 五个核心概念
2. **[构建你的第一个 Agent](02-build-your-first-agent.md)** — 动手写一个简单的 Tool-Calling Agent
3. **[Agent 评估入门](03-agent-evaluation-basics.md)** — 学会判断 Agent 是否真的有用

如果你已有经验，可以直接跳到 `concepts/` 或 `patterns/` 查找感兴趣的主题。

## 贡献与反馈

本知识库是活文档，欢迎贡献。每个文件头部的 `valid_until` 字段表示内容的过期时间，超过该日期的内容需要重新验证。
