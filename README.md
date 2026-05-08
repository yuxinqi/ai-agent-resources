# AI Agent Evidence Hub

> 让每一个 AI Agent 实践都有路径可循、有代码可跑、有证据可查、有结果可复现。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Last Verified](https://img.shields.io/badge/Last_Verified-2026--05--08-green.svg)]()
[![Metadata Check](https://img.shields.io/badge/Metadata_Check-passing-brightgreen.svg)]()
[![Link Check](https://img.shields.io/badge/Link_Check-passing-brightgreen.svg)]()
[![Verified Assets](https://img.shields.io/badge/Verified_Assets-7-orange.svg)]()
[![Contributors](https://img.shields.io/badge/Contributors-welcome-purple.svg)]()

---

## 这个项目解决什么问题

AI Agent 领域正在经历爆发式增长，但实践者普遍面临四个核心困境：

1. **信息更新太快** — 今天能用的 API，明天可能就变了；上周的最佳实践，这周可能已经过时。你收藏的教程，可能正在悄悄误导你。
2. **概念混乱不堪** — Agent、Workflow、Tool、Skill、MCP、RAG……每个人都在用这些词，但每个人说的不一定是同一件事。概念之间是什么关系？哪些是基础？哪些是衍生？
3. **工具频繁变动** — LangChain 昨天还在用这个接口，今天换了那个；新框架每周冒出来，选型全靠运气。跟着某个框架走，很可能过两个月就要推倒重来。
4. **难以复现结果** — 博客文章说"我做了个 Agent 效果很好"，但你照着做就是跑不通。没有环境、没有版本、没有完整代码，只有截图和结论。

**AI Agent Evidence Hub 的目标：不只是收藏链接，而是让每一条知识都经得起验证，让每一个实践都能被复现。**

---

## 和普通 Awesome List 有什么不同

| 对比项 | 普通 Awesome List | 本项目 |
|--------|-------------------|--------|
| 内容形式 | 链接集合 + 一句话描述 | 结构化文档 + 验真报告 + 可运行代码 |
| 可信度 | 无验证，内容可能已过时 | 每条关键信息附带验真时间、评级、验证流程 |
| 实用性 | 知道"有什么"，不知道"怎么用" | 按场景编排实践路径，提供可运行的 Playbook |
| 更新机制 | 依赖人工维护，容易腐烂 | 验真周期驱动更新，CI 自动检查链接与元数据 |
| 使用路径 | 浏览 → 离开 | 学习概念 → 跟着实践 → 验证结果 → 贡献回社区 |

---

## 你可以用它做什么

- 按照实践路径从零搭建一个 Tool-Using Agent，每一步都有代码可参考、有结果可验证
- 搭建一个 RAG 系统，从概念理解到向量数据库选型到效果评估，完整闭环
- 对比主流 Agent 框架的实际表现，不只是看 GitHub Star 数，而是看验真报告里的真实数据
- 快速验证一条信息的时效性——每个知识点都有验真日期和评级
- 按图索骥地学习 AI Agent 概念——三层架构让概念之间关系清晰可见
- 贡献你的实践结果，帮助后来者少踩坑

---

## 三层架构

本项目采用 **Knowledge → Practice → Evidence** 三层架构组织内容：

```
┌─────────────────────────────────────────────────────┐
│                 Evidence Layer                       │
│           验真报告 · 效果评级 · 复现记录              │
│     "这条信息最后在什么时候、什么环境下验证通过"        │
├─────────────────────────────────────────────────────┤
│                 Practice Layer                       │
│        Playbook · 代码示例 · 场景实战指南             │
│       "照着做就能跑通，跑通了就有证据"                 │
├─────────────────────────────────────────────────────┤
│                 Knowledge Layer                      │
│       概念文档 · 框架对比 · API 平台指南              │
│      "理解概念是正确实践的前提"                        │
└─────────────────────────────────────────────────────┘
```

- **Knowledge Layer** — 稳定的基础知识和概念，变更频率低。包括 AI/Agent 核心概念、API 平台申请指南、提示词工程基础等。
- **Practice Layer** — 面向场景的实践路径，按"跟着做就能跑通"的标准编写。包括 Tool-Using Agent Playbook、RAG Agent Playbook、框架对比实战等。
- **Evidence Layer** — 所有内容的可信度保障。每条关键信息都有验真报告，标注验证时间、环境、评级和完整流程。

---

## 快速开始

| 我想…… | 去这里 |
|---------|--------|
| 了解项目整体结构和使用方式 | [Getting Started](docs/getting-started.md) |
| 搭建一个能调用工具的 Agent | [Tool-Using Agent Playbook](docs/playbooks/tool-using-agent.md) |
| 搭建一个 RAG 检索增强系统 | [RAG Agent Playbook](docs/playbooks/rag-agent.md) |
| 对比主流 Agent 框架的优劣 | [框架对比](docs/playbooks/framework-comparison.md) |
| 了解验真机制和验证流程 | [验真中心](verification/README.md) |

```bash
git clone https://github.com/yuxinqi/ai-agent-resources.git
cd ai-agent-resources

# 启动本地可视化
python3 -m http.server 8000
# 浏览器打开 http://localhost:8000/visualization/
```

---

## 项目结构

```
ai-agent-resources/
├── docs/
│   ├── concepts/          # Knowledge Layer — 核心概念
│   │   ├── llm-basics.md
│   │   ├── agent-architecture.md
│   │   ├── rag-retrieval.md
│   │   ├── function-calling.md
│   │   ├── mcp-protocol.md
│   │   ├── embedding-vector-db.md
│   │   └── fine-tuning.md
│   ├── platforms/         # Knowledge Layer — API 平台指南
│   │   ├── openai-api-guide.md
│   │   ├── anthropic-claude-guide.md
│   │   ├── google-gemini-guide.md
│   │   ├── deepseek-api-guide.md
│   │   └── platform-comparison.md
│   ├── prompts/           # Knowledge Layer — 提示词工程
│   │   ├── prompt-engineering-basics.md
│   │   ├── chain-of-thought.md
│   │   ├── prompt-templates.md
│   │   └── system-prompt-best-practices.md
│   ├── skills/            # Knowledge Layer — Skills 资源
│   │   ├── skills-overview.md
│   │   ├── writing-skills.md
│   │   ├── code-review-skill.md
│   │   ├── data-extraction-skill.md
│   │   └── summarization-skill.md
│   ├── tools/             # Knowledge Layer — 工具与框架
│   │   └── langchain-intro.md
│   ├── playbooks/         # Practice Layer — 场景实战 Playbook
│   │   ├── tool-using-agent.md
│   │   ├── rag-agent.md
│   │   └── framework-comparison.md
│   ├── workflows/         # Knowledge Layer — 流程化指南
│   │   ├── ai-app-development.md
│   │   ├── api-selection-migration.md
│   │   ├── build-rag-system.md
│   │   └── prompt-engineering-workflow.md
│   └── getting-started.md # 快速入门
├── verification/          # Evidence Layer — 验真中心
│   ├── README.md
│   ├── prompts/
│   ├── platforms/
│   └── skills/
├── visualization/         # 可视化
│   └── index.html
├── scripts/               # 辅助脚本
├── INDEX.md               # 自动生成的总索引
├── CONTRIBUTING.md
├── ROADMAP.md
├── CHANGELOG.md
└── LICENSE
```

---

## 贡献指南

我们欢迎各种形式的贡献：新增内容、更新验真、修正错误、完善实践路径。

详细规范请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## 许可

本项目基于 [MIT License](LICENSE) 开源。
