---
id: pattern-guardrails
title: Guardrails 模式
type: pattern
level: intermediate
status: draft
evidence_level: L2
practical_rating: A
last_reviewed: "2026-05-08"
valid_until: "2026-08-08"
related:
  - pattern-hitl
  - concept-evaluation
depends_on:
  - concept-agent
  - concept-tool-use
tags:
  - pattern
  - guardrails
  - safety
  - validation
  - input-output
---

# Guardrails 模式

## 架构图

```
┌─────────────────────────────────────────────────┐
│                    用户输入                       │
└─────────────────────┬───────────────────────────┘
                      ▼
              ┌───────────────┐
              │ Input Guard   │ ← 输入验证：格式、意图、安全
              │ (输入护栏)     │
              └───────┬───────┘
                      │ 合法输入
                      ▼
              ┌───────────────┐
              │     Agent     │ ← 正常执行
              │  (智能体)      │
              └───────┬───────┘
                      │ 工具调用
                      ▼
              ┌───────────────┐
              │ Tool Guard    │ ← 工具调用验证：参数、权限、频率
              │ (工具护栏)     │
              └───────┬───────┘
                      │ 合法调用
                      ▼
              ┌───────────────┐
              │ Output Guard  │ ← 输出验证：安全、隐私、格式
              │ (输出护栏)     │
              └───────┬───────┘
                      │ 合法输出
                      ▼
              ┌───────────────┐
              │   最终输出     │
              └───────────────┘
```

## 适用条件

- 系统面向终端用户，需要**防止恶意输入**
- Agent 可以执行有副作用的操作，需要**限制操作范围**
- 输出可能包含敏感信息，需要**过滤隐私内容**
- 合规要求**内容审核**（如金融、医疗领域）
- 系统有**成本限制**，需要防止资源滥用

## 不适用条件

- 内部工具，用户可信
- 对延迟极度敏感（Guardrails 增加延迟）
- Guardrails 本身不可靠（误拦截率过高）
- 简单的规则可用 Prompt 指令替代

## 最小代码示例

