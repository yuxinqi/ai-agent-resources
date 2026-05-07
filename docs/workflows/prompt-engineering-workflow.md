---
title: 提示词工程工作流
category: workflows
tags: [提示词, 工作流, Prompt Engineering]
related:
  - ../concepts/llm-basics.md
  - ../prompts/prompt-engineering-basics.md
depends_on:
  - ../concepts/llm-basics.md
verification: false
created: 2026-05-07
updated: 2026-05-07
---

<!-- related_to: docs/concepts/llm-basics.md, docs/prompts/prompt-engineering-basics.md, docs/prompts/system-prompt-best-practices.md -->

# 提示词工程工作流

> 从需求到高质量的提示词，完整的提示词工程流程。

---

## 🗺️ 工作流

```
需求分析 → 初稿编写 → 效果测试 → 迭代优化 → 验真 → 固化版本
```

## 步骤一：需求分析

| 维度 | 问题 |
|------|------|
| 任务类型 | 写作/分析/编码/翻译/其他？ |
| 输出格式 | 自由文本/结构化/代码/JSON？ |
| 质量标准 | 准确性/创造性/一致性哪个优先？ |
| 约束条件 | 长度/风格/角色/安全限制？ |
| 目标模型 | 将在哪个模型上运行？ |

## 步骤二：初稿编写

使用 **CRISPE 框架** 构建提示词：

```
C - Capacity/Role (角色)：你是什么角色？
R - Insight/Context (上下文)：背景信息
I - Instruction (指令)：具体任务
S - Style (风格)：输出风格
P - Purpose/Example (目的/示例)：期望的输出示例
E - Evaluation (评估)：如何判断输出质量
```

### 模板

```markdown
# 角色
你是一个 [角色描述]

# 上下文
[背景信息]

# 指令
[具体任务说明]

# 输出要求
[格式/风格/长度等]

# 示例
输入：[示例输入]
输出：[期望输出]
```

## 步骤三：效果测试

### 测试方法

| 方法 | 说明 | 适用阶段 |
|------|------|---------|
| A/B 测试 | 对比不同提示词版本 | 优化阶段 |
| 边缘用例测试 | 测试极端输入 | 稳定阶段 |
| 回归测试 | 确保旧用例不受影响 | 每次修改后 |
| 人工评估 | 人工评分输出质量 | 关键场景 |

### 评估维度

- **准确性**：输出是否正确
- **完整性**：是否涵盖所有要求
- **格式合规**：是否符合输出格式
- **安全性**：是否产生有害内容
- **一致性**：多次输出是否一致

## 步骤四：迭代优化

```
初稿 → 测试 → 发现问题 → 修改 → 再测试
```

常见优化方向：
1. 更明确的角色设定
2. 提供更多示例（Few-shot）
3. 分步骤指导（Chain-of-Thought）
4. 约束输出格式
5. 添加否定指令（"不要..."）

## 步骤五：验真

将优化后的提示词提交到 `verification/prompts/` 目录进行验真。

## 步骤六：固化版本

- 为提示词创建版本号（v1.0, v1.1）
- 记录测试结果和验真报告
- 保存到 `docs/prompts/` 目录
