---
title: OpenAI API 指南验真报告
verified_doc: docs/platforms/openai-api-guide.md
verified_date: 2026-05-07
verified_by: AI 自动验真
model_version: GPT-4o / Claude 4 Sonnet
rating: B
next_verification: 2026-06-07
---

# OpenAI API 指南验真报告

## 验真摘要

对 `docs/platforms/openai-api-guide.md` 的内容进行验证，重点关注注册流程、API 兼容性、定价信息和模型可用性。

## 验真内容

### 1. 注册与 API 密钥申请 ✅

- 流程描述准确：访问 platform.openai.com → 注册 → API keys → 创建密钥
- 需要手机验证：✅ 正确
- 免费额度：注册时赠送 $5 额度 — ✅ 确认有效（~2026.05）
- ⚠️ 注意事项：免费额度有有效期（通常 3 个月），文档未明确说明

### 2. Python SDK 示例 ✅

- `pip install openai` — 安装命令正确，最新 SDK >= 1.0
- 客户端初始化示例 — 使用 `OpenAI(api_key="...")` 方式，与当前 SDK API 一致
- ⚠️ 建议补充环境变量方式：`client = OpenAI()`（自动读取 `OPENAI_API_KEY`）

### 3. 定价参考 ⚠️ 部分一致

- GPT-4o 价格：$2.50 / $10.00（输入/输出每百万 token） — ✅ 基本一致
- GPT-4o mini 价格：$0.15 / $0.60 — ✅ 基本一致
- ⚠️ 文档未列出 o3 和 o4-mini 系列的价格，建议补充

### 4. 模型信息 ⚠️ 需更新

- 文档中的模型列表基本准确
- ⚠️ o3 系列：文档提到了 o3，但缺少 o3-mini-high 等变体
- ⚠️ 推理模型（o-series）的计费方式不同（按输出 token 计费 + 额外思考 token），文档未体现

### 5. 限流信息 ✅

- 免费层 Rate Limit（~3 RPM / 200,000 TPM）— ✅ 基本准确
- Tier 1-5 分级限流 — 描述正确

### 6. 可用性信息 ✅

- 中国区直接访问受限 — ✅ 准确
- 需要通过海外服务器中转 — ✅ 准确

## 验真结论

**评级：B**（大部分信息准确，但定价和模型信息需定期更新）

### 待改进项
1. 补充 o3/o4-mini 系列的定价和模型信息
2. 明确免费额度的有效期限制
3. 建议增加环境变量配置示例
4. 推理模型计费方式的说明
