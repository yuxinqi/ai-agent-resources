---
title: 提示词工程基础
category: prompts
tags: [提示词, 入门, Prompt Engineering]
related:
  - ../concepts/llm-basics.md
  - system-prompt-best-practices.md
depends_on:
  - ../concepts/llm-basics.md
verification: false
created: 2026-05-07
updated: 2026-05-07
---

<!-- related_to: docs/concepts/llm-basics.md, docs/prompts/system-prompt-best-practices.md -->
<!-- follows: docs/workflows/prompt-engineering-workflow.md -->

# 提示词工程基础

> 提示词工程（Prompt Engineering）是通过设计和优化输入提示词来引导 LLM 输出期望结果的技术。

---

## 一、基础原则

1. **明确具体**：告诉模型你想要什么，越具体越好
2. **提供上下文**：给模型足够的背景信息
3. **分解复杂任务**：把大任务拆成小步骤
4. **使用示例**：Few-shot 示例能显著提升效果
5. **指定输出格式**：明确告诉模型输出的格式要求

## 二、提示词类型

| 类型 | 说明 | 示例 |
|------|------|------|
| Zero-shot | 不给示例，直接提问 | "翻译这句话为英文：..." |
| Few-shot | 给几个示例再提问 | "示例1... 示例2... 现在请..." |
| Chain-of-Thought | 引导模型逐步推理 | "让我们一步一步思考..." |
| Role Prompting | 设定角色 | "你是一位资深Python工程师..." |

## 三、相关资源

- [System Prompt 最佳实践](system-prompt-best-practices.md)
- [Chain-of-Thought 提示技巧](chain-of-thought.md)
- [提示词工程工作流](../workflows/prompt-engineering-workflow.md)
