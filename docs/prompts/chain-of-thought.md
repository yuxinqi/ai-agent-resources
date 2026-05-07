---
title: Chain-of-Thought 提示技巧
category: prompts
tags: [CoT, 推理, 高级技巧]
related:
  - prompt-engineering-basics.md
depends_on:
  - prompt-engineering-basics.md
verification: false
created: 2026-05-07
updated: 2026-05-07
---

<!-- related_to: docs/prompts/prompt-engineering-basics.md -->

# Chain-of-Thought 提示技巧

> Chain-of-Thought (CoT) 通过引导模型展示推理过程来提升复杂问题的回答质量。

---

## 一、什么是 CoT

CoT 让 LLM 在给出最终答案前，先展示逐步推理的过程。

### 传统提示 vs CoT 提示

```
传统提示：
问：小明有 5 个苹果，给了小红 2 个，又买了 3 个，现在有几个？
答：6 个

CoT 提示：
问：小明有 5 个苹果，给了小红 2 个，又买了 3 个，现在有几个？
答：小明原本有 5 个苹果。给了小红 2 个后：5 - 2 = 3。
    又买了 3 个后：3 + 3 = 6。
    所以小明现在有 6 个苹果。
```

## 二、CoT 的主要变体

| 变体 | 方法 | 适用场景 |
|------|------|---------|
| Zero-shot CoT | 直接加"让我们一步一步思考" | 通用推理 |
| Few-shot CoT | 给几个推理示例 | 复杂推理 |
| Self-Consistency | 多次采样取多数答案 | 高精度需求 |
| Tree-of-Thoughts | 并行探索多条推理路径 | 探索型任务 |

## 三、最佳实践

1. 使用引导语："让我们一步一步地思考"
2. 分解复杂问题
3. 明确推理的每个步骤
4. 需要高精度时结合 Self-Consistency
