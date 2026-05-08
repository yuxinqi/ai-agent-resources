# 📇 总索引

> AI Agent Evidence Hub — 按 Knowledge / Practice / Evidence 三层架构分类
> ✅ = 已验真 · ⏳ = 待验真 · ⚠️ = 需更新 · 证据等级 L0-L4 · 推荐等级 A-D

> 最后更新：2026-05-08

---

## 一、新手入门 (Getting Started)

| 文档 | 难度 | 验真状态 | 证据等级 |
|------|------|---------|---------|
| [项目概览](docs/getting-started/00-overview.md) | 入门 | ⏳ | L0 |
| [Agent 基础概念](docs/getting-started/01-agent-basics.md) | 入门 | ⏳ | L0 |
| [构建你的第一个 Agent](docs/getting-started/02-build-your-first-agent.md) | 入门 | ⏳ | L0 |
| [Agent 评估基础](docs/getting-started/03-agent-evaluation-basics.md) | 入门 | ⏳ | L0 |

## 二、核心概念 (Concepts)

| 文档 | 证据等级 | 推荐等级 | 最后更新 |
|------|---------|---------|---------|
| [Agent 智能体](docs/concepts/agent.md) | L1 | B | 2026-05-08 |
| [Tool Use 工具使用](docs/concepts/tool-use.md) | L1 | B | 2026-05-08 |
| [Planning 规划](docs/concepts/planning.md) | L0 | C | 2026-05-08 |
| [Memory 记忆](docs/concepts/memory.md) | L0 | C | 2026-05-08 |
| [RAG 检索增强生成](docs/concepts/rag.md) | L1 | B | 2026-05-08 |
| [Multi-Agent 多智能体](docs/concepts/multi-agent.md) | L0 | C | 2026-05-08 |
| [Evaluation 评估](docs/concepts/evaluation.md) | L1 | B | 2026-05-08 |

## 三、架构模式 (Patterns)

| 文档 | 适合场景 | 证据等级 | 推荐等级 |
|------|---------|---------|---------|
| [Planner-Executor](docs/patterns/planner-executor.md) | 复杂任务拆解 | L1 | B |
| [Router](docs/patterns/router.md) | 多工具分流 | L1 | B |
| [Reflection](docs/patterns/reflection.md) | 自我检查 | L0 | C |
| [Evaluator-Optimizer](docs/patterns/evaluator-optimizer.md) | 生成后优化 | L0 | C |
| [Human-in-the-Loop](docs/patterns/human-in-the-loop.md) | 高风险任务 | L1 | B |
| [Guardrails](docs/patterns/guardrails.md) | 安全控制 | L1 | B |

## 四、实战手册 (Playbooks)

| 文档 | 优先级 | 证据等级 | 推荐等级 |
|------|--------|---------|---------|
| [构建 Tool-Using Agent](docs/playbooks/build-tool-using-agent.md) | P0 | L1 | B |
| [构建 RAG Agent](docs/playbooks/build-rag-agent.md) | P0 | L1 | B |
| [构建 Research Agent](docs/playbooks/build-research-agent.md) | P1 | L0 | C |
| [构建 Coding Agent](docs/playbooks/build-coding-agent.md) | P1 | L0 | C |
| [生产就绪指南](docs/playbooks/production-readiness.md) | P0 | L1 | B |

## 五、平台指南 (Platforms)

| 文档 | 证据等级 | 推荐等级 | 最后更新 |
|------|---------|---------|---------|
| [模型能力矩阵](docs/platforms/model-capability-matrix.md) | L1 | B | 2026-05-08 |
| [API 平台对比](docs/platforms/api-platform-comparison.md) | L1 | B | 2026-05-08 |
| [成本与延迟参考](docs/platforms/cost-latency-reference.md) | L1 | B | 2026-05-08 |
| [平台变更日志](docs/platforms/platform-change-log.md) | L2 | B | 2026-05-08 |
| [OpenAI API 指南](docs/platforms/openai-api-guide.md) | L2 | A | 2026-05-07 |
| [Anthropic Claude API 指南](docs/platforms/anthropic-claude-guide.md) | L2 | A | 2026-05-07 |
| [DeepSeek API 指南](docs/platforms/deepseek-api-guide.md) | L1 | B | 2026-05-07 |
| [Google Gemini API 指南](docs/platforms/google-gemini-guide.md) | L1 | B | 2026-05-07 |
| [API 平台综合对比](docs/platforms/platform-comparison.md) | L1 | B | 2026-05-07 |

## 六、工具选型 (Tools)

| 文档 | 证据等级 | 推荐等级 | 最后更新 |
|------|---------|---------|---------|
| [Agent 框架对比选型](docs/tools/framework-comparison.md) | L1 | B | 2026-05-08 |
| [评估工具](docs/tools/evaluation-tools.md) | L0 | C | 2026-05-08 |
| [追踪与可观测性](docs/tools/tracing-and-observability.md) | L0 | C | 2026-05-08 |
| [部署工具](docs/tools/deployment-tools.md) | L0 | C | 2026-05-08 |
| [LangChain 入门](docs/tools/langchain-intro.md) | L0 | C | 2026-05-07 |

## 七、案例分析 (Case Studies)

