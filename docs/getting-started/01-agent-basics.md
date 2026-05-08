---
id: gs-agent-basics
title: Agent 基础概念
type: getting-started
level: beginner
status: draft
evidence_level: L2
practical_rating: A
last_reviewed: "2026-05-08"
valid_until: "2026-08-08"
related:
  - gs-overview
  - gs-first-agent
  - concept-agent
  - concept-tool-use
depends_on:
  - gs-overview
tags:
  - agent
  - basics
  - getting-started
---

# Agent 基础概念

本文介绍 AI Agent 的五个核心概念：Agent、Tool Use、Memory、Planning 和 RAG。理解这些概念是构建任何 Agent 系统的基础。

## Agent（智能体）

Agent 是一个能够**自主完成目标**的 AI 系统。它与传统 LLM 对话的核心区别在于"自主性"——Agent 不是被动回答问题，而是主动规划步骤、调用工具、观察结果并调整策略。

一个 Agent 的最小组成：

```
目标 → 规划 → 行动(调用工具) → 观察 → 调整 → 行动 → ... → 目标完成
```

关键特征：
- **自主决策**：Agent 自己决定下一步做什么，而非由预定义流程驱动
- **工具使用**：通过调用外部工具扩展能力边界
- **状态保持**：在多轮交互中维护上下文和记忆
- **错误恢复**：当某步失败时能回退或尝试替代方案

## Tool Use（工具使用）

Tool Use 是 Agent 与外部世界交互的机制。LLM 本身只能生成文本，但通过 Function Calling / Tool Calling，Agent 可以查询数据库、调用 API、读写文件、执行代码——几乎可以做任何编程能做的事。

工具使用的工作流：

1. **定义工具**：用 JSON Schema 描述工具的名称、参数和返回值
2. **LLM 决策**：LLM 根据用户请求决定调用哪个工具、传什么参数
3. **执行工具**：运行时执行工具代码，获取结果
4. **结果回传**：将工具执行结果返回给 LLM，让它继续推理

```python
# 工具定义示例
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "获取指定城市的天气",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名称"}
            },
            "required": ["city"]
        }
    }
}]
```

关键原则：**工具定义即文档**。LLM 完全依赖工具描述来决定何时、如何调用工具，因此 description 必须清晰、无歧义。

## Memory（记忆）

Memory 让 Agent 能在多轮对话和多次执行中保持上下文。根据持久性和范围，Memory 可以分为：

| 类型 | 作用 | 示例 |
|------|------|------|
| Short-term Memory | 单次对话内的上下文 | 对话历史 |
| Long-term Memory | 跨对话的持久信息 | 用户偏好、知识库 |
| Working Memory | 当前任务的中间状态 | 已完成的步骤、待处理项 |

实践中，Memory 的核心挑战是**上下文窗口有限**。当对话历史超出窗口时，需要策略来压缩或筛选历史信息（如滑动窗口、摘要、向量检索）。

## Planning（规划）

Planning 是 Agent 将复杂目标分解为可执行步骤的能力。没有规划的 Agent 容易陷入"只见树木不见森林"的困境——每一步看似合理，但整体偏离目标。

常见的规划策略：

- **ReAct**：交替进行推理(Reasoning)和行动(Acting)，每步都反思当前状态
- **Plan-and-Execute**：先制定完整计划，再逐步执行，执行中可修正计划
- **Tree of Thought**：探索多条推理路径，选择最优方案

规划不是万能的。简单任务（单次工具调用即可完成）不需要规划，过度规划反而增加延迟和出错概率。

## RAG（检索增强生成）

RAG（Retrieval-Augmented Generation）让 Agent 在生成回答前先从外部知识库检索相关信息，从而解决 LLM 知识过时和幻觉问题。

RAG 的基本流程：

```
用户问题 → Query 改写 → 向量检索/关键词检索 → 重排序 → 拼接上下文 → LLM 生成
```

关键组件：
- **Embedding 模型**：将文本转为向量，决定检索质量的上限
- **向量数据库**：存储和检索向量，如 Chroma、Pinecone、Weaviate
- **Chunking 策略**：文档切分方式直接影响检索粒度
- **Reranker**：对检索结果重排序，提升相关性

RAG 不是万能解。当知识需要精确引用（如法律条文）或需要复杂推理时，纯 RAG 往往不够，需要结合 Agent 的规划和推理能力。

## 五者的关系

这五个概念不是孤立的，它们在 Agent 系统中协同工作：

```
Agent（大脑）
├── Planning（规划：分解目标）
├── Tool Use（行动：执行步骤）
├── Memory（记忆：保持上下文）
└── RAG（知识：获取外部信息）
```

一个完整 Agent 的工作流程：Agent 接收目标 → Planning 分解任务 → 每步可能需要 Tool Use 执行、RAG 检索知识、Memory 回忆历史 → 根据结果调整计划 → 最终完成目标。

## 下一步

现在你已经了解了基础概念，接下来[构建你的第一个 Agent](02-build-your-first-agent.md) 来实践这些知识。
