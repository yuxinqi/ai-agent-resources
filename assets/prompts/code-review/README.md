# Code Review Prompt

Perform a structured code review that identifies bugs, security issues, performance problems, and style violations with severity ratings and actionable suggestions.

## Overview

This prompt produces consistent, actionable code reviews by:

1. **Categorizing** findings by type (bug, security, performance, style, maintainability)
2. **Rating** each finding by severity (critical, high, medium, low, info)
3. **Suggesting** specific fixes for every issue found
4. **Acknowledging** what the code does well

## Parameters

| Parameter            | Type    | Required | Default                                       | Description                    |
|----------------------|---------|----------|-----------------------------------------------|--------------------------------|
| `code`               | string  | Yes      | —                                             | The source code to review      |
| `language`           | string  | Yes      | —                                             | Programming language           |
| `file_path`          | string  | No       | —                                             | File path for context          |
| `review_focus`       | array   | No       | ["bugs","security","performance","style"]     | Areas to focus on              |
| `severity_threshold` | string  | No       | "info"                                        | Minimum severity to report     |

### Supported Languages

python, javascript, typescript, go, java, rust, ruby, cpp, c, other

## Output Structure

- **overall_assessment** — Brief summary of code quality
- **findings** — Array of issues, each with:
  - `severity` — critical / high / medium / low / info
  - `category` — bug / security / performance / style / maintainability / accessibility
  - `location` — Line number or code reference
  - `description` — What the issue is
  - `suggestion` — Specific fix
  - `rule` — Optional standard being violated (CWE, PEP8, etc.)
- **positives** — Things the code does well
- **summary_stats** — Count of findings by severity level

## Usage Example

```python
from jinja2 import Template
import yaml

with open("prompt.yaml") as f:
    prompt_config = yaml.safe_load(f)

data = {
    "code": "def login(user, pwd):\n    if user == 'admin' and pwd == '1234':\n        return True",
    "language": "python",
    "file_path": "auth/login.py",
    "review_focus": ["security", "bugs"],
    "severity_threshold": "medium"
}

template = Template(prompt_config["user_prompt_template"])
rendered = template.render(**data)

# Use with your LLM
# response = llm.chat(
#     system=prompt_config["system_prompt"],
#     user=rendered
# )
```

## Test Cases

The `examples.jsonl` file contains 5 test cases covering:

1. SQL injection in Python — security-focused review
2. Off-by-one error in JavaScript — bug-focused review
3. XSS vulnerability in Go — security-focused review
4. Weak hashing + bug in Python — security and bug review
5. Clean Python code — should produce mostly low/info findings

## Design Principles

- **Actionable**: Every finding includes a specific suggestion
- **Severity-aware**: Critical issues are never buried in noise
- **Balanced**: Acknowledges good code, not just problems
- **Standard-referencing**: Maps findings to CWE, PEP8, etc. where applicable
