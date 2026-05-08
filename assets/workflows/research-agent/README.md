# Research Agent Workflow

A multi-step research agent workflow that plans queries, searches the web, reads content, summarizes findings, and verifies citations.

## Workflow Architecture

```
query_planner → web_searcher → content_reader → summarizer → citation_checker
```

### Nodes

| Node              | Type   | Description                                      |
|-------------------|--------|--------------------------------------------------|
| `query_planner`   | LLM    | Decompose topic into focused search queries      |
| `web_searcher`    | Skill  | Execute searches and collect URLs                |
| `content_reader`  | Skill  | Extract text from search results                 |
| `summarizer`      | LLM    | Synthesize documents into structured summary     |
| `citation_checker`| LLM    | Verify citations map to actual source content    |

## Quick Start

```bash
# Set your OpenAI API key
export OPENAI_API_KEY="sk-..."

# Run the demo
python demo.py "quantum computing applications"
python demo.py "remote work productivity" --focus "collaboration,wellbeing"
```

## Workflow Inputs

| Parameter      | Type    | Required | Default | Description                    |
|----------------|---------|----------|---------|--------------------------------|
| `topic`        | string  | Yes      | —       | The research topic             |
| `focus_areas`  | array   | No       | []      | Sub-topics to prioritize       |

## Workflow Outputs

| Output          | Type   | Description                     |
|-----------------|--------|---------------------------------|
| `summary`       | dict   | Structured research summary     |
| `verification`  | dict   | Citation verification results   |

### Summary Structure

```json
{
  "summary": "...",
  "key_findings": [
    {"finding": "...", "confidence": "high", "sources": ["source-1"]}
  ],
  "disagreements": [],
  "limitations": []
}
```

### Verification Structure

```json
{
  "verified": true,
  "issues": [],
  "corrections": []
}
```

## Customization

### Using a Real Search API

Replace the `web_search()` function in `demo.py` with a call to an actual search API:

```python
def web_search(queries: list[str], max_results: int = 3) -> list[dict]:
    from skill import WebSearchSkill
    skill = WebSearchSkill(api_key=os.getenv("SEARCH_API_KEY"))
    results = []
    for query in queries:
        results.extend(skill.execute(query, max_results=max_results))
    return results
```

### Adding New Nodes

Edit `workflow.yaml` to add nodes between existing steps:

```yaml
nodes:
  my_new_node:
    type: llm
    description: Custom processing step
    next: summarizer
```

## Requirements

- Python 3.10+
- OpenAI API key (for LLM calls)
- Optional: `openai`, `requests`, `Jinja2`, `PyYAML` (see requirements.txt)
