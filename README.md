# AI Agent Resources — 开放、可验真的 AI 资料知识库

> **让每一条 AI 知识都有据可查、有时可依、有源可溯。**

---

## 🧭 项目理念

AI 与 Agent 技术正以史无前例的速度演进。信息爆炸的同时也带来了三个核心困境：

| 困境 | 我们的解法 |
|------|-----------|
| **真伪难辨** — 概念、工具、API 频繁更新，旧信息误导性极强 | 建立 **验真机制**，每条关键信息附带验真时间、效果评级、验证流程 |
| **碎片化** — 资料散落于博客、文档、推文、论文之间 | **结构化整理** + **关系图谱**，将孤立知识点连接为知识网络 |
| **上手难** — 从概念到实践的门槛高，信息查找成本大 | **流程化组织**，按"从入门到应用"的路径编排资料，降低使用难度 |

## 📦 内容体系

```
ai-agent-resources/
├── docs/               # 📝 核心文档
│   ├── concepts/       # AI/Agent 核心概念（含关系图谱索引）
│   ├── platforms/      # 主流 API 平台申请与使用指南
│   ├── prompts/        # 提示词工程资源
│   ├── skills/         # Skills / Tools 资源
│   ├── tools/          # 开发工具与框架
│   └── workflows/      # 流程化实践指南
├── verification/       # ✅ 验真中心
│   ├── prompts/        # 提示词验真报告
│   ├── skills/         # Skills 验真报告
│   └── platforms/      # 平台信息验真
├── visualization/      # 📊 HTML 可视化
│   ├── index.html      # 可视化总入口
│   └── ...             # 更多交互式可视化
└── scripts/            # 🔧 辅助脚本
```

## ✨ 核心特色

### ✅ 验真系统 (Verification System)

每条信息附带 **验真标签**：

```
📅 验真日期：2026-05-07
📋 验真流程：[步骤说明]
⭐ 效果评级：[A/B/C/D]
🔗 参考来源：[链接]
```

### 🔗 相关性分析

通过文档内嵌的关系标记（`related`, `depends_on`, `follows`）建立知识图谱，支持可视化浏览。

### 🧩 流程化组织

按"角色→场景→任务"组织资料：

- **AI 应用开发者** → 需要选模型 → 查看模型对比 → 申请 API → 阅读最佳实践
- **Prompt Engineer** → 需要提升效果 → 查看技能验真 → 参考高级技巧

## 🚀 快速开始

```bash
# 克隆项目
git clone https://github.com/yuxinqi/ai-agent-resources.git
cd ai-agent-resources

# （可选）启动本地可视化
python3 -m http.server 8000
# 打开浏览器访问 http://localhost:8000/visualization/
```

## 📄 许可

MIT License
