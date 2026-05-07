---
title: 如何编写高质量的 Skills
category: skills
tags: [Skills, 教程, 编写指南]
related:
  - skills-overview.md
depends_on:
  - skills-overview.md
verification: false
created: 2026-05-07
updated: 2026-05-07
---

<!-- related_to: docs/skills/skills-overview.md -->

# 如何编写高质量的 Skills

> 编写高质量的 Skills 需要考虑清晰性、可复用性和可维护性。

---

## 一、Skill 的基本结构

```markdown
---
name: my-skill
description: 简短描述该技能的用途
---

# 技能名称

## 触发条件
什么情况下应该激活此技能。

## 核心指令
具体的提示词内容，指导 AI 的行为。

## 工具需求
该技能需要哪些外部工具。

## 输出规范
期望的输出格式和标准。

## 使用示例
输入/输出示例。
```

## 二、编写原则

1. **单一职责**：一个 Skill 只做一件事
2. **清晰触发**：明确什么情况下使用
3. **具体指令**：不给 AI 模糊的指示
4. **可测试**：每个 Skill 都应该可以独立验证效果

## 三、验真要求

每个提交到本仓库的 Skills 必须：
1. 附带验真报告（使用 `verification/skills/template.md`）
2. 注明测试的模型和日期
3. 提供使用示例