```python
import re
from dataclasses import dataclass
from typing import Any, Callable

@dataclass
class GuardrailResult:
    passed: bool
    reason: str = ""
    sanitized_value: Any = None

class InputGuard:
    """输入护栏：验证用户输入"""

    def __init__(self):
        self.rules: list[Callable] = []

    def add_rule(self, rule: Callable):
        self.rules.append(rule)

    def check(self, user_input: str) -> GuardrailResult:
        for rule in self.rules:
            result = rule(user_input)
            if not result.passed:
                return result
        return GuardrailResult(passed=True, sanitized_value=user_input)

# 输入规则
def check_length(max_length: int = 2000) -> Callable:
    def rule(text: str) -> GuardrailResult:
        if len(text) > max_length:
            return GuardrailResult(False, f"输入过长：{len(text)} > {max_length}")
        return GuardrailResult(True)
    return rule

def check_injection(text: str) -> GuardrailResult:
    """检测常见的 Prompt Injection 模式"""
    patterns = [
        r"ignore\s+(all\s+)?previous\s+instructions",
        r"system\s*:\s*",
        r"you\s+are\s+now\s+",
        r"forget\s+(everything|all)",
    ]
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return GuardrailResult(False, f"检测到可能的注入攻击")
    return GuardrailResult(True)

def check_pii(text: str) -> GuardrailResult:
    """检测输入中的个人身份信息"""
    # 手机号
    if re.search(r"1[3-9]\d{9}", text):
        return GuardrailResult(False, "输入包含手机号，请移除敏感信息")
    # 身份证号
    if re.search(r"\d{17}[\dXx]", text):
        return GuardrailResult(False, "输入包含身份证号，请移除敏感信息")
    return GuardrailResult(True)

class ToolGuard:
    """工具调用护栏：验证工具调用的合法性"""

    def __init__(self):
        self.rate_limits: dict[str, list] = {}
        self.blocked_actions: set = set()

    def check(self, tool_name: str, params: dict) -> GuardrailResult:
        if tool_name in self.blocked_actions:
            return GuardrailResult(False, f"工具 {tool_name} 已被禁用")

        # 频率限制
        from time import time
        now = time()
        if tool_name in self.rate_limits:
            self.rate_limits[tool_name] = [
                t for t in self.rate_limits[tool_name] if now - t < 60
            ]
            if len(self.rate_limits[tool_name]) >= 10:  # 每分钟最多 10 次
                return GuardrailResult(False, f"工具 {tool_name} 调用过于频繁")
        self.rate_limits.setdefault(tool_name, []).append(now)

        return GuardrailResult(True)

class OutputGuard:
    """输出护栏：验证 Agent 输出"""

    def check(self, output: str) -> GuardrailResult:
        # 检查是否泄露了系统 Prompt
        if "system_prompt" in output.lower() or "你是一个" in output[:50]:
            return GuardrailResult(False, "输出可能泄露了系统指令")

        # 检查敏感关键词
        sensitive = ["密码", "password", "api_key", "secret"]
        for kw in sensitive:
            if kw in output.lower():
                return GuardrailResult(False, f"输出包含敏感关键词：{kw}")

        return GuardrailResult(True)

# 组合使用
input_guard = InputGuard()
input_guard.add_rule(check_length())
input_guard.add_rule(check_injection)
input_guard.add_rule(check_pii)

tool_guard = ToolGuard()
tool_guard.blocked_actions.add("execute_shell")  # 禁用危险工具

output_guard = OutputGuard()

def safe_agent(user_input: str, agent_fn: Callable) -> str:
    # 输入检查
    input_result = input_guard.check(user_input)
    if not input_result.passed:
        return f"[输入被拦截] {input_result.reason}"

    # 执行 Agent
    output = agent_fn(input_result.sanitized_value)

    # 输出检查
    output_result = output_guard.check(output)
    if not output_result.passed:
        return "抱歉，我无法提供该回答。"

    return output
```

## 失败模式

| 失败模式 | 症状 | 解法 |
|---------|------|------|
| 误拦截 | 合法输入被错误拒绝 | 收集误拦截案例，优化规则精确度 |
| 绕过 | 攻击者绕过 Guardrails | 多层防护 + Prompt 层面也加约束 |
| 性能开销 | Guardrails 增加显著延迟 | 规则检查优先，LLM 检查仅在必要时使用 |
| 规则冲突 | 不同规则互相矛盾 | 明确规则优先级，记录冲突案例 |
| 规则膨胀 | 规则越来越多难以维护 | 定期审查，合并相似规则，删除过时规则 |

## 验收标准

1. 已知攻击向量拦截率 > 99%
2. 合法请求误拦截率 < 1%
3. Guardrails 延迟增加 < 100ms（规则型）
4. 输出敏感信息泄露率 < 0.1%
5. 工具调用频率限制 100% 生效

## 相关模式

- [Human-in-the-Loop](human-in-the-loop.md) — Guardrails 无法处理时升级为人工审批
- [Evaluation](../concepts/evaluation.md) — 评估 Guardrails 的有效性

## 验真状态

| 结论 | 证据等级 | 来源 |
|------|---------|------|
| 多层防护比单层更可靠 | L2 | 安全工程最佳实践 |
| 规则型 Guardrails 延迟可忽略 | L3 | 多生产系统验证 |
| Prompt Injection 检测仍有大量绕过方式 | L2 | OWASP LLM 安全研究 |
| 输出护栏对敏感信息过滤有效 | L2 | Nemo Guardrails 实践 |

## 参考来源

- NVIDIA NeMo Guardrails (2024)
- OWASP Top 10 for LLM Applications (2024)
- Rebuff.ai Prompt Injection Detection (2024)
- Lakera Guard Security Research (2024)
