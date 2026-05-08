# 项目路线图

> 本路线图记录 AI Agent Evidence Hub 的阶段性目标与交付计划。

---

## Phase 1 — 重构定位和标准（第1周）

将项目从"资料合集"升级为"Evidence Hub"，建立三层架构标准。

### P0 — 必须完成

- [ ] 重写 README.md，明确 "AI Agent Evidence Hub" 定位
- [ ] 创建 ROADMAP.md 和 CHANGELOG.md
- [ ] 定义三层架构（Knowledge / Practice / Evidence）的目录规范
- [ ] 编写 Playbook 编写规范文档
- [ ] 创建 `docs/playbooks/` 目录结构

### P1 — 应当完成

- [ ] 更新 CONTRIBUTING.md，补充 Playbook 和验真贡献流程
- [ ] 更新 INDEX.md 生成脚本，支持 Playbook 和 Evidence 索引
- [ ] 清理现有文档的 frontmatter，统一元数据格式

---

## Phase 2 — 第一个可运行闭环：Tool-Using Agent（第2周）

从零到一跑通第一个高频场景，形成"概念 → 实践 → 验真"完整闭环。

### 交付文件

- [ ] `docs/playbooks/tool-using-agent.md` — Tool-Using Agent Playbook
  - 场景定义与目标
  - 前置知识清单（指向 Knowledge Layer）
  - 分步实践指南（含可运行代码）
  - 常见问题与排错
- [ ] `docs/getting-started.md` — 项目快速入门
- [ ] `verification/playbooks/tool-using-agent-verification.md` — Playbook 验真报告
- [ ] 更新 README.md 快速开始部分，链接到新 Playbook

---

## Phase 3 — 补第二个高频场景：RAG Agent（第3周）

覆盖第二大高频实践场景，验证三层架构的可扩展性。

### 交付文件

- [ ] `docs/playbooks/rag-agent.md` — RAG Agent Playbook
  - RAG 全流程实践（文档加载 → 切分 → Embedding → 检索 → 生成）
  - 多种向量数据库对比实战
  - 效果评估与调优方法
- [ ] `docs/playbooks/framework-comparison.md` — Agent 框架对比 Playbook
  - LangChain / LlamaIndex / CrewAI / AutoGen 实际使用对比
  - 基于 Playbook 的统一评估维度
- [ ] `verification/playbooks/rag-agent-verification.md` — RAG Playbook 验真报告
- [ ] `verification/playbooks/framework-comparison-verification.md` — 框架对比验真报告

---

## Phase 4 — 验证可视化与发布准备（第4周）

完善验真可视化，准备 v0.1 正式发布。

### 交付任务

- [ ] 更新 `visualization/index.html`，支持三层架构导航
- [ ] 添加 Playbook 验真状态可视化看板
- [ ] 完善所有现有文档的验真标签
- [ ] CI 流程增加 Playbook 代码块的可运行性检查
- [ ] 编写 v0.1 Release Notes
- [ ] 更新 README.md 中的 Badges 数据

---

## 第31–60天：扩展实战场景

在 v0.1 基础上扩展更多高频场景，覆盖 Agent 开发的主要痛点。

### 计划内容

- Multi-Agent 协作 Playbook（Agent 间通信、任务分配、冲突解决）
- Coding Agent Playbook（代码生成、审查、调试场景）
- Data Analysis Agent Playbook（数据分析、报表生成场景）
- MCP 集成 Playbook（Model Context Protocol 实战）
- 对应的验真报告和效果评估
- 各场景的 Common Pitfalls 文档

---

## 第61–90天：形成差异化壁垒

从"内容覆盖"走向"深度价值"，建立项目不可替代性。

### 计划内容

- Agent 效果 Benchmark 体系——建立可量化的评估标准
- 版本迁移追踪——框架/API 版本变更时自动触发验真更新
- 社区贡献者激励体系——验真贡献积分、Playbook 认证
- 英文版关键内容翻译
- 与其他开源项目的交叉验证（如 LangChain 官方文档的独立验证）
- 自动化验真流水线（CI 中集成 API 可达性检测、代码可运行性检测）

---

## v0.1 Release：Verified Agent Basics

**目标**：发布第一个可用的、经过验证的 AI Agent 实践基础包。

**包含内容**：
- 重构后的项目定位与三层架构
- Tool-Using Agent 完整 Playbook（含验真）
- RAG Agent 完整 Playbook（含验真）
- Agent 框架对比 Playbook（含验真）
- 项目快速入门指南
- 验真可视化看板
- 统一的贡献规范

**发布标准**：
- 所有 Playbook 代码可运行
- 所有验真报告评级 ≥ B
- README Badges 全部显示真实数据
- CI 流程全部通过
