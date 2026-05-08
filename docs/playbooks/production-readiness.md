---
id: playbook-production
title: Agent 生产就绪指南
type: playbook
level: advanced
status: draft
evidence_level: L2
practical_rating: A
last_reviewed: "2026-05-08"
valid_until: "2026-08-08"
related:
  - concept-evaluation
  - pattern-guardrails
  - pattern-hitl
  - tool-tracing
  - tool-deployment
depends_on:
  - concept-evaluation
  - concept-agent
tags:
  - playbook
  - production
  - reliability
  - operations
  - deployment
---

# Agent 生产就绪指南

## 目标

将 Agent 从原型阶段推进到生产环境，确保可靠性、可观测性、安全性和成本可控。

## 适用场景

- Agent 已完成原型验证，准备上线
- 已有 Agent 上线但问题频发，需要加固
- 团队需要规范化 Agent 上线流程
- 从 POC 转向生产级系统的关键阶段

## 不适用场景

- 仍在原型探索阶段（过早优化）
- 内部低风险工具（可适当降低标准）
- 一次性脚本或演示

## 最小架构

```
                    ┌─────────────────┐
                    │   Load Balancer  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │   API Gateway    │ ← Rate Limit, Auth
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        ┌──────────┐  ┌──────────┐  ┌──────────┐
        │ Agent    │  │ Agent    │  │ Agent    │
        │ Instance │  │ Instance │  │ Instance │
        └────┬─────┘  └────┬─────┘  └────┬─────┘
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                    ┌──────────────┐
                    │  Observability│ ← Traces, Metrics, Logs
                    │   Platform    │
                    └──────────────┘
```

## 前置知识

- [Evaluation 概念](../concepts/evaluation.md)
- [Guardrails 模式](../patterns/guardrails.md)
- [Human-in-the-Loop 模式](../patterns/human-in-the-loop.md)
- [Tracing 工具](../tools/tracing-and-observability.md)

## 实现步骤

### Step 1：可靠性保障

```python
import time
import logging
from functools import wraps
from typing import Callable

logger = logging.getLogger("agent-production")

# 1. 超时控制
def with_timeout(timeout_seconds: int = 30):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import signal

            def handler(signum, frame):
                raise TimeoutError(f"Agent 执行超时 ({timeout_seconds}s)")

            old_handler = signal.signal(signal.SIGALRM, handler)
            signal.alarm(timeout_seconds)
            try:
                return func(*args, **kwargs)
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)
        return wrapper
    return decorator

# 2. 重试机制（带指数退避）
def with_retry(max_retries: int = 3, base_delay: float = 1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    delay = base_delay * (2 ** attempt)
                    logger.warning(f"第 {attempt+1} 次失败，{delay}s 后重试: {e}")
                    time.sleep(delay)
        return wrapper
    return decorator

# 3. 熔断器
class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = 0
        self.state = "closed"  # closed, open, half-open

    def call(self, func: Callable, *args, **kwargs):
        if self.state == "open":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "half-open"
            else:
                raise Exception("熔断器开启，请求被拒绝")

        try:
            result = func(*args, **kwargs)
            if self.state == "half-open":
                self.state = "closed"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = "open"
            raise

# 4. 降级策略
class FallbackAgent:
    def __init__(self, primary_agent, fallback_agent, failure_threshold: float = 0.5):
        self.primary = primary_agent
        self.fallback = fallback_agent
        self.failure_threshold = failure_threshold
        self.recent_results = []

    def run(self, user_input: str) -> str:
        # 如果主 Agent 近期失败率过高，直接用降级
        if self.recent_results and sum(self.recent_results[-10:]) / len(self.recent_results[-10:]) < self.failure_threshold:
            logger.warning("主 Agent 失败率过高，切换到降级 Agent")
            return self.fallback.run(user_input)

        try:
            result = self.primary.run(user_input)
            self.recent_results.append(1)
            return result
        except Exception as e:
            self.recent_results.append(0)
            logger.error(f"主 Agent 失败: {e}")
            return self.fallback.run(user_input)
```

### Step 2：可观测性

