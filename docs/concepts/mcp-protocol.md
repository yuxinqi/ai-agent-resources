---
title: MCP 协议 — Model Context Protocol
category: concepts
tags: [MCP, 协议, 工具集成, 标准化]
related:
  - agent-architecture.md
  - function-calling.md
depends_on:
  - agent-architecture.md
verification: false
created: 2026-05-07
updated: 2026-05-07
---

<!-- related_to: docs/concepts/agent-architecture.md, docs/concepts/function-calling.md -->

# MCP 协议 — Model Context Protocol

## 📋 概念速览

| 项目 | 内容 |
|------|------|
| 全称 | Model Context Protocol (模型上下文协议) |
| 提出者 | Anthropic (2024 年底) |
| 定位 | AI 模型与外部工具/数据源之间的开放标准协议 |
| 类比 | "AI 的 USB-C 接口" — 统一工具接入标准 |
| 状态 | 开源，快速增长中 |
| ⚠️ 状态 | ⏳ 待验真 |

---

## 一、为什么需要 MCP

在 MCP 出现之前，每个 AI Agent 框架都有自己的工具接入方式：

```
LangChain Agent ──→ 自建工具系统
AutoGen        ──→ 自建工具系统
Claude Agent   ──→ 自建工具系统
OpenAI GPTs    ──→ 自建工具系统
     ↓
每个框架各自为政，工具开发者需要为每个框架分别适配
```

**MCP 的目标**：提供一个**统一的、开放的**协议标准，让工具一次接入，随处可用。

## 二、MCP 架构

```
┌──────────────────────────────────────┐
│            MCP Host (主机)            │
│    • Claude Desktop                  │
│    • VS Code + Claude Extension      │
│    • 自定义 MCP 客户端               │
└──────────────┬───────────────────────┘
               │ MCP Protocol (JSON-RPC)
               │
     ┌─────────┴──────────┐
     │    MCP Server      │
     │  (工具提供方)       │
     │                    │
     │ • 文件系统工具      │
     │ • 数据库查询工具    │
     │ • 网页搜索工具      │
     │ • API 集成工具      │
     └────────────────────┘
```

### 核心组件

| 组件 | 角色 | 说明 |
|------|------|------|
| **MCP Host** | 客户端 | 运行 LLM 和 MCP 客户端的应用 |
| **MCP Server** | 服务端 | 暴露工具、资源和提示词的外部服务 |
| **MCP Protocol** | 协议 | JSON-RPC 2.0 基础上的通信规范 |

### 支持的三大原语

| 原语 | 说明 | 类比 |
|------|------|------|
| **Tools** (工具) | 可被 LLM 调用的函数 | API 端点 |
| **Resources** (资源) | 可被 LLM 读取的数据 | GET 请求 |
| **Prompts** (提示词) | 预定义的提示词模板 | 模板引擎 |

## 三、MCP 工作流程

```
用户请求 → LLM 分析 → 决定调用工具
                        │
                        ▼
           Host 通过 MCP 协议向 Server 发送请求
                        │
                        ▼
           Server 执行操作并返回结果
                        │
                        ▼
           LLM 结合工具结果生成最终回复
```

### 实际示例

```json
// Host → Server: 调用工具请求
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "read_file",
    "arguments": {
      "path": "/data/report.md"
    }
  },
  "id": 1
}

// Server → Host: 工具执行结果
{
  "jsonrpc": "2.0",
  "result": {
    "content": [
      { "type": "text", "text": "# 报告内容..." }
    ]
  },
  "id": 1
}
```

## 四、MCP vs 其他方案

| 特性 | MCP | Function Calling | 自定义 Tool System |
|------|-----|-----------------|-------------------|
| 开放性 | ✅ 开放标准 | ❌ 平台锁定 | ❌ 自建 |
| 标准化 | ✅ 统一协议 | ⚠️ 各平台不同 | ❌ 无标准 |
| 动态发现 | ✅ 支持 | ⚠️ 部分支持 | ❌ 需硬编码 |
| 生态 | 快速增长 | 成熟 | 取决于框架 |
| 适用场景 | 通用工具集成 | 同平台工具 | 简单场景 |

## 五、如何搭建一个 MCP Server

### 快速开始 (Python)

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server

# 创建 MCP Server
app = Server("my-tools")

@app.list_tools()
async def list_tools():
    return [
        {
            "name": "get_weather",
            "description": "获取指定城市的天气",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"}
                }
            }
        }
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "get_weather":
        city = arguments["city"]
        # 调用天气 API...
        return {"content": [{"type": "text", "text": f"{city} 天气晴朗"}]}

if __name__ == "__main__":
    import anyio
    anyio.run(stdio_server(app))
```

### 配置 MCP

在 Claude Desktop 或支持 MCP 的客户端中配置：

```json
{
  "mcpServers": {
    "my-tools": {
      "command": "python",
      "args": ["path/to/server.py"]
    }
  }
}
```

## 六、相关资源

- [Agent 架构](agent-architecture.md) — MCP 是 Agent 的工具基础
- [Function Calling 机制](function-calling.md) — MCP 的前身与补充
- [API 平台申请指南](../platforms/openai-api-guide.md)
