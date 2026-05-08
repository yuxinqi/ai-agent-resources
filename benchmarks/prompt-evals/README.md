---
title: 提示词评估基准
category: benchmark
tags: [提示词, 评估, 基准测试]
created: 2026-05-08
updated: 2026-05-08
---

# Prompt Evals — 提示词评估基准

> 本目录存放提示词评估（Prompt Evaluation）相关的基准测试定义、测试数据和结果。

---

## 目录结构

```
benchmarks/prompt-evals/
├── README.md              ← 本文件
├── test-cases/            # 测试用例定义（YAML/JSON）
├── results/               # 评估结果存档
└── scripts/               # 评估脚本
```

## 评估维度

| 维度 | 说明 | 评估方法 |
|------|------|---------|
| **指令遵循** | 是否严格遵循提示词中的指令和格式要求 | 格式匹配 + 人工评分 |
| **输出质量** | 输出内容的准确性、完整性和一致性 | 人工评分 + LLM-as-Judge |
| **鲁棒性** | 对输入扰动的稳定性 | 同义改写测试 |
| **安全性** | 是否产生有害或不适当内容 | 安全检测 + 人工审核 |
| **效率** | Token 使用效率和延迟 | 自动统计 |

## 评估流程

1. **定义测试用例**：在 `test-cases/` 中创建 YAML 文件，描述输入、预期输出和评分标准
2. **执行评估**：运行评估脚本，对目标提示词进行批量测试
3. **收集结果**：结果保存在 `results/` 目录，含各维度评分
4. **分析报告**：生成评估报告，标注评级（A/B/C/D）

## 测试用例格式

```yaml
name: "system-prompt-format-compliance"
description: "测试 System Prompt 格式遵循能力"
model: "gpt-4o"
test_cases:
  - input: "请用 JSON 格式列出 5 个编程语言"
    expected_format: "JSON array"
    scoring:
      format_compliance: 1.0  # 格式权重
      content_accuracy: 0.5   # 内容权重
      completeness: 0.3       # 完整性权重
  - input: "以 Markdown 表格形式对比 3 个数据库"
    expected_format: "Markdown table"
    scoring:
      format_compliance: 1.0
      content_accuracy: 0.5
      completeness: 0.3
```

## 评级标准

| 评级 | 说明 | 通过率 |
|------|------|--------|
| A | 优秀，所有测试用例通过 | ≥90% |
| B | 良好，大部分测试用例通过 | ≥70% |
| C | 一般，部分测试用例通过 | ≥50% |
| D | 较差，多数测试用例未通过 | <50% |

## 现有评估

| 评估名称 | 目标提示词 | 最新结果 | 评级 |
|---------|----------|---------|------|
| — | — | — | — |

> 尚无已完成评估，请按上述流程创建测试用例并执行。

---

*维护者：项目验真团队 | 最后更新：2026-05-08*