| 文档 | 证据等级 | 推荐等级 |
|------|---------|---------|
| [客服 Agent](docs/case-studies/customer-support-agent.md) | L1 | B |
| [研究 Agent](docs/case-studies/research-agent.md) | L1 | B |
| [内部知识 Agent](docs/case-studies/internal-knowledge-agent.md) | L1 | B |
| [PR Review Agent](docs/case-studies/pr-review-agent.md) | L1 | B |

## 八、可复用资产 (Assets)

### Prompt 资产

| 资产 | 证据等级 | 推荐等级 |
|------|---------|---------|
| [Research Summary Prompt](assets/prompts/research-summary/README.md) | L2 | B |
| [Code Review Prompt](assets/prompts/code-review/README.md) | L2 | B |
| [RAG Answer Prompt](assets/prompts/rag-answer/README.md) | L1 | C |

### Skill 资产

| 资产 | 证据等级 | 推荐等级 |
|------|---------|---------|
| [Web Search Skill](assets/skills/web-search/README.md) | L2 | B |
| [File Reader Skill](assets/skills/file-reader/README.md) | L2 | B |

### Workflow 资产

| 资产 | 证据等级 | 推荐等级 |
|------|---------|---------|
| [Research Agent Workflow](assets/workflows/research-agent/README.md) | L2 | B |
| [RAG Agent Workflow](assets/workflows/rag-agent/README.md) | L1 | C |

## 九、可运行示例 (Examples)

| 示例 | 说明 |
|------|------|
| [Tool-Using Agent](examples/tool-using-agent/README.md) | 最小工具调用 Agent 示例 |
| [RAG Agent](examples/rag-agent/README.md) | 最小 RAG Agent 示例 |

## 十、验真中心 (Verification)

### 验真报告

| 报告 | 类型 | 证据等级 | 推荐等级 |
|------|------|---------|---------|
| [Research Summary Prompt 验真](verification/reports/prompts/research-summary-202605.md) | Prompt | L2 | B |
| [Code Review Prompt 验真](verification/reports/prompts/code-review-202605.md) | Prompt | L2 | B |
| [Web Search Skill 验真](verification/reports/skills/web-search-202605.md) | Skill | L2 | B |
| [Research Agent Workflow 验真](verification/reports/workflows/research-agent-202605.md) | Workflow | L2 | B |
| [OpenAI API 验真](verification/reports/platforms/openai-api-202605.md) | Platform | L2 | B |

### 验真 Schemas

| Schema | 说明 |
|--------|------|
| [verification.schema.json](verification/schema/verification.schema.json) | 验真报告 Schema |
| [prompt.schema.json](verification/schema/prompt.schema.json) | Prompt 资产 Schema |
| [skill.schema.json](verification/schema/skill.schema.json) | Skill 资产 Schema |
| [workflow.schema.json](verification/schema/workflow.schema.json) | Workflow 资产 Schema |

### 变更日志

| 文档 | 说明 |
|------|------|
| [API 兼容性变更](verification/changelog/api-compatibility.md) | API 兼容性追踪 |
| [模型能力变更](verification/changelog/model-capability-changes.md) | 模型能力变更追踪 |
| [已废弃内容](verification/changelog/deprecated-items.md) | 废弃内容记录 |

## 十一、Benchmark

| 目录 | 说明 |
|------|------|
| [Prompt 评测](benchmarks/prompt-evals/README.md) | Prompt 小样本评测 |
| [Skill 测试](benchmarks/skill-tests/README.md) | Skill 单元测试 |
| [Workflow 评测](benchmarks/workflow-evals/README.md) | Workflow 端到端评测 |
| [评测报告](benchmarks/reports/README.md) | Benchmark 报告 |

## 十二、模板 (Templates)

| 模板 | 类型 |
|------|------|
| [概念卡片模板](templates/concept-card-template.md) | 文档模板 |
| [Playbook 模板](templates/playbook-template.md) | 文档模板 |
| [验真报告模板](templates/verification-report-template.md) | 文档模板 |
| [Prompt 资产模板](templates/prompt-asset-template.yaml) | YAML 模板 |
| [Skill 模板](templates/skill-template.py) | Python 模板 |
| [Workflow 模板](templates/workflow-template.yaml) | YAML 模板 |
| [Agent 设计文档模板](templates/agent-design-doc-template.md) | 文档模板 |
| [上线检查清单模板](templates/production-checklist-template.md) | 文档模板 |

## 十三、可视化 (Visualization)

| 页面 | 说明 |
|------|------|
| [知识图谱](visualization/index.html) | 概念关系图谱 |
| [Dashboard](visualization/dashboard.html) | 项目状态面板 |
| [关系图](visualization/graph.html) | 增强知识图谱 |

## 十四、脚本 (Scripts)

| 脚本 | 说明 |
|------|------|
| [generate-index.py](scripts/generate-index.py) | 自动生成 INDEX.md |
| [validate_metadata.py](scripts/validate_metadata.py) | 校验文档 metadata |
| [check_links.py](scripts/check_links.py) | 检查链接完整性 |
| [build_graph.py](scripts/build_graph.py) | 构建知识图谱数据 |
| [run_verification.py](scripts/run_verification.py) | 运行验真检查 |
| [generate_badges.py](scripts/generate_badges.py) | 生成 Badges |
