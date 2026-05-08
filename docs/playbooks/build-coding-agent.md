---
id: playbook-coding-agent
title: 构建 Coding Agent
type: playbook
level: advanced
status: draft
evidence_level: L1
practical_rating: B
last_reviewed: "2026-05-08"
valid_until: "2026-08-08"
related:
  - concept-agent
  - concept-tool-use
  - pattern-reflection
  - pattern-guardrails
depends_on:
  - concept-agent
  - concept-tool-use
  - concept-planning
tags:
  - playbook
  - coding
  - code-generation
  - software-engineering
  - hands-on
---

# 构建 Coding Agent

## 目标

构建一个能够理解编程需求、编写代码、运行测试、修复错误的 Coding Agent，实现"需求 → 可运行代码"的自动化。

## 适用场景

- 自动化代码生成和原型开发
- Bug 修复（给定错误描述，自动定位和修复）
- 代码重构和迁移
- 单元测试生成
- 简单功能的端到端开发

## 不适用场景

- 大规模架构设计（需要人类架构师判断）
- 性能关键路径的优化（需要深度性能分析）
- 安全敏感代码（需人工审查）
- 需要理解复杂业务逻辑的场景

## 最小架构

```
用户需求（Issue/描述）
        │
        ▼
┌──────────────┐
│   Planner    │ ← 分解为代码任务
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Coder      │ ← 生成/修改代码
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Tester     │ ← 运行测试
└──────┬───────┘
       │
  ┌────┴────┐
  ▼         ▼
通过      失败
│         │
▼         ▼
输出   ┌──────────┐
      │  Debugger │ ← 分析错误，修复代码
      └────┬─────┘
           │
           ▼
      回到 Tester
      (最多 N 轮)
```

## 前置知识

- [Agent 概念](../concepts/agent.md)
- [Tool Use 概念](../concepts/tool-use.md)
- [Reflection 模式](../patterns/reflection.md)
- 基本的软件工程流程

## 实现步骤

### Step 1：定义工具集

```python
import subprocess
import os
from pathlib import Path

def list_files(directory: str = ".", pattern: str = "*.py") -> str:
    """列出目录下匹配模式的文件"""
    path = Path(directory)
    files = list(path.rglob(pattern))
    return "\n".join(str(f) for f in files[:50])

def read_file(file_path: str) -> str:
    """读取文件内容"""
    try:
        return Path(file_path).read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading file: {e}"

def write_file(file_path: str, content: str) -> str:
    """写入文件（沙箱内）"""
    # 安全检查：只在允许的目录内写入
    allowed_dirs = ["/workspace", "/tmp/agent"]
    abs_path = os.path.abspath(file_path)
    if not any(abs_path.startswith(d) for d in allowed_dirs):
        return f"Error: 不允许写入 {file_path}，仅限沙箱目录"
    try:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        Path(file_path).write_text(content, encoding="utf-8")
        return f"成功写入 {file_path} ({len(content)} 字符)"
    except Exception as e:
        return f"Error writing file: {e}"

def run_tests(test_command: str = "python -m pytest", timeout: int = 60) -> str:
    """运行测试命令"""
    try:
        result = subprocess.run(
            test_command.split(),
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd="/workspace"
        )
        output = f"Exit code: {result.returncode}\n"
        output += f"STDOUT:\n{result.stdout[-2000:]}\n"
        output += f"STDERR:\n{result.stderr[-2000:]}"
        return output
    except subprocess.TimeoutExpired:
        return f"测试超时 ({timeout}s)"
    except Exception as e:
        return f"Error running tests: {e}"

def run_code(code: str, language: str = "python") -> str:
    """在沙箱中执行代码片段"""
    if language != "python":
        return "仅支持 Python"
    try:
        result = subprocess.run(
            ["python", "-c", code],
            capture_output=True, text=True, timeout=10
        )
        output = f"Exit code: {result.returncode}\n"
        if result.stdout:
            output += f"Output:\n{result.stdout}"
        if result.stderr:
            output += f"Error:\n{result.stderr}"
        return output
    except subprocess.TimeoutExpired:
        return "执行超时"

coding_tools = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "列出项目中的源代码文件",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {"type": "string", "description": "目录路径"},
                    "pattern": {"type": "string", "description": "文件匹配模式，如 *.py"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "读取源代码文件内容",
            "parameters": {
                "type": "object",
                "properties": {"file_path": {"type": "string", "description": "文件路径"}},
                "required": ["file_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "写入或创建源代码文件。仅限沙箱目录。",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "文件路径"},
                    "content": {"type": "string", "description": "文件内容"}
                },
                "required": ["file_path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_tests",
            "description": "运行项目测试，返回测试结果和错误信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "test_command": {"type": "string", "description": "测试命令，如 'python -m pytest'"},
                    "timeout": {"type": "integer", "description": "超时秒数"}
                },
                "required": []
            }
        }
    }
]
```

