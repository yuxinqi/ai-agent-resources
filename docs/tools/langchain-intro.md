---
title: LangChain 框架入门
category: tools
tags: [LangChain, 框架, Python, LLM]
related:
  - ../concepts/agent-architecture.md
  - ../concepts/rag-retrieval.md
depends_on:
  - ../concepts/llm-basics.md
verification: false
created: 2026-05-07
updated: 2026-05-07
---

<!-- related_to: docs/concepts/agent-architecture.md, docs/concepts/rag-retrieval.md -->

# LangChain 框架入门

> LangChain 是一个用于构建 LLM 应用的框架，提供链式调用、Agent、RAG 等能力。

---

## 一、快速概览

| 项目 | 内容 |
|------|------|
| 官网 | https://langchain.com |
| 语言 | Python, JavaScript/TypeScript |
| 核心能力 | Chain, Agent, RAG, Memory, Tool |
| 适用场景 | 快速构建 LLM 应用原型到生产 |
| ⚠️ 状态 | ⏳ 待验真 |

## 二、核心概念

| 概念 | 说明 |
|------|------|
| Model | LLM 模型的抽象封装 |
| Prompt Template | 提示词模板 |
| Chain | 将多个步骤串联为流水线 |
| Agent | 具有工具调用能力的智能体 |
| Retriever | 检索器 |
| Memory | 对话记忆管理 |
| Tool | 外部工具封装 |

## 三、快速示例

> ⚠️ 以下示例使用 LangChain v0.3+ API。需先安装：`pip install langchain langchain-openai`

```python
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import tool
from langchain.prompts import PromptTemplate

# 创建模型
llm = ChatOpenAI(model="gpt-4o")

# 定义工具
@tool
def search(query: str) -> str:
    """搜索信息"""
    return f"搜索结果: {query}"

# 创建 Agent
tools = [search]
prompt = PromptTemplate.from_template("...")
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

# 执行
result = agent_executor.invoke({"input": "搜索 AI 新闻"})
print(result)
```
