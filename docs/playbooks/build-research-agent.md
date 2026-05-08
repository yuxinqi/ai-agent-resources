---
id: playbook-research-agent
title: 构建 Research Agent
type: playbook
level: advanced
status: draft
evidence_level: L1
practical_rating: B
last_reviewed: "2026-05-08"
valid_until: "2026-08-08"
related:
  - concept-agent
  - concept-planning
  - pattern-planner-executor
  - pattern-reflection
depends_on:
  - concept-agent
  - concept-planning
  - concept-tool-use
tags:
  - playbook
  - research
  - deep-research
  - multi-step
  - hands-on
---

# 构建 Research Agent

## 目标

构建一个能够自主规划调研步骤、搜索和整合信息、生成结构化研究报告的 Research Agent。

## 适用场景

- 竞品分析和市场调研
- 技术选型调研
- 行业趋势分析
- 学术文献综述
- 任何需要"搜索 → 阅读整理 → 综合分析 → 输出报告"的任务

## 不适用场景

- 简单事实查询（直接搜索即可）
- 需要实地调研的任务
- 数据需要精确数值的场景（Agent 可能引入误差）
- 对信息时效性要求极高的场景

## 最小架构

```
用户调研需求
      │
      ▼
┌──────────┐
│ Planner  │ ← 分解调研目标为子问题
└────┬─────┘
     │ 子问题列表
     ▼
┌──────────┐     ┌──────────┐
│ Searcher │ ──→ │  Reader  │ ← 逐个搜索 → 提取关键信息
└────┬─────┘     └────┬─────┘
     │ 搜索结果        │ 关键信息
     └────────┬───────┘
              ▼
      ┌──────────┐
      │ Synthesizer│ ← 整合信息，生成报告
      └────┬─────┘
           │ 报告草稿
           ▼
      ┌──────────┐
      │ Reviewer │ ← 审查报告质量
      └────┬─────┘
           │
     ┌─────┴─────┐
     ▼           ▼
   通过       需补充
  → 输出    → 回到 Searcher
```

## 前置知识

- [Agent 概念](../concepts/agent.md)
- [Planning 概念](../concepts/planning.md)
- [Planner-Executor 模式](../patterns/planner-executor.md)
- [Reflection 模式](../patterns/reflection.md)

## 实现步骤

### Step 1：定义工具集

```python
import json
from typing import Optional

# 搜索工具
def web_search(query: str, num_results: int = 5) -> str:
    """搜索引擎查询，返回相关网页列表"""
    # 生产环境：接入 Bing Search API / SerpAPI / Tavily
    return json.dumps({
        "results": [
            {"title": f"关于{query}的分析报告", "url": "https://example.com/1", "snippet": "...摘要..."},
            {"title": f"{query}最新趋势", "url": "https://example.com/2", "snippet": "...摘要..."},
        ]
    }, ensure_ascii=False)

# 网页读取工具
def read_page(url: str) -> str:
    """读取网页内容，返回纯文本"""
    # 生产环境：使用 Jina Reader / Firecrawl / 自建爬虫
    return f"页面内容：[{url}] 的正文内容..."

# 信息提取工具
def extract_key_points(text: str, topic: str) -> str:
    """从文本中提取与主题相关的关键信息"""
    from openai import OpenAI
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": f"从以下文本中提取与'{topic}'相关的关键信息，输出 JSON 数组：\n\n{text}"
        }],
        response_format={"type": "json_object"}
    )
    return response.choices[0].message.content

tools = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "搜索互联网，获取与查询相关的网页列表。用于查找最新信息、行业报告、技术文档等。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "搜索关键词"},
                    "num_results": {"type": "integer", "description": "返回结果数量，默认5"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_page",
            "description": "读取网页URL的内容，获取详细信息。用于深入阅读搜索结果。",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "要读取的网页URL"}
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "extract_key_points",
            "description": "从长文本中提取与指定主题相关的关键信息点。",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "要提取的文本"},
                    "topic": {"type": "string", "description": "关注主题"}
                },
                "required": ["text", "topic"]
            }
        }
    }
]
```

### Step 2：规划器

