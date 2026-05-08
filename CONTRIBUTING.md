# 贡献指南

感谢您想为 **AI Agent Resources** 做出贡献！本项目的核心在于**可验真、结构化、流程化**，请在贡献时遵循以下规范。

## 内容规范

### 1. 文档 Frontmatter

每篇核心文档应包含以下元信息（放在文档开头）：

```markdown
---
title: 文档标题
category: concepts | platforms | prompts | skills | tools | workflows | patterns | playbooks | case-studies
tags: [关键词1, 关键词2]
related: [相关文档路径]
depends_on: [前置知识文档路径]
verification: true | false
evidence_level: L0 | L1 | L2 | L3 | L4
rating: A | B | C | D
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

### 2. 证据等级

所有文档应标注证据等级（`evidence_level`）：

| 等级 | 含义 | 适用场景 |
|------|------|---------|
| L0 | 官方文档直接验证 | API 端点、官方定价 |
| L1 | 实际操作验证 | 注册流程、SDK 示例 |
| L2 | 交叉验证 | 框架对比、最佳实践 |
| L3 | 理论推导 | 架构设计、趋势分析 |
| L4 | 待验证 | 新创建的内容 |

### 3. 评级

已验真的文档应标注评级（`rating`）：

| 评级 | 含义 | 通过率 |
|------|------|--------|
| A | 完全验证通过 | ≥90% |
| B | 大部分验证通过 | ≥70% |
| C | 部分验证通过 | ≥50% |
| D | 待验真 | <50% |

### 4. 验真要求

- **所有平台申请指南**必须在发布前完成验真
- **提示词和技能**必须附带效果验证
- **过时信息**请标注 `⚠️ 待更新` 并提 Issue
- 验真格式请参考 `verification/` 目录下的模板和报告

## 工作流程

```
Fork 本仓库 → 创建分支 → 编写/修改内容 → 添加/更新验真 → 提交 PR
```

### PR 要求

1. PR 标题格式：`[类型] 简短描述`
   - `[new]` 新增内容
   - `[update]` 更新内容
   - `[verify]` 验真更新
   - `[fix]` 错误修正
   - `[restructure]` 结构重组
2. 每个 PR 应聚焦于单一主题
3. 如果涉及验真，请在 PR 描述中说明验真流程
4. PR 模板中包含证据等级和影响层级字段

## 目录结构说明

```
docs/
├── getting-started/   # 入门指南：快速上手路径
├── concepts/          # 核心概念：LLM、Agent、RAG、MCP 等
├── platforms/         # API 平台：OpenAI、Claude、Gemini 等
├── prompts/           # 提示词：模板、技巧、最佳实践
├── skills/            # 技能：可用技能的定义与使用
├── tools/             # 工具：开发框架、SDK、平台
├── workflows/         # 流程：从入门到上手的完整路径
├── patterns/          # 设计模式：常见架构模式
├── playbooks/         # 实战手册：场景化操作指南
└── case-studies/      # 案例研究：实际项目案例分析

verification/
├── reports/           # 验真报告（按类型分类）
├── changelog/         # 变更日志
└── */template.md      # 验真模板

benchmarks/
├── prompt-evals/      # 提示词评估基准
├── skill-tests/       # 技能测试基准
├── workflow-evals/    # 工作流评估基准
└── reports/           # 基准测试报告

visualization/         # 可视化页面
assets/                # 资源文件
examples/              # 示例代码
```

## 本地开发

```bash
# 1. 生成 INDEX.md
python3 scripts/generate-index.py

# 2. 验证 Frontmatter
python3 scripts/validate_metadata.py

# 3. 检查链接
python3 scripts/check_links.py

# 4. 构建知识图谱
python3 scripts/build_graph.py

# 5. 生成 Badges
python3 scripts/generate_badges.py

# 6. 运行验真检查
python3 scripts/run_verification.py --check-expiry --stats

# 7. 预览可视化页面
python3 -m http.server 8000
# 打开浏览器访问 http://localhost:8000/visualization/

# 8. CI 检查（等效于 GitHub Actions）
python3 scripts/generate-index.py --check
python3 scripts/validate_metadata.py --ci
python3 scripts/check_links.py --ci
```

## CI/CD 流程

本仓库使用 GitHub Actions 进行自动化检查：

| Workflow | 触发条件 | 说明 |
|----------|---------|------|
| validate-metadata.yml | PR/Push 到 docs/ | 验证 frontmatter 格式和字段 |
| check-links.yml | PR + 每周一 | 检查内部和外部链接 |
| update-index.yml | Push 到 master | 自动更新 INDEX.md 和部署 Pages |
| build-graph.yml | Push 到 master | 构建知识图谱数据 |
| smoke-test-assets.yml | PR/Push 到 assets/ | 验证资源文件完整性 |

## 有问题？

请提交 [Issue](https://github.com/yuxinqi/ai-agent-resources/issues) 或直接开启 Discussion。
