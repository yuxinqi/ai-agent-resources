---
title: Agent 架构 — 智能体的核心设计模式
category: concepts
tags: [Agent, 智能体, 架构设计, 工具使用]
related:
  - llm-basics.md
  - function-calling.md
  - mcp-protocol.md
depends_on:
  - llm-basics.md
verification: false
created: 2026-05-07
updated: 2026-05-07
---

<!-- related_to: docs/concepts/llm-basics.md, docs/concepts/function-calling.md, docs/concepts/mcp-protocol.md -->
<!-- depends_on: docs/concepts/llm-basics.md -->

# Agent 架构 — 智能体的核心设计模式

## 📋 概念速览

| 项目 | 内容 |
|------|------|
| 定义 | 能够自主感知环境、做出决策并执行行动的 AI 系统 |
| 核心组件 | LLM（大脑）+ Tools（工具）+ Memory（记忆）+ Planning（规划） |
| 代表框架 | AutoGen, CrewAI, LangChain Agent, Claude Agent SDK |
| 关键协议 | MCP (Model Context Protocol), Function Calling |
| ⚠️ 状态 | ⏳ 待验真 |

---

## 一、什么是 AI Agent

AI Agent（智能体）是以 LLM 为核心"大脑"，通过调用外部工具、维护记忆、执行多步规划来完成复杂任务的自主系统。

### 与传统 LLM 调用的区别

| 特性 | 传统 LLM 调用 | AI Agent |
|------|-------------|----------|
| 交互方式 | 单轮或简单多轮对话 | 多步推理 + 工具调用循环 |
| 外部工具 | 无或手动触发 | 自动决策并调用 |
| 记忆管理 | 上下文窗口 | 结构化记忆（短期 + 长期） |
| 任务复杂度 | 单步骤任务 | 多步骤复杂任务 |
| 自主性 | 完全依赖用户引导 | 可自主规划和执行 |

## 二、Agent 核心架构

```
              ┌──────────────────────────────────┐
              │           用户输入                 │
              └────────────┬─────────────────────┘
                           ▼
              ┌──────────────────────────────────┐
              │         🧠 LLM (大脑)             │
              │   • 理解意图                      │
              │   • 推理规划                      │
              │   • 生成回复/行动                 │
              └────┬──────────┬─────────────────┘
                   │          │
          ┌────────▼──┐  ┌───▼──────────┐
          │  工具调用   │  │   记忆系统    │
          │ (Tools)    │  │ (Memory)     │
          │ • MCP      │  │ • 短期对话   │
          │ • Function │  │ • 长期知识   │
          │ • API      │  │ • 向量记忆   │
          └────────┬───┘  └───┬──────────┘
                   │          │
                   └────┬─────┘
                        ▼
              ┌──────────────────────────────────┐
              │         执行 & 反馈               │
              │   • 调用结果                      │
              │   • 环境状态                      │
              │   • 错误处理                      │
              └──────────────────────────────────┘
```

### Agent 工作循环 (Agent Loop)

```
1. 感知 (Perceive) — 接收用户输入和环境状态
2. 思考 (Think)    — LLM 分析当前状态，决定下一步
3. 行动 (Act)      — 调用工具或生成回复
4. 观察 (Observe)  — 接收工具执行结果
   └──→ 回到步骤 2，直到任务完成
```

## 三、主流 Agent 设计模式

### 3.1 ReAct 模式 (Reasoning + Acting)

最基础的 Agent 模式，交替执行推理和行动：

```
Thought: 用户想查询天气，我需要调用天气 API
Action: call_weather_api(city="北京")
Observation: {"temp": 25, "weather": "晴"}
Thought: 获取到天气数据，可以回复用户
Action: 回复用户天气信息
```

### 3.2 Plan-and-Execute 模式

先规划、后执行：

```
Plan:
  1. 搜索相关论文 ✅
  2. 下载 PDF 文件 ✅
  3. 提取关键信息 ✅
  4. 生成总结报告 ⏳
Execute: 按顺序执行每个步骤
```

### 3.3 多 Agent 协作模式

多个专业化 Agent 协同工作：

```
┌─────────────────────────────────────────────┐
│              Orchestrator Agent              │
│            (协调者/管理者 Agent)              │
└────┬──────────┬──────────┬──────────────────┘
     │          │          │
  ┌──▼──┐   ┌──▼──┐   ┌──▼──┐
  │研究员│   │编码员│   │审查员│
  │Agent│   │Agent│   │Agent│
  └─────┘   └─────┘   └─────┘
```

## 四、Agent 关键组件详解

### 4.1 工具系统 (Tools)

| 类型 | 示例 | 接入方式 |
|------|------|---------|
| 信息检索 | 网页搜索、数据库查询 | MCP / Function Calling |
| 文件操作 | 读写文件、图片处理 | 本地 SDK / MCP |
| API 调用 | 第三方服务集成 | REST API / MCP |
| 代码执行 | Python/JS 沙箱 | 本地运行时 |
| 浏览器 | 网页自动化 | Browser MCP |

### 4.2 记忆系统 (Memory)

| 类型 | 存储位置 | 生命周期 | 用途 |
|------|---------|---------|------|
| 短期记忆 | Context Window | 单次会话 | 当前对话上下文 |
| 长期记忆 | 向量数据库/文件 | 跨会话 | 用户偏好、知识积累 |
| 工作记忆 | Agent 内部状态 | 单任务 | 任务进度、中间结果 |

### 4.3 规划能力 (Planning)

| 方式 | 说明 | 适用场景 |
|------|------|---------|
| 即时规划 | 每步动态决策 | 简单任务、交互式任务 |
| 预规划 | 先规划再执行 | 复杂多步任务 |
| 分层规划 | 子目标分解 | 超复杂任务 |

## 五、主流 Agent 框架对比

| 框架 | 开发商 | 语言 | 特色 | 适用场景 |
|------|--------|------|------|---------|
| LangChain Agent | LangChain | Python/JS | 生态丰富 | 通用 Agent 开发 |
| AutoGen | Microsoft | Python | 多 Agent 对话 | 多 Agent 协作 |
| CrewAI | CrewAI | Python | 角色化 Agent | 团队模拟 |
| Claude Agent SDK | Anthropic | JS/Python | 深度工具集成 | Claude 生态 |
| OpenAI Agents SDK | OpenAI | Python | 简洁设计 | OpenAI 生态 |

## 六、实践经验与注意事项

### 6.1 常见陷阱

1. **循环陷阱**：Agent 在错误分支中无限循环 → 设置最大迭代次数
2. **幻觉传播**：一步错误导致后续全错 → 加验证节点
3. **工具选择错误**：Agent 选了错的工具 → 优化工具描述
4. **上下文超限**：多步操作导致上下文爆炸 → 定期总结压缩

### 6.2 最佳实践

- **清晰的工具描述**：每个工具的名称和描述要精确
- **渐进式授权**：高风险操作需用户确认
- **错误处理**：每个工具调用都要处理失败场景
- **日志记录**：记录每个步骤的思考和行动，便于调试

## 七、相关资源

- [LLM 基础](llm-basics.md) — Agent 的"大脑"工作原理
- [Function Calling 机制](function-calling.md) — Agent 调用工具的核心能力
- [MCP 协议](mcp-protocol.md) — 工具接入的标准化协议
- [AutoGen 多 Agent 框架](../tools/autogen-intro.md)
- [CrewAI 多 Agent 协作](../tools/crewai-intro.md)
