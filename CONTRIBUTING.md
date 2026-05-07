# 贡献指南

感谢您想为 **AI Agent Resources** 做出贡献！本项目的核心在于**可验真、结构化、流程化**，请在贡献时遵循以下规范。

## ✍️ 内容规范

### 1. 文档模板

每篇核心文档应包含以下元信息（放在文档开头）：

```markdown
---
title: 文档标题
category: concepts | platforms | prompts | skills | tools | workflows
tags: [关键词1, 关键词2]
related: [相关文档路径]
depends_on: [前置知识文档路径]
verification: true | false  # 是否已验真
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

### 2. 验真要求

- **所有平台申请指南**必须在发布前完成验真
- **提示词和 Skills**必须附带效果验证
- **过时信息**请标注 `⚠️ 待更新` 并提 Issue
- 验真格式请参考 `verification/` 目录下的模板

### 3. 相关性标记

在文档中标记与其他文档的关系：

```markdown
<!-- related_to: docs/concepts/agent-framework.md -->
<!-- depends_on: docs/concepts/llm-basics.md -->
<!-- follows: docs/platforms/openai-api-guide.md -->
```

## 🔄 工作流程

```
Fork 本仓库 → 创建分支 → 编写/修改内容 → 添加/更新验真 → 提交 PR
```

### PR 要求

1. PR 标题格式：`[类型] 简短描述`
   - `[new]` 新增内容
   - `[update]` 更新内容
   - `[verify]` 验真更新
   - `[fix]` 错误修正
2. 每个 PR 应聚焦于单一主题
3. 如果涉及验真，请在 PR 描述中说明验真流程

## 📋 目录结构说明

```
docs/concepts/      # AI 概念：LLM、Agent、RAG、MCP 等
docs/platforms/     # API 平台：OpenAI、Claude、Gemini 等申请与使用
docs/prompts/       # 提示词：模板、技巧、最佳实践
docs/skills/        # Skills：可用技能的定义、使用方式
docs/tools/         # 工具：开发框架、SDK、平台
docs/workflows/     # 流程：从入门到上手的完整路径
verification/       # 验真：所有验真报告的存档
visualization/      # 可视化：HTML 交互页面
```

## 🖥️ 本地开发

```bash
# 1. 生成 INDEX.md
python3 scripts/generate-index.py

# 2. 预览可视化页面
python3 -m http.server 8000
# 打开浏览器访问 http://localhost:8000/visualization/

# 3. 检查 INDEX.md 是否最新（CI 使用）
python3 scripts/generate-index.py --check
```

## ❓ 有问题？

请提交 [Issue](https://github.com/yuxinqi/ai-agent-resources/issues) 或直接开启 Discussion。
