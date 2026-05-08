# Tool-Using Agent Example

A complete minimal agent that uses OpenAI-compatible tool calling to solve tasks with calculator, web_search, and file_reader tools.

## What It Demonstrates

- **Tool definitions** using the OpenAI function calling format
- **Tool-calling loop** — the agent iterates between LLM responses and tool executions
- **Three tools**: calculator, web_search, file_reader
- **Error handling** for tool execution failures
- **Iteration limit** to prevent infinite loops

## Quick Start

```bash
# Set your API key
export OPENAI_API_KEY="sk-..."

# Run the agent
python main.py "What is 15% of 847?"
python main.py "Search for Python async patterns and summarize the findings"
python main.py "Read the file data.txt and tell me the total"
```

## Architecture

```
User Query
    │
    ▼
┌──────────┐
│   LLM    │◄─────────────────┐
│ (GPT-4o) │                  │
└────┬─────┘                  │
     │                        │
     ├── No tool call ──► Return answer
     │
     ├── Tool call: calculator()
     │        │
     │        ▼
     │    Execute ──► Result
     │
     ├── Tool call: web_search()
     │        │
     │        ▼
     │    Execute ──► Result
     │
     └── Tool call: file_reader()
              │
              ▼
          Execute ──► Result ───────┘
                                    (loop back to LLM)
```

## Tools

### Calculator

Evaluates mathematical expressions safely.

```python
calculator("2 ** 10")        # → "1024"
calculator("sqrt(144)")      # → "12.0"
calculator("15 * 847 / 100") # → "127.05"
```

### Web Search

Searches the web for information (simulated in the demo).

```python
web_search("Python async patterns", max_results=5)
```

### File Reader

Reads local files in .txt, .md, .json, .csv formats.

```python
file_reader("data/config.json")  # Returns parsed JSON
file_reader("notes.txt")          # Returns text content
```

## Customization

### Adding a New Tool

1. Implement the tool function:

```python
def my_tool(param1: str) -> str:
    """My custom tool description."""
    return "result"
```

2. Add the tool definition to `TOOL_DEFINITIONS`:

```python
{
    "type": "function",
    "function": {
        "name": "my_tool",
        "description": "What the tool does",
        "parameters": {
            "type": "object",
            "properties": {
                "param1": {"type": "string", "description": "First parameter"}
            },
            "required": ["param1"]
        }
    }
}
```

3. Register it in `TOOL_MAP`:

```python
TOOL_MAP["my_tool"] = my_tool
```

### Using a Real Search API

Replace the `web_search()` function with a call to an actual search API (see `assets/skills/web-search/skill.py`).

## Requirements

- Python 3.10+
- OpenAI API key
- No external pip packages required (uses stdlib only)
