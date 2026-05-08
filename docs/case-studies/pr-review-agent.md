---
id: case-pr-review
title: PR Review Agent 案例
type: case-study
level: advanced
status: draft
evidence_level: L2
practical_rating: B
last_reviewed: "2026-05-08"
valid_until: "2026-08-08"
related:
  - concept-agent
  - concept-tool-use
  - pattern-reflection
  - pattern-guardrails
depends_on:
  - concept-agent
  - concept-tool-use
tags:
  - case-study
  - code-review
  - pr-review
  - developer-tools
  - production
---

# PR Review Agent 案例

## 背景

某 50 人研发团队，每天 30-40 个 PR 需要 Review。Senior 工程师每天花 2-3 小时做 Code Review，但仍有 30% 的 PR 需要多轮修改。目标：Agent 先做第一轮自动 Review，标记潜在问题，人工只审查 Agent 标记的部分。

## 系统架构

```
PR 创建事件 (GitHub Webhook)
    │
    ▼
PR Agent
    ├── 获取 PR diff
    ├── 分析代码变更
    ├── 检查常见问题
    │   ├── Bug 模式检测
    │   ├── 安全漏洞扫描
    │   ├── 性能问题检测
    │   ├── 代码风格检查
    │   └── 测试覆盖率
    ├── 生成 Review 评论
    └── 提交到 GitHub PR
    │
    ▼
人工 Reviewer
    ├── 审查 Agent 标记的问题
    ├── 补充架构和业务逻辑审查
    └── Approve / Request Changes
```

## 技术选型

| 组件 | 选择 | 理由 |
|------|------|------|
| LLM | GPT-4o | 代码理解需要强模型 |
| 框架 | LangGraph | 多步骤流程 |
| 代码获取 | GitHub API | 原生集成 |
| 静态分析 | Ruff + Semgrep | 规则型检查不靠 LLM |
| 部署 | GitHub Actions | PR 事件触发 |

## 实现细节

### Review Pipeline

```python
class PRReviewAgent:
    def __init__(self, github_client, llm_client):
        self.github = github_client
        self.llm = llm_client

    async def review_pr(self, repo: str, pr_number: int):
        # 1. 获取 PR 信息
        pr = await self.github.get_pr(repo, pr_number)
        diff = await self.github.get_diff(repo, pr_number)
        files = await self.github.get_files(repo, pr_number)

        # 2. 过滤：只 Review 代码文件
        code_files = [f for f in files if f.endswith(('.py', '.js', '.ts', '.go'))]
        if not code_files:
            return "无可 Review 的代码文件"

        # 3. 分段 Review（避免超长 diff）
        reviews = []
        for file in code_files:
            file_diff = extract_file_diff(diff, file)
            if len(file_diff) > 10000:  # 大文件分段
                segments = split_diff(file_diff, max_size=8000)
                for seg in segments:
                    review = await self.review_segment(seg, file, pr.description)
                    reviews.append(review)
            else:
                review = await self.review_segment(file_diff, file, pr.description)
                reviews.append(review)

        # 4. 汇总 + 去重
        final_review = self.merge_reviews(reviews)

        # 5. 提交 Review
        await self.github.create_review(
            repo, pr_number,
            body=final_review.summary,
            comments=final_review.inline_comments
        )
```

### Review Prompt

```python
REVIEW_PROMPT = """你是一个严格的 Code Reviewer。审查以下代码变更。

PR 描述：{pr_description}
文件：{file_path}
变更：
```diff
{diff}
```

检查维度：
1. **Bug 风险**：逻辑错误、边界情况、空指针、竞态条件
2. **安全问题**：注入、敏感信息泄露、权限问题
3. **性能问题**：不必要的循环、N+1 查询、内存泄漏
4. **可维护性**：命名、复杂度、重复代码
5. **测试**：是否需要补充测试

输出 JSON：
{
    "severity": "high/medium/low",
    "category": "bug/security/performance/maintainability/test",
    "line": 行号,
    "comment": "具体问题描述和建议修改",
    "suggestion": "建议的修改代码（可选）"
}

重要：
- 只报告真正的问题，不要为了找问题而找问题
- 每个问题必须给出具体的修改建议
- 区分"必须修改"和"建议改进"
- 不要评论代码风格（由 Ruff/Prettier 处理）"""
```

