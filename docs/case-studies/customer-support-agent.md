---
id: case-customer-support
title: 客服 Agent 案例
type: case-study
level: intermediate
status: draft
evidence_level: L3
practical_rating: A
last_reviewed: "2026-05-08"
valid_until: "2026-08-08"
related:
  - concept-agent
  - concept-tool-use
  - pattern-router
  - pattern-guardrails
  - playbook-tool-agent
depends_on:
  - concept-agent
  - concept-tool-use
tags:
  - case-study
  - customer-support
  - production
---

# 客服 Agent 案例

## 背景

某电商平台日均客服咨询 5000+，人工客服团队 50 人，高峰期响应时间 > 5 分钟。目标：用 Agent 处理 60% 的常见咨询，人工仅处理复杂和情绪化问题。

## 系统架构

```
用户消息
    │
    ▼
意图路由（Router）
    ├── 订单查询 → Order Agent
    ├── 退款/售后 → Refund Agent
    ├── 物流查询 → Logistics Agent
    ├── 商品咨询 → Product Agent
    └── 复杂/情绪化 → 人工客服
```

## 技术选型

| 组件 | 选择 | 理由 |
|------|------|------|
| LLM | GPT-4o-mini | 成本低，中文理解好 |
| 路由 | LLM-based Router | 意图分类准确率 > 95% |
| 框架 | LangGraph | 状态管理、Human-in-the-Loop |
| 知识库 | RAG + Elasticsearch | FAQ + 商品知识 |
| 部署 | Docker + K8s | 弹性伸缩 |

## 实现细节

### 工具设计

```python
# 核心工具集
tools = [
    query_order,       # 查询订单状态
    check_logistics,   # 查询物流信息
    init_refund,       # 发起退款
    check_refund,      # 查询退款进度
    search_product,    # 搜索商品信息
    search_faq,        # 搜索常见问题
    transfer_human,    # 转人工
]
```

### Router 设计

```python
ROUTER_PROMPT = """分类用户意图。可选类别：
- order_query: 订单状态查询
- refund: 退款/售后
- logistics: 物流查询
- product: 商品咨询
- complaint: 投诉/不满（转人工）
- other: 其他（转人工）

判断规则：
- 用户表达不满或愤怒 → complaint（转人工）
- 涉及金额争议 → complaint（转人工）
- 其他按主题分类"""

# 置信度 < 0.7 时转人工
```

### Guardrails

- 输入：Prompt Injection 检测、敏感信息过滤
- 工具调用：退款金额 > 500 元需人工确认
- 输出：不承诺具体时间（如"明天一定到"）、不透露内部信息

## 结果

| 指标 | 上线前 | 上线后 | 变化 |
|------|--------|--------|------|
| 平均响应时间 | 5.2 分钟 | 0.8 分钟 | -85% |
| 自动解决率 | 0% | 62% | +62% |
| 人工客服工作量 | 5000/天 | 1900/天 | -62% |
| 用户满意度 | 3.2/5 | 4.1/5 | +28% |
| 单次服务成本 | ¥8.5 | ¥2.1 | -75% |

## 踩过的坑

### 坑 1：Agent 过度承诺

**问题**：Agent 说"您的退款 2 小时内到账"，但实际需要 1-3 天。

**原因**：System Prompt 没有明确禁止时间承诺，Agent 为了讨好用户编造了时间。

**解法**：在 System Prompt 中明确"不要承诺具体时间，只说'1-3 个工作日'"，输出 Guardrail 检查时间承诺。

### 坑 2：退款被滥用

**问题**：用户发现 Agent 可以自动退款，大量发起"不想要了"的退款请求。

**原因**：Refund Agent 审核过于宽松，没有风险判断。

**解法**：加入风险评分——同一用户 30 天内退款 > 3 次需人工审核，退款金额 > 500 元需人工确认。

### 坑 3：情绪识别不准

**问题**：用户已经很愤怒但 Agent 还在按流程走，激化矛盾。

**原因**：Router 没有有效识别情绪信号。

**解法**：增加情绪检测模型，"愤怒"和"投诉"关键词触发转人工。在 System Prompt 中加入"如果用户表达不满，先安抚再处理"。

### 坑 4：高峰期 API 限流

**问题**：大促期间 API 请求暴增，OpenAI Rate Limit 导致大量失败。

**解法**：
- 多 API Key 轮换
- 请求排队 + 优先级（已下单用户优先）
- 降级到模板回复

## 经验教训

1. **先做意图路由，再做深度处理**：Router 的准确率决定整体体验
2. **高风险操作必须 Human-in-the-Loop**：退款、赔偿等不能全自动
3. **输出 Guardrails 和输入一样重要**：防止 Agent 说不该说的话
4. **监控"转人工率"**：如果 > 40%，说明 Agent 覆盖不够
5. **持续用真实对话优化**：每周分析 100 条对话，找优化点

## 成本分析

| 项目 | 月成本 |
|------|--------|
| LLM API (GPT-4o-mini) | ¥3,200 |
| 向量数据库 (Elasticsearch) | ¥1,500 |
| 部署 (K8s, 3 副本) | ¥2,400 |
| LangSmith | ¥800 |
| **总计** | **¥7,900** |
| 节省人工成本 | ¥85,000/月 |
| **ROI** | **10.7x** |
