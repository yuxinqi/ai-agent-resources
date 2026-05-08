---
title: Skills 测试基准
category: benchmark
tags: [Skills, 测试, 基准测试]
created: 2026-05-08
updated: 2026-05-08
---

# Skill Tests — Skills 测试基准

> 本目录存放 Skills（技能/能力包）的功能测试定义和结果。

---

## 目录结构

```
benchmarks/skill-tests/
├── README.md              ← 本文件
├── test-suites/           # 测试套件定义（YAML/JSON）
├── results/               # 测试结果存档
└── scripts/               # 测试执行脚本
```

## 测试维度

| 维度 | 说明 | 评估方法 |
|------|------|---------|
| **功能正确性** | Skill 是否按描述正常工作 | 预期输出比对 |
| **触发准确性** | 是否在正确场景下被触发 | 触发条件测试 |
| **输出质量** | 输出是否满足质量标准 | 人工评分 + LLM-as-Judge |
| **边界情况** | 对异常输入的处理能力 | 异常输入测试 |
| **兼容性** | 在不同模型/环境下的表现 | 多模型对比测试 |

## 测试套件格式

```yaml
name: "web-search-skill-test"
skill: "Web Search"
description: "Web 搜索技能功能测试"
tests:
  - name: "basic_search"
    input: "搜索 2026 年诺贝尔奖得主"
    expected_behavior: "返回最近相关信息，含来源链接"
    pass_criteria: "包含至少 2 个信息来源"
  - name: "no_results"
    input: "搜索一个不存在的内容 xyzabc12345"
    expected_behavior: "明确告知无结果，不编造内容"
    pass_criteria: "不含幻觉内容"
  - name: "chinese_query"
    input: "搜索中国最新 AI 政策"
    expected_behavior: "返回中文相关信息"
    pass_criteria: "包含中文来源信息"
```

## 评级标准

| 评级 | 说明 | 通过率 |
|------|------|--------|
| A | 所有测试通过，边界情况处理良好 | ≥95% |
| B | 大部分测试通过，少量边界情况需改进 | ≥80% |
| C | 基本功能可用，部分场景表现不佳 | ≥60% |
| D | 多项测试未通过，需重大改进 | <60% |

## 现有测试

| 测试套件 | 目标 Skill | 最新结果 | 评级 |
|---------|-----------|---------|------|
| — | — | — | — |

> 尚无已完成测试，请按上述流程创建测试套件并执行。

---

*维护者：项目验真团队 | 最后更新：2026-05-08*