### 规则 + LLM 混合策略

```python
# 规则型检查（快、准、便宜）
rule_checks = [
    run_ruff(file),       # Python 风格
    run_semgrep(file),    # 安全漏洞
    check_todo_count(file),  # TODO 数量
    check_test_coverage(file),  # 测试覆盖
]

# LLM 检查（慢、但理解语义）
llm_checks = [
    review_bug_risk(diff),
    review_security(diff),
    review_performance(diff),
    review_logic_correctness(diff),
]

# 合并：规则检查优先，LLM 补充规则无法检测的语义问题
```

## 结果

| 指标 | 纯人工 | Agent + 人工 | 变化 |
|------|--------|-------------|------|
| Review 时间/PR | 45 分钟 | 20 分钟 | -56% |
| 首次 Review 到合并 | 1.5 天 | 0.8 天 | -47% |
| 多轮修改率 | 30% | 18% | -40% |
| Bug 漏检率 | 15% | 8% | -47% |
| Senior 每日 Review 时间 | 2.5 小时 | 1 小时 | -60% |

### Agent Review 质量

| 问题类型 | 检出率 | 误报率 |
|---------|--------|--------|
| Bug 风险 | 72% | 25% |
| 安全漏洞 | 85% | 15% |
| 性能问题 | 60% | 30% |
| 可维护性 | 65% | 35% |
| 测试缺失 | 78% | 20% |

## 踩过的坑

### 坑 1：误报过多

**问题**：初期 Agent 对每个 PR 都提出 5-10 个问题，大部分是误报，Reviewers 开始忽略 Agent 评论。

**原因**：Prompt 太宽泛，"宁可错杀不可放过"的策略适得其反。

**解法**：
- 调整 Prompt："只报告高置信度问题"
- 分级标注：`[必须修改]` vs `[建议改进]`
- 规则型检查不经过 LLM，减少误报
- 追踪误报率，持续优化 Prompt

### 坑 2：大文件超上下文

**问题**：单个文件 diff 超过 10K tokens，Agent 无法完整理解。

**解法**：大文件按函数/类分段 Review，每段独立分析。对超长文件只 Review 变更部分及其上下文。

### 坑 3：不理解业务逻辑

**问题**：Agent 无法判断代码是否符合业务需求，只能做语法和模式层面的检查。

**解法**：明确 Agent 的定位——做"代码质量检查"而非"业务逻辑审查"。业务逻辑仍需人工 Review。在 Review 末尾标注"此 Review 不涵盖业务逻辑正确性"。

### 坑 4：开发者抵触

**问题**：部分开发者觉得 Agent Review 是"机器指手画脚"，产生抵触情绪。

**解法**：
- Agent 以"建议"而非"要求"的语气
- Agent 评论用开发者友好的风格
- 追踪 Agent 对开发者代码质量的改善效果，用数据说服

## 经验教训

1. **规则 + LLM 混合 > 纯 LLM**：规则检查快且准，LLM 补充语义理解
2. **减少误报比提高召回更重要**：误报过多会导致信任崩塌
3. **Agent 定位要明确**：做代码质量检查，不做业务逻辑审查
4. **人工仍然必需**：Agent 是辅助而非替代
5. **语气和呈现方式影响接受度**：友好的评论风格让开发者更愿意接受

## 成本分析

| 项目 | 月成本 |
|------|--------|
| LLM API (GPT-4o) | ¥4,500 |
| GitHub Actions | ¥800 |
| Semgrep | ¥1,200 |
| **总计** | **¥6,500** |
| 节省 Senior 时间 | ¥60,000/月 |
| **ROI** | **9.2x** |