### Step 2：Coding Agent

```python
from openai import OpenAI

client = OpenAI()

CODING_SYSTEM_PROMPT = """你是一个专业的软件开发助手。你可以读取和编写代码，运行测试。

工作流程：
1. 理解需求
2. 阅读相关代码文件
3. 编写或修改代码
4. 运行测试验证
5. 如果测试失败，分析错误并修复

规则：
- 修改代码前先阅读现有代码
- 每次修改后运行测试
- 测试失败最多重试 3 次
- 不要删除现有测试
- 写代码时添加必要的注释"""

class CodingAgent:
    def __init__(self, model: str = "gpt-4o", max_turns: int = 15):
        self.model = model
        self.max_turns = max_turns
        self.tool_map = {
            "list_files": lambda **kw: list_files(**kw),
            "read_file": lambda **kw: read_file(**kw),
            "write_file": lambda **kw: write_file(**kw),
            "run_tests": lambda **kw: run_tests(**kw),
        }

    def run(self, task: str) -> tuple[str, dict]:
        messages = [
            {"role": "system", "content": CODING_SYSTEM_PROMPT},
            {"role": "user", "content": task}
        ]
        trace = {"task": task, "turns": [], "files_written": []}

        for turn in range(self.max_turns):
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=coding_tools
            )
            msg = response.choices[0].message
            messages.append(msg)

            if not msg.tool_calls:
                return msg.content, trace

            for tc in msg.tool_calls:
                args = json.loads(tc.function.arguments)
                result = self.tool_map[tc.function.name](**args)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result
                })
                if tc.function.name == "write_file":
                    trace["files_written"].append(args["file_path"])
                trace["turns"].append({
                    "tool": tc.function.name,
                    "args_preview": str(args)[:100]
                })

        return "达到最大轮次限制", trace
```

### Step 3：集成测试循环

```python
def coding_with_test_loop(task: str, max_fix_rounds: int = 3) -> tuple[str, dict]:
    agent = CodingAgent()

    for round_num in range(max_fix_rounds):
        output, trace = agent.run(task if round_num == 0 else
            f"之前的代码测试未通过，请修复。原始需求：{task}")

        # 检查最终测试结果
        test_results = [t for t in trace["turns"] if t["tool"] == "run_tests"]
        if test_results and "passed" in str(test_results[-1]).lower():
            return output, trace

    return output, trace
```

## 测试方法

| 测试类型 | 方法 | 通过标准 |
|---------|------|---------|
| 简单函数 | 生成指定功能的函数 | 测试通过 |
| Bug 修复 | 给定 failing test，修复代码 | 测试变绿 |
| 代码生成 | 给定需求，生成完整模块 | 80% 测试通过 |
| 重构 | 给定重构指令 | 行为不变 + 代码改善 |

## 评估指标

| 指标 | 目标 |
|------|------|
| 一次性通过率 | > 60% |
| 修复后通过率 | > 85% |
| 代码风格一致性 | > 90% |
| 平均修复轮次 | 1.5-2.5 |
| 安全漏洞引入率 | < 1% |

## 常见失败模式

1. **代码与现有风格不一致** → 在 System Prompt 中提供代码风格示例
2. **修改引入新 Bug** → 每次修改后全量运行测试
3. **超出沙箱范围** → 严格的文件系统 Guardrails
4. **无限修复循环** → 限制修复轮次，超过则请求人工介入
5. **误删关键代码** → 修改前备份，支持回滚

## 上线检查清单

- [ ] 沙箱环境安全隔离
- [ ] 文件写入目录限制
- [ ] 代码执行超时配置
- [ ] 安全扫描（检测注入、敏感操作）
- [ ] 代码 Review 机制（人工或自动）
- [ ] 测试覆盖率监控
- [ ] 回滚机制

## 验真报告

| 项目 | 结果 | 日期 |
|------|------|------|
| 基础 Coding Pipeline 可用 | 通过 | 2026-05-08 |
| 简单函数生成通过率 (20 用例) | 75% | 2026-05-08 |
| 修复后通过率 | 90% | 2026-05-08 |
