---
title: Skills 概念与最佳实践
category: skills
tags: [Skills, 教程, 最佳实践]
related: []
depends_on:
  - ../concepts/agent-architecture.md
verification: false
created: 2026-05-07
updated: 2026-05-07
---

<!-- related_to: docs/concepts/mcp-protocol.md, docs/concepts/agent-architecture.md -->

# Skills 概念与最佳实践

> Skills 是可复用的能力模块，封装了特定的 AI 行为模式和提示词指令。

---

## 一、什么是 Skills

Skills 是可复用的 AI 能力包，可以理解为"给 AI 的预配置技能"。它们通常包含：

- **触发条件**：什么情况下激活该技能
- **提示词指令**：指导 AI 行为的具体指令
- **工具配置**：所需的外部工具
- **输出规范**：期望的输出格式

### Skills vs Prompts

| 维度 | Prompts | Skills |
|------|---------|--------|
| 范围 | 单次交互的指令 | 可复用的能力包 |
| 复杂性 | 简单到中等 | 中等到复杂 |
| 可复用性 | 通常需定制 | 开箱即用 |
| 包含内容 | 提示文本 | 提示 + 工具 + 配置 |

## 二、常见 Skills 类型

| 类型 | 说明 | 示例 |
|------|------|------|
| 写作 Skill | 特定类型的写作辅助 | 技术文档、营销文案 |
| 编码 Skill | 编程相关任务 | 代码审查、重构 |
| 分析 Skill | 数据分析和洞察 | 日志分析、趋势预测 |
| 研究 Skill | 信息检索和总结 | 文献综述、竞品分析 |

## 三、相关资源

- [如何编写高质量的 Skills](writing-skills.md)