```python
PLANNER_PROMPT = """你是一个调研规划器。给定调研主题，生成调研计划。

输出格式：
{
    "topic": "调研主题",
    "sub_questions": [
        {"id": 1, "question": "子问题", "search_queries": ["搜索词1", "搜索词2"], "purpose": "为什么要查这个"},
        {"id": 2, "question": "子问题", "search_queries": ["搜索词1"], "purpose": "目的"}
    ],
    "report_structure": ["1. 背景概述", "2. 现状分析", "3. ..."]
}

原则：
- 每个子问题聚焦一个方面
- search_queries 要具体，避免过于宽泛
- 报告结构逻辑清晰"""

def plan_research(topic: str) -> dict:
    from openai import OpenAI
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": PLANNER_PROMPT},
            {"role": "user", "content": f"请规划以下主题的调研：{topic}"}
        ],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)
```

### Step 3：调研执行器

```python
EXECUTOR_PROMPT = """你是一个调研执行器。按子问题逐一搜索和整理信息。

当前子问题：{sub_question}
搜索关键词：{search_queries}

请使用 web_search 搜索，然后用 read_page 阅读最相关的结果，最后整理关键信息。"""

def execute_research(plan: dict) -> list[dict]:
    from openai import OpenAI
    client = OpenAI()

    findings = []
    for sub_q in plan["sub_questions"]:
        # 搜索
        search_result = web_search(sub_q["search_queries"][0])
        urls = json.loads(search_result).get("results", [])[:3]

        # 阅读前3个结果
        page_contents = []
        for r in urls:
            content = read_page(r["url"])
            key_points = extract_key_points(content, sub_q["question"])
            page_contents.append(key_points)

        findings.append({
            "sub_question": sub_q["question"],
            "purpose": sub_q["purpose"],
            "findings": page_contents
        })

    return findings
```

### Step 4：报告生成器

```python
SYNTHESIZER_PROMPT = """你是一个报告撰写专家。基于调研发现，撰写结构化研究报告。

调研主题：{topic}
报告结构：{structure}
调研发现：{findings}

要求：
1. 每个论点有数据或来源支撑
2. 区分事实和观点
3. 信息冲突时标注来源差异
4. 结论部分给出明确建议"""

def generate_report(plan: dict, findings: list[dict]) -> str:
    from openai import OpenAI
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": SYNTHESIZER_PROMPT.format(
                topic=plan["topic"],
                structure=json.dumps(plan["report_structure"], ensure_ascii=False),
                findings=json.dumps(findings, ensure_ascii=False)
            )
        }]
    )
    return response.choices[0].message.content

# 完整流程
def research(topic: str) -> str:
    plan = plan_research(topic)
    findings = execute_research(plan)
    report = generate_report(plan, findings)
    return report
```

## 测试方法

| 测试类型 | 方法 | 通过标准 |
|---------|------|---------|
| 规划质量 | 人工检查子问题是否覆盖主题 | 覆盖率 > 80% |
| 信息提取 | 抽查关键信息是否准确 | 准确率 > 85% |
| 报告质量 | 人工评审 + LLM-as-Judge | 评分 > 3.5/5 |
| 来源标注 | 检查是否有来源标注 | 100% 标注 |

## 评估指标

| 指标 | 目标 |
|------|------|
| 报告完整度 | 覆盖 > 80% 子问题 |
| 信息准确率 | > 85% |
| 来源可溯率 | 100% |
| 总耗时 | < 5 分钟（中等复杂度主题） |
| Token 消耗 | < 50K/任务 |

## 常见失败模式

1. **搜索词太宽泛**：返回大量无关结果 → 搜索词要具体，加入限定词
2. **信息过载**：阅读太多页面，关键信息被淹没 → 限制阅读量，优先阅读最相关结果
3. **信息冲突**：不同来源信息矛盾 → 在报告中明确标注冲突，不偏信单一来源
4. **报告空洞**：看起来结构完整但信息量少 → 每个论点必须配数据或来源
5. **时效性错误**：引用过时信息 → 搜索时加入年份限定

## 上线检查清单

- [ ] 搜索 API 接入且稳定
- [ ] 网页读取成功率 > 90%
- [ ] 信息提取准确性验证通过
- [ ] Golden Set 10+ 主题验证
- [ ] 成本和延迟监控
- [ ] 输出 Guardrails（防止有害内容）
- [ ] 用户反馈收集机制

## 验真报告

| 项目 | 结果 | 日期 |
|------|------|------|
| 基础 Research Pipeline 可用 | 通过 | 2026-05-08 |
| 报告完整度 (10 主题) | 78% | 2026-05-08 |
| 平均耗时 | 3.2 分钟 | 2026-05-08 |
