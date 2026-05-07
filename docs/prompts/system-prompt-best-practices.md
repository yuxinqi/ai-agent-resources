---
title: System Prompt 最佳实践
category: prompts
tags: [System Prompt, 最佳实践, 高级技巧]
related:
  - prompt-engineering-basics.md
  - chain-of-thought.md
depends_on:
  - prompt-engineering-basics.md
verification: false
created: 2026-05-07
updated: 2026-05-07
---

<!-- related_to: docs/prompts/prompt-engineering-basics.md -->

# System Prompt 最佳实践

> System Prompt 是设定 AI 行为和能力的核心手段。

---

## 一、System Prompt 的作用

| 功能 | 说明 |
|------|------|
| 角色设定 | 定义 AI 的身份和专长 |
| 行为约束 | 限制 AI 的输出范围和行为方式 |
| 能力声明 | 声明 AI 可以使用的工具和权限 |
| 规则定义 | 定义交互规则和边界条件 |

## 二、高质量 System Prompt 模板

```markdown
你是一个 [角色]。你的职责包括：

## 核心能力
- [能力 1]
- [能力 2]

## 行为准则
1. [规则 1]
2. [规则 2]

## 输出格式
- 使用 [格式] 输出
- 每次回复需要包含 [必要元素]

## 限制
- 不要 [禁止行为 1]
- 不要 [禁止行为 2]
```

## 三、常见策略

1. **角色锚定**：给你的 AI 一个明确且一致的角色身份
2. **分层指令**：把指令分为"必须做"和"最好做"
3. **否定指令**：明确指出不想要的行为（注意：不要过度使用）
4. **格式约束**：用结构化格式约束输出
5. **安全护栏**：添加安全相关的限制指令
