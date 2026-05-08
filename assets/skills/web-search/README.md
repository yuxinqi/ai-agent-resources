# Web Search Skill

A web search skill for AI agents that retrieves search results with configurable limits, error handling, and structured output.

## Installation

No external dependencies beyond the Python standard library.

```bash
# No pip install needed — uses only stdlib (urllib, json, logging)
```

## Quick Start

```python
from skill import WebSearchSkill

skill = WebSearchSkill(api_key="your-api-key")
results = skill.execute("python async patterns", max_results=5)

for result in results:
    print(f"[{result.rank}] {result.title}")
    print(f"    {result.url}")
    print(f"    {result.snippet}")
```

## API Reference

### `WebSearchSkill`

```python
WebSearchSkill(
    api_key: str | None = None,
    base_url: str | None = None,
    timeout: int = 10,
)
```

| Parameter  | Type     | Default                          | Description              |
|------------|----------|----------------------------------|--------------------------|
| `api_key`  | `str`    | `None`                           | API key for search backend |
| `base_url` | `str`    | `https://api.search.example.com/v1/search` | Search API endpoint |
| `timeout`  | `int`    | `10`                             | Request timeout (seconds) |

#### `execute(query, max_results=5)`

Execute a web search and return structured results.

```python
results: list[SearchResult] = skill.execute(
    query="python async patterns",
    max_results=5,
)
```

- **query** (`str`) — The search query (must be non-empty).
- **max_results** (`int`) — Maximum results to return (1–20).
- **Returns** — `list[SearchResult]` sorted by rank.
- **Raises**:
  - `ValueError` — Invalid query or max_results.
  - `SearchError` — Network or API error.

### `SearchResult`

| Field      | Type             | Description               |
|------------|------------------|---------------------------|
| `title`    | `str`            | Result title              |
| `url`      | `str`            | Result URL                |
| `snippet`  | `str`            | Short text snippet        |
| `rank`     | `int`            | Result rank (1-based)     |
| `metadata` | `dict[str, Any]` | Additional metadata       |

#### `to_dict()`

Convert to a plain dictionary.

## Custom Backend

Subclass `WebSearchSkill` and override `_call_api()`:

```python
class MySearchBackend(WebSearchSkill):
    def _call_api(self, query: str, max_results: int) -> list[dict]:
        # Your custom search implementation
        response = my_search_client.search(query, limit=max_results)
        return response.results
```

## Running Tests

```bash
cd assets/skills/web-search
python -m pytest test_skill.py -v
```

## Error Handling

| Error Type      | When                                     |
|-----------------|------------------------------------------|
| `ValueError`    | Empty query or invalid `max_results`     |
| `SearchError`   | Network failure or invalid API response  |
