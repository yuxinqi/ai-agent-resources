# Research Summary Prompt

Synthesize multiple research sources into a structured summary with key findings, methodology notes, and confidence ratings.

## Overview

This prompt helps AI agents produce high-quality research summaries by:

1. **Synthesizing** information from multiple sources
2. **Identifying** key findings with confidence ratings
3. **Highlighting** disagreements between sources
4. **Flagging** methodological limitations

## Parameters

| Parameter   | Type    | Required | Default | Description                          |
|-------------|---------|----------|---------|--------------------------------------|
| `topic`     | string  | Yes      | —       | The research topic to summarize      |
| `sources`   | array   | Yes      | —       | List of source documents to analyze  |
| `max_length`| integer | No       | 1000    | Maximum word count for the summary   |
| `focus_areas`| array  | No       | []      | Sub-topics to prioritize             |

### Source Object

Each source in the `sources` array should have:

- `title` (string) — Title or identifier of the source
- `content` (string) — The text content from the source
- `url` (string, optional) — URL for the source

## Output Structure

The prompt returns a structured object with:

- **summary** — The synthesized research summary text
- **key_findings** — Array of findings, each with:
  - `finding` — The finding text
  - `confidence` — Rating: high, medium, or low
  - `sources` — Which source(s) support this finding
- **disagreements** — Areas where sources conflict
- **limitations** — Methodological concerns or data gaps

## Usage Example

```python
from jinja2 import Template
import yaml

# Load the prompt
with open("prompt.yaml") as f:
    prompt_config = yaml.safe_load(f)

# Prepare your data
data = {
    "topic": "Impact of remote work on productivity",
    "sources": [
        {
            "title": "Stanford Study 2023",
            "content": "Remote workers were 13% more productive...",
            "url": "https://example.com/study"
        }
    ],
    "max_length": 500,
    "focus_areas": ["productivity metrics"]
}

# Render the user prompt
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

1. Remote work productivity — multiple sources with disagreements
2. Carbon capture technology — conflicting efficiency data
3. Microservices architecture — technology domain synthesis
4. Vitamin D supplementation — medical evidence with confounders
5. LLM hallucination rates — single-source summary

## Design Principles

- **Never fabricate**: All findings must trace back to provided sources
- **Confidence-aware**: Explicit ratings help downstream consumers assess reliability
- **Disagreement-transparent**: Conflicting findings are surfaced, not hidden
- **Concise by default**: Respects `max_length` to avoid bloated outputs