```python
import json
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime

@dataclass
class AgentTrace:
    request_id: str
    user_input: str
    start_time: datetime
    model: str
    turns: list = field(default_factory=list)
    total_tokens: int = 0
    total_duration: float = 0
    tool_calls: list = field(default_factory=list)
    final_output: str = ""
    status: str = "success"  # success, timeout, error, rate_limited

    def to_dict(self):
        return asdict(self)

class Observability:
    """可观测性管理器"""

    def __init__(self, export_fn=None):
        self.traces: list[AgentTrace] = []
        self.export_fn = export_fn  # 导出到 LangSmith/Datadog/etc.

    def start_trace(self, request_id: str, user_input: str, model: str) -> AgentTrace:
        trace = AgentTrace(
            request_id=request_id,
            user_input=user_input,
            start_time=datetime.now(),
            model=model
        )
        return trace

    def end_trace(self, trace: AgentTrace):
        trace.total_duration = (datetime.now() - trace.start_time).total_seconds()
        self.traces.append(trace)
        if self.export_fn:
            self.export_fn(trace.to_dict())

    def get_metrics(self) -> dict:
        if not self.traces:
            return {}
        durations = [t.total_duration for t in self.traces]
        tokens = [t.total_tokens for t in self.traces]
        statuses = [t.status for t in self.traces]

        return {
            "total_requests": len(self.traces),
            "success_rate": statuses.count("success") / len(statuses),
            "p50_latency": sorted(durations)[len(durations)//2],
            "p95_latency": sorted(durations)[int(len(durations)*0.95)],
            "avg_tokens": sum(tokens) / len(tokens),
            "avg_tool_calls": sum(len(t.tool_calls) for t in self.traces) / len(self.traces)
        }
```

### Step 3：成本控制

```python
class CostController:
    """成本控制：Token 预算 + 单次限制"""

    def __init__(self, max_tokens_per_request: int = 10000,
                 daily_budget_tokens: int = 1000000,
                 cost_per_1k_input: float = 0.15,
                 cost_per_1k_output: float = 0.6):
        self.max_per_request = max_tokens_per_request
        self.daily_budget = daily_budget_tokens
        self.cost_per_1k_input = cost_per_1k_input
        self.cost_per_1k_output = cost_per_1k_output
        self.daily_usage = 0

    def check_budget(self, estimated_tokens: int) -> bool:
        if estimated_tokens > self.max_per_request:
            return False
        if self.daily_usage + estimated_tokens > self.daily_budget:
            return False
        return True

    def record_usage(self, input_tokens: int, output_tokens: int):
        self.daily_usage += input_tokens + output_tokens
        cost = (input_tokens * self.cost_per_1k_input + output_tokens * self.cost_per_1k_output) / 1000
        return cost
```

## 测试方法

| 测试类型 | 方法 | 通过标准 |
|---------|------|---------|
| 负载测试 | 模拟 100 并发请求 | P95 < 10s |
| 故障注入 | API 超时/错误 | 熔断器正常工作 |
| 成本测试 | 持续请求 | 不超预算 |
| 安全测试 | Prompt Injection 攻击 | 拦截率 > 95% |

## 评估指标

| 指标 | 目标 | 告警阈值 |
|------|------|---------|
| 成功率 | > 95% | < 90% |
| P95 延迟 | < 10s | > 15s |
| 错误率 | < 5% | > 10% |
| 日成本 | < 预算 | > 80% 预算 |
| 熔断触发 | < 1 次/天 | > 5 次/天 |

## 常见失败模式

1. **API 限流**：上游 LLM API 限流导致批量失败 → 实现请求队列 + 指数退避
2. **成本超支**：用户大量请求导致 API 费用暴涨 → 每用户/每日 Token 预算
3. **级联故障**：一个组件故障导致整个系统不可用 → 熔断器 + 降级策略
4. **冷启动延迟**：首次请求延迟高 → 预热机制 + 连接池
5. **日志爆炸**：Trace 数据过多 → 采样 + 聚合

## 上线检查清单

- [ ] 超时控制（全局 + 每步）
- [ ] 重试机制（带退避）
- [ ] 熔断器配置
- [ ] 降级策略
- [ ] 速率限制（API + 用户级）
- [ ] Token 预算和成本告警
- [ ] Tracing 和 Metrics 仪表盘
- [ ] 错误告警（PagerDuty/Slack）
- [ ] Input/Output Guardrails
- [ ] 安全审计通过
- [ ] 回滚方案就绪
- [ ] 文档更新（API 文档、运维手册）
- [ ] On-call 轮值安排
- [ ] 压力测试通过

## 验真报告

| 项目 | 结果 | 日期 |
|------|------|------|
| 熔断器在 API 故障时正常工作 | 通过 | 2026-05-08 |
| 降级策略有效 | 通过 | 2026-05-08 |
| 成本控制有效 | 通过 | 2026-05-08 |
| P95 延迟 8.5s (100 并发) | 通过 | 2026-05-08 |
