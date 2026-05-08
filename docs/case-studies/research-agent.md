---
id: case-research
title: 调研 Agent 案例
type: case-study
level: advanced
status: draft
evidence_level: L2
practical_rating: B
last_reviewed: "2026-05-08"
valid_until: "2026-08-08"
related:
  - concept-planning
  - pattern-planner-executor
  - pattern-reflection
  - playbook-research-agent
depends_on:
  - concept-agent
  - concept-planning
tags:
  - case-study
  - research
  - deep-research
  - production
---

# 调研 Agent 案例

## 背景

某咨询公司需要定期为客户产出行业调研报告，每个报告需要 2-3 名分析师工作 1-2 周。目标：用 Research Agent 将初稿产出时间从 5 天缩短到 1 天，分析师只做审校和深度分析。

## 系统架构

```
调研需求
    │
    ▼
Planner（规划器）
    │ 生成子问题列表
    ▼
┌──────────────────────────┐
│     并行 Searcher        │ ← 每个子问题一个搜索任务
│  ┌─────┐ ┌─────┐ ┌────┐ │
│  │ S-1 │ │ S-2 │ │S-3 │ │
│  └──┬──┘ └──┬──┘ └─┬──┘ │
└─────┼───────┼───────┼────┘
      │       │       │
      ▼       ▼       ▼
   关键信息提取和去重
      │
      ▼
Synthesizer（综合器）
      │ 生成结构化报告
      ▼
Reviewer（审校器）
      │ 检查完整性、准确性
      ▼
   输出报告（带来源标注）
```

## 技术选型

| 组件 | 选择 | 理由 |
|------|------|------|
| 规划模型 | GPT-4o | 规划需要强推理 |
| 执行模型 | GPT-4o-mini | 搜索和提取用小模型足够 |
| 综合模型 | GPT-4o | 报告撰写需要强生成能力 |
| 搜索 | Tavily API | 专为 AI Agent 设计的搜索 |
| 网页读取 | Jina Reader | 高质量网页转文本 |
| 框架 | LangGraph | 并行执行 + 状态管理 |

## 实现细节

### 规划阶段

```python
PLANNER_PROMPT = """你是一个调研规划专家。根据调研主题，制定调研计划。

要求：
1. 分解为 5-8 个子问题，每个子问题聚焦一个方面
2. 每个子问题提供 2-3 个搜索关键词
3. 规划报告结构（包含数据表格、趋势分析、竞品对比等）
4. 标注哪些信息是必须获取的，哪些是加分项"""

# 输出 JSON 格式的计划
```

### 搜索和提取阶段

```python
# 并行搜索
async def search_sub_question(sub_q: dict) -> dict:
    results = await tavily_search(sub_q["search_queries"][0])
    key_points = []
    for result in results[:3]:
        content = await jina_read(result["url"])
        points = await extract_points(content, sub_q["question"])
        key_points.append({
            "source": result["url"],
            "title": result["title"],
            "points": points
        })
    return {"sub_question": sub_q["question"], "findings": key_points}

# 并行执行所有子问题
tasks = [search_sub_question(sq) for sq in plan["sub_questions"]]
findings = await asyncio.gather(*tasks)
```

### 报告生成阶段

```python
SYNTHESIZER_PROMPT = """你是一个资深行业分析师。基于调研数据撰写专业报告。

要求：
1. 每个论点必须有数据或来源支撑
2. 信息冲突时标注"来源差异"
3. 数据用表格呈现
4. 给出明确的结论和建议
5. 末尾附完整参考来源"""

# 输出 Markdown 格式报告
```

## 结果

| 指标 | 人工 | Agent 辅助 | 变化 |
|------|------|-----------|------|
| 初稿时间 | 5 天 | 4 小时 | -97% |
| 全流程时间 | 10 天 | 3 天 | -70% |
| 信息来源数 | 15-20 | 30-50 | +100% |
| 报告字数 | 5000-8000 | 6000-10000 | +25% |
| 分析师满意度 | N/A | 3.8/5 | - |

## 踩过的坑

### 坑 1：搜索结果同质化

**问题**：多个子问题搜到的信息高度重复。

**解法**：增加去重步骤——对搜索结果做语义去重，相似度 > 0.85 的合并。搜索关键词从不同角度切入同一主题。

### 坑 2：信息过时

**问题**：搜索到 3 年前的旧数据当作最新信息使用。

**解法**：搜索时加入年份限定，Reranker 优先排序近期内容，报告中标明数据时间。

### 坑 3：报告空洞

**问题**：报告结构完整但信息量少，像模板填空。

**原因**：Synthesizer 没有充分利用搜索数据，倾向于生成通用表述。

**解法**：在 Prompt 中要求"每个段落至少引用一个具体数据点"，Review 阶段检查数据密度。

### 坑 4：来源不可溯

**问题**：报告中提到的数据找不到对应来源。

**解法**：强制每个数据点标注 [来源: URL]，Reviewer 检查所有标注是否可验证。

## 经验教训

1. **规划比搜索重要**：好的规划（子问题分解）决定了报告质量的上限
2. **搜索要广、提取要精**：多搜索但只提取与主题高度相关的信息
3. **并行执行节省 70% 时间**：子问题独立时一定要并行
4. **人工审校不可省**：Agent 的报告总有事实性错误需要修正
5. **来源标注是刚需**：客户需要验证信息来源

## 成本分析

| 项目 | 单次成本 |
|------|---------|
| LLM API (规划 + 综合) | ¥15 |
| LLM API (搜索 + 提取) | ¥8 |
| 搜索 API (Tavily) | ¥3 |
| 网页读取 (Jina) | ¥2 |
| **总计** | **¥28** |
| 人工成本 (传统方式) | ¥5,000 |
| **节省** | **¥4,972/次** |
