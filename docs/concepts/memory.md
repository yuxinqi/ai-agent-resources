---
id: concept-memory
title: Memory（记忆）
type: concept
level: intermediate
status: draft
evidence_level: L2
practical_rating: B
last_reviewed: "2026-05-08"
valid_until: "2026-08-08"
related:
  - concept-agent
  - concept-rag
  - concept-planning
depends_on:
  - concept-agent
tags:
  - memory
  - context-management
  - core-concept
---

# Memory（记忆）

## 一句话解释

Memory 是 Agent 在多轮对话和多次执行中存储、检索和利用信息的能力，解决 LLM 无状态和上下文窗口有限的核心限制。

## 它解决什么问题

LLM 是无状态的——每次调用都是全新的，没有"记忆"。但真实的 Agent 任务需要：

- **对话连续性**：记住用户之前说了什么，避免重复询问
- **跨会话持久化**：记住用户偏好、历史交互，提供个性化服务
- **任务状态维护**：在多步执行中跟踪已完成和待完成的步骤
- **知识积累**：从历史交互中学习和改进

上下文窗口有限（即使 128K 也有上限），不可能把所有历史信息都塞进去。Memory 的核心挑战是：**在有限的上下文空间中，选择最相关的信息呈现给 LLM**。

## 什么时候应该使用

- 对话超过 5 轮，需要引用早期信息
- Agent 需要跨会话保持用户偏好或知识
- 多步任务需要跟踪中间状态
- 用户有个性化需求，Agent 需要记住用户特征

## 什么时候不应该使用

- 单轮问答，无需保持上下文
- 任务完全无状态，每次调用独立
- Memory 检索的延迟不可接受
- 存储敏感信息且缺乏安全措施

## 最小实践示例

### Short-term Memory（对话历史管理）

```python
from collections import deque

class ConversationMemory:
    def __init__(self, max_messages: int = 20):
        self.messages = deque(maxlen=max_messages)

    def add(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    def get_context(self) -> list:
        return list(self.messages)

    def summarize_if_needed(self, summarizer_fn) -> list:
        """当消息超过阈值时，将早期消息摘要压缩"""
        if len(self.messages) > 15:
            old_messages = [self.messages.popleft() for _ in range(5)]
            summary = summarizer_fn(old_messages)
            self.messages.appendleft({
                "role": "system",
                "content": f"[历史对话摘要] {summary}"
            })
        return list(self.messages)
```

### Long-term Memory（持久化存储）

```python
import json
from pathlib import Path

class PersistentMemory:
    def __init__(self, storage_path: str = "memory.json"):
        self.path = Path(storage_path)
        self.data = json.loads(self.path.read_text()) if self.path.exists() else {}

    def save(self, key: str, value: str):
        self.data[key] = value
        self.path.write_text(json.dumps(self.data, ensure_ascii=False, indent=2))

    def retrieve(self, key: str) -> str | None:
        return self.data.get(key)

    def search(self, query: str) -> list[str]:
        """简单关键词搜索（生产环境应用向量检索）"""
        return [v for k, v in self.data.items() if query.lower() in v.lower()]

# 使用：记住用户偏好
memory = PersistentMemory()
memory.save("user_preference_language", "中文")
memory.save("user_weather_last_city", "北京")
```

## 常见失败模式

1. **上下文窗口溢出**：历史消息过多，超出 Token 限制，导致 API 报错或信息截断。解法：滑动窗口 + 摘要压缩。

2. **摘要信息丢失**：压缩历史时丢失关键细节。解法：保留最近 N 轮完整消息，只对更早的消息做摘要。

3. **检索相关性差**：从长期记忆中检索到的信息与当前问题不相关。解法：使用向量检索替代关键词搜索，加入 Reranker。

4. **记忆冲突**：新旧信息矛盾（如用户改了偏好），旧记忆未更新。解法：实现记忆更新和淘汰策略，设置 TTL。

5. **隐私泄露**：将敏感信息（密码、API Key）存入 Memory 并在后续对话中暴露。解法：敏感信息过滤，Memory 存储加密。

## 评估方法

| 维度 | 指标 | 方法 |
|------|------|------|
| 召回率 | 记忆命中率 | 需要历史信息时是否成功检索到 |
| 准确率 | 检索相关性 | 检索到的信息是否与当前任务相关 |
| 压缩率 | Token 节省比例 | 摘要后的 Token 数 / 原始 Token 数 |
| 延迟 | 检索延迟 | P95 < 200ms |
| 一致性 | 记忆一致性 | 新旧信息是否矛盾 |

## 相关概念

- [Agent](agent.md) — Memory 是 Agent 的核心组件
- [RAG](rag.md) — RAG 是一种特殊的 Memory 实现方式
- [Planning](planning.md) — 规划时需要从 Memory 中检索相关信息

## 验真状态

| 结论 | 证据等级 | 来源 |
|------|---------|------|
| 滑动窗口 + 摘要是最实用的短期记忆策略 | L2 | 多框架默认实现 |
| 向量检索比关键词搜索在长期记忆中更有效 | L2 | RAG 研究验证 |
| 记忆检索延迟对 Agent 性能影响显著 | L1 | 初步实验 |
| 超过 128K 上下文时摘要压缩是必需的 | L2 | 社区实践 |

## 参考来源

- LangChain Memory Module Documentation (2024)
- MemGPT: Towards LLMs as Operating Systems (Packer et al., 2023)
- Zhong et al., "MemoryBank: Enhancing Large Language Models with Long-Term Memory" (2023)
- OpenAI, "Best Practices for Context Management" (2024)
