---
title: LLM 基础 — 大语言模型工作原理
category: concepts
tags: [LLM, Transformer, 基础理论, 模型架构]
related:
  - agent-architecture.md
  - function-calling.md
  - fine-tuning.md
depends_on: []
verification: false
created: 2026-05-07
updated: 2026-05-07
---

<!-- related_to: docs/concepts/agent-architecture.md, docs/concepts/function-calling.md, docs/concepts/fine-tuning.md -->
<!-- follows: docs/workflows/ai-app-development.md -->

# LLM 基础 — 大语言模型工作原理

## 📋 概念速览

| 项目 | 内容 |
|------|------|
| 全称 | Large Language Model (大语言模型) |
| 核心技术 | Transformer 架构 |
| 代表模型 | GPT-4o, Claude 4, Gemini 2.5, DeepSeek-V3, LLaMA 3 |
| 输入/输出 | 文本 → 文本（多模态模型支持图像、音频等） |
| ⚠️ 状态 | ⏳ 待验真 |

> **验真说明**：本文为基础概念文档，不涉及时效性极强的操作信息，暂无需验真。关联的平台操作文档将单独验真。

---

## 一、什么是 LLM

大语言模型（Large Language Model）是一种基于**海量文本数据**训练而成的深度学习模型，能够理解和生成自然语言。其核心能力来源于 **Transformer 架构**中的自注意力（Self-Attention）机制。

### 关键发展时间线

```
2017 — Transformer 论文 "Attention Is All You Need" (Google)
  ↓
2018 — GPT-1 (OpenAI) — 首个生成式预训练模型
  ↓
2019 — GPT-2 — 规模扩大，展示零样本能力
  ↓
2020 — GPT-3 — 1750 亿参数，展示上下文学习 (In-Context Learning)
  ↓
2022 — ChatGPT — 基于 GPT-3.5，对话式 AI 引爆全球
  ↓
2023 — GPT-4, Claude 3, LLaMA 2 — 多模态、开源
  ↓
2024 — Claude 3.5, GPT-4o, Gemini 2.0 — 原生多模态、Agent
  ↓
2025-2026 — Claude 4, Gemini 2.5, DeepSeek-V3 — 推理增强、深度 Agent 能力
```

## 二、核心工作原理

### 2.1 Transformer 架构

LLM 基于 Transformer 的 **Decoder-only** 架构（大多数现代 LLM）：

```
输入文本 → [Token 化] → [Embedding] → [多层 Decoder Block] → [输出概率分布]
                                              │
                                    ┌─────────┴──────────┐
                                    │ Self-Attention 层   │
                                    │ Feed-Forward 层     │
                                    │ Layer Normalization │
                                    └────────────────────┘
```

### 2.2 关键概念

| 概念 | 说明 |
|------|------|
| **Token** | 文本的最小处理单元，一个词或子词 |
| **Attention** | 模型关注输入中不同部分之间关系的能力 |
| **Context Window** | 模型一次能处理的最大 Token 数 |
| **Temperature** | 控制输出随机性的参数（0=确定，1=高随机） |
| **Top-p / Top-k** | 采样策略，控制输出的多样性 |

### 2.3 训练三阶段

```
1. 预训练 (Pre-training)
   海量无标注数据 → 下一词预测 → 基础能力
         ↓
2. 指令微调 (Instruction Tuning)
   高质量对话数据 → 对齐人类指令 → 可用性提升
         ↓
3. 强化学习 (RLHF/DPO)
   人类反馈 → 偏好对齐 → 安全与有用性
```

## 三、LLM 的能力边界

### ✅ 擅长
- 文本理解、生成、总结、翻译
- 代码编写与调试
- 逻辑推理（随着模型增强而提升）
- 角色扮演与对话
- 遵循复杂指令

### ❌ 不擅长 / 需注意
- **事实准确性**：可能产生"幻觉"（Hallucination）
- **实时信息**：训练数据有截止日期（除非接入检索）
- **精确计算**：数学运算不如下专用计算器
- **长上下文一致性**：超长文本中可能丢失细节
- **主观判断**：没有真正的"理解"和"意图"

## 四、主流模型对比

| 模型 | 开发商 | 上下文窗口 | 多模态 | 开源 | 最新版本 (截至 2026.05) |
|------|--------|-----------|--------|------|------------------------|
| GPT-4o | OpenAI | 128K | ✅ 是 | ❌ | 2025 年 |
| Claude 4 | Anthropic | 200K | ✅ 是 | ❌ | 2026 年初 |
| Gemini 2.5 | Google | 1M+ | ✅ 是 | ❌ | 2026 年 |
| DeepSeek-V3 | DeepSeek | 128K | ❌ 文本 | ✅ | 2025 年底 |
| LLaMA 3 | Meta | 128K | ✅ 是 | ✅ | 2025 年 |
| Qwen 2.5 | 阿里云 | 128K | ✅ 是 | ✅ | 2025 年 |

> ⚠️ 以上信息基于公开资料整理，**待验真**。具体参数请以官方文档为准。

## 五、相关资源

- [Agent 架构](agent-architecture.md) — LLM 作为 Agent 的"大脑"
- [Function Calling 机制](function-calling.md) — LLM 调用外部工具的能力
- [Fine-tuning 微调](fine-tuning.md) — 在 LLM 基础上定制化训练
- [API 平台综合对比](../platforms/platform-comparison.md)

## 六、推荐学习路径

```
LLM 基础 ← 你现在在这里
  → Agent 架构
    → Function Calling
      → MCP 协议
        → RAG 系统
          → 多 Agent 协作
```
