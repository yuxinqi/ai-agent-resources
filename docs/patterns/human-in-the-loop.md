---
id: pattern-hitl
title: Human-in-the-Loop 模式
type: pattern
level: intermediate
status: draft
evidence_level: L2
practical_rating: A
last_reviewed: "2026-05-08"
valid_until: "2026-08-08"
related:
  - pattern-guardrails
  - pattern-reflection
  - concept-evaluation
depends_on:
  - concept-agent
tags:
  - pattern
  - human-in-the-loop
  - approval
  - safety
---

# Human-in-the-Loop 模式

## 架构图

```
┌─────────────────────────────────────────────────┐
│                    用户输入                       │
└─────────────────────┬───────────────────────────┘
                      ▼
              ┌───────────────┐
              │     Agent     │ ← 自主执行
              │  (智能体)      │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │  需要审批？     │ ← 规则判断
              └───────┬───────┘
                      │
            ┌─────────┴─────────┐
            ▼                   ▼
          不需要               需要
    → 直接执行          ┌──────────────┐
                       │  Human 审批   │
                       │  (人工审批)    │
                       └──────┬───────┘
                              │
                    ┌─────────┼─────────┐
                    ▼                   ▼
                  批准                拒绝/修改
              → 执行操作          → Agent 调整后重试
```

## 适用条件

- 操作有**不可逆的副作用**（删除数据、发送邮件、资金操作）
- 输出需要**专业判断**（法律文本、医疗建议）
- 系统刚上线，**还不够可靠**，需要人工兜底
- 合规要求**人工审核**（金融、医疗、法律领域）

## 不适用条件

- 操作完全可逆且低风险
- 人工审批延迟不可接受（如实时客服）
- 审批量过大，人工处理不过来
- 人工审批成为瓶颈，降低系统价值

## 最小代码示例

```python
from enum import Enum
from typing import Callable

class ApprovalStatus(Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    MODIFIED = "modified"

class HumanInTheLoop:
    def __init__(self):
        self.auto_approve_rules = {}  # 操作类型 → 自动审批规则
        self.pending_approvals = []

    def add_rule(self, action_type: str, auto_approve: bool,
                 risk_threshold: float = 0.5):
        """添加审批规则"""
        self.auto_approve_rules[action_type] = {
            "auto_approve": auto_approve,
            "risk_threshold": risk_threshold
        }

    def should_approve(self, action: dict) -> bool:
        """判断操作是否需要人工审批"""
        action_type = action["type"]
        rule = self.auto_approve_rules.get(action_type, {
            "auto_approve": False,
            "risk_threshold": 0.0
        })

        # 规则明确允许自动审批
        if rule["auto_approve"] and action.get("risk", 1.0) <= rule["risk_threshold"]:
            return False

        # 高风险操作始终需要审批
        HIGH_RISK_ACTIONS = {"delete", "send_email", "transfer_money", "publish"}
        if action_type in HIGH_RISK_ACTIONS:
            return True

        # 默认需要审批
        return not rule["auto_approve"]

    def request_approval(self, action: dict, approver: Callable) -> dict:
        """请求人工审批"""
        if not self.should_approve(action):
            return {"status": ApprovalStatus.APPROVED, "action": action}

        # 展示给审批人
        approval = approver(action)

        if approval["status"] == ApprovalStatus.MODIFIED:
            # 人工修改了操作参数
            return {"status": ApprovalStatus.MODIFIED, "action": approval["modified_action"]}

        return {"status": approval["status"], "action": action}

# 使用示例
hitl = HumanInTheLoop()

# 低风险操作自动审批
hitl.add_rule("search", auto_approve=True, risk_threshold=1.0)
hitl.add_rule("read", auto_approve=True, risk_threshold=1.0)

# 高风险操作需审批
hitl.add_rule("delete", auto_approve=False)
hitl.add_rule("send_email", auto_approve=False)

# 模拟人工审批
def mock_approver(action):
    print(f"[审批请求] 操作类型: {action['type']}, 参数: {action.get('params')}")
    response = input("批准？(y/n/m=修改): ").strip().lower()
    if response == "y":
        return {"status": ApprovalStatus.APPROVED}
    elif response == "m":
        return {"status": ApprovalStatus.MODIFIED, "modified_action": {
            **action, "params": {"to": "modified@example.com"}
        }}
    return {"status": ApprovalStatus.REJECTED}

result = hitl.request_approval(
    {"type": "send_email", "params": {"to": "user@example.com", "body": "..."}, "risk": 0.8},
    mock_approver
)
```

## 失败模式

| 失败模式 | 症状 | 解法 |
|---------|------|------|
| 审批疲劳 | 人工审批太多，审批人随意批准 | 分级审批，低风险自动通过，仅高风险需审批 |
| 审批瓶颈 | 人工审批延迟过长 | 异步审批 + 通知机制，设置审批超时 |
| 审批标准不一致 | 不同审批人标准不同 | 标准化审批清单，量化风险评分 |
| 过度依赖人工 | 所有操作都需审批，系统失去自动化价值 | 逐步扩大自动审批范围，监控自动审批准确率 |
| 审批绕过 | Agent 绕过审批机制 | 审批逻辑在 Agent 外部（Middleware层），非 Prompt 控制 |

## 验收标准

1. 所有高风险操作 100% 经过审批
2. 自动审批准确率 > 99%（不应自动审批的被拦截）
3. 平均审批等待时间 < 5 分钟
4. 审批拒绝率 < 30%（过高说明 Agent 质量差）
5. 审批通过后操作成功率 > 95%

## 相关模式

- [Guardrails](guardrails.md) — 自动化的安全防护
- [Reflection](reflection.md) — 自我修正减少人工审批需求

## 验真状态

| 结论 | 证据等级 | 来源 |
|------|---------|------|
| HITL 是高风险操作的标准做法 | L3 | 金融、医疗行业标准 |
| 分级审批可减少 80% 的审批量 | L2 | 多企业实践 |
| 审批疲劳在每天 > 20 次时出现 | L1 | UX 研究 |

## 参考来源

- Microsoft, "Human-in-the-Loop Patterns for AI Systems" (2024)
- LangGraph Human-in-the-Loop Documentation (2024)
- Amershi et al., "Guidelines for Human-AI Interaction" (2019)
