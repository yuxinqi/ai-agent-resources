---
id: tool-deployment
title: Agent 部署工具
type: tool
level: intermediate
status: draft
evidence_level: L0
practical_rating: C
last_reviewed: 2026-05-08
valid_until: 2026-08-08
related:
  - playbook-production
depends_on:
  - concept-agent
tags:
  - agent
  - deployment
  - production
  - devops
---

# Agent 部署工具

## 一句话定位

将 Agent 从开发环境推向生产环境所需的部署和运维工具。

## 适合场景

- Agent 需要面向真实用户提供服务
- 需要 7×24 稳定运行
- 需要弹性扩缩容
- 需要灰度发布和回滚能力

## 不适合场景

- 内部工具、Demo 或原型
- 使用量极小的场景

## 部署方案对比

### Serverless（推荐起步方案）

| 平台 | 特点 | 适合 |
|------|------|------|
| AWS Lambda | 事件驱动、按调用付费 | 低频、短时任务 |
| Vercel | 前端友好、Edge 函数 | Web Agent |
| Cloudflare Workers | 超低延迟、全球分布 | 对延迟敏感的 Agent |

### 容器化部署

| 方案 | 特点 | 适合 |
|------|------|------|
| Docker + K8s | 标准化、弹性伸缩 | 中大规模生产系统 |
| Docker Compose | 简单、单机部署 | 小团队、开发测试 |

### Agent 专用平台

| 平台 | 特点 | 适合 |
|------|------|------|
| LangServe | LangChain 官方部署方案 | LangChain 项目 |
| Streamlit | 快速构建 Web 界面 | 内部工具、Demo |
| Gradio | ML 模型展示 | 交互式 Agent Demo |

## 关键考虑

| 因素 | 说明 |
|------|------|
| 冷启动 | Serverless 冷启动可能影响首次响应时间 |
| 超时 | LLM 调用可能超过平台超时限制 |
| 并发 | 需要考虑 API 限流和并发控制 |
| 成本 | 长时间运行的 Agent 成本可能很高 |
| 安全 | API Key 管理、输入验证、输出过滤 |

## 生产检查清单

1. [ ] 健康检查端点
2. [ ] 优雅关闭处理
3. [ ] 请求超时和重试机制
4. [ ] API Key 安全存储
5. [ ] 输入长度限制
6. [ ] 输出内容过滤
7. [ ] 速率限制
8. [ ] 错误日志和监控
9. [ ] 灰度发布方案
10. [ ] 回滚方案

## 验真结论

- 证据等级：L0
- 推荐等级：C（部署方案依赖具体业务需求，需要自行评估）
- 有效期至：2026-08-08
