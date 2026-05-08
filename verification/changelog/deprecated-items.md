---
title: 废弃项目记录
category: changelog
tags: [废弃, 兼容性, 迁移]
created: 2026-05-08
updated: 2026-05-08
---

# 废弃项目记录

> 记录已废弃的 API、模型、功能和文档内容，提供迁移指引。

---

## API 废弃

| 项目 | 废弃日期 | 替代方案 | 影响文档 | 状态 |
|------|---------|---------|---------|------|
| OpenAI Completions API | 2026-03-01 | Chat Completions API | docs/platforms/openai-api-guide.md | 已迁移 |
| OpenAI `/v1/engines` 端点 | 2026-01-15 | `/v1/models` | docs/platforms/openai-api-guide.md | 已迁移 |
| Anthropic `count_tokens` 旧端点 | 2026-02-01 | `messages/count_tokens` | docs/platforms/anthropic-claude-guide.md | 已迁移 |
| Google Gemini `generateMessage` | 2025-12-01 | `generateContent` | docs/platforms/google-gemini-guide.md | 已迁移 |

## 模型废弃

| 模型 | 废弃日期 | 替代模型 | 说明 | 状态 |
|------|---------|---------|------|------|
| GPT-3.5-turbo | 2026-04-01 | GPT-4o-mini | 性能更好、价格更低 | 已下线 |
| GPT-4 (非 turbo) | 2026-03-01 | GPT-4o | 速度更快、成本更低 | 已下线 |
| Claude 3 Haiku | 2026-02-01 | Claude 4 Haiku | 新一代模型 | 已下线 |
| Claude 3 Opus | 2026-04-15 | Claude 4 Opus | 新一代模型 | 已下线 |
| text-embedding-ada-002 | 2026-05-01 | text-embedding-3-small | 更高效、更便宜 | 过渡中 |

## 功能废弃

| 功能 | 废弃日期 | 替代方案 | 说明 | 状态 |
|------|---------|---------|------|------|
| OpenAI `functions` 参数 | 2026-01-01 | `tools` 参数 | 更灵活的工具调用格式 | 已迁移 |
| Anthropic `tool_choice` 旧格式 | 2026-02-15 | 新 `tool_choice` 格式 | 支持更多控制选项 | 已迁移 |
| OpenAI `logprobs` (Completions) | 2026-03-01 | Chat Completions `logprobs` | 仅 Chat 版本可用 | 已迁移 |

## 文档内容废弃

| 文档 | 废弃内容 | 替代内容 | 操作 | 状态 |
|------|---------|---------|------|------|
| openai-api-guide.md | GPT-3.5-turbo 示例代码 | GPT-4o-mini 示例代码 | 更新代码块 | 待更新 |
| openai-api-guide.md | Completions API 用法 | Chat Completions / Responses API | 重写章节 | 待更新 |
| anthropic-claude-guide.md | Claude 3 系列说明 | Claude 4 系列 | 更新模型列表 | 待更新 |

## 迁移指引

### GPT-3.5-turbo → GPT-4o-mini

```python
# 旧代码
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[...]
)

# 新代码
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[...]
)
```

**说明**：GPT-4o-mini 在性能上超越 GPT-3.5-turbo，且价格更低。无需修改其他参数。

### Completions API → Chat Completions API

```python
# 旧代码（已废弃）
response = client.completions.create(
    model="gpt-3.5-turbo-instruct",
    prompt="Translate: "
)

# 新代码
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a translator."},
        {"role": "user", "content": "Translate: "}
    ]
)
```

### `functions` → `tools` 参数

```python
# 旧代码（已废弃）
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[...],
    functions=[{"name": "get_weather", "parameters": {...}}]
)

# 新代码
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[...],
    tools=[{"type": "function", "function": {"name": "get_weather", "parameters": {...}}}]
)
```

---

*维护者：项目验真团队 | 最后更新：2026-05-08*
