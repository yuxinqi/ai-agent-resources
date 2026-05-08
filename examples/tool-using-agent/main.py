#!/usr/bin/env python3
"""Tool-Using Agent Example.

A complete minimal agent that uses OpenAI-compatible tool calling to
solve tasks with calculator, web_search, and file_reader tools.

Usage:
    python main.py "What is 15% of 847?"
    python main.py "Search for Python async patterns and summarize"
    python main.py "Read the file data.txt and tell me the total"

Requires:
    export OPENAI_API_KEY="sk-..."
"""

from __future__ import annotations

import json
import math
import os
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Optional


# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------

def calculator(expression: str) -> str:
    """Evaluate a mathematical expression safely.

    Supports: +, -, *, /, **, sqrt, sin, cos, tan, log, pi, e.

    Args:
        expression: A mathematical expression string.

    Returns:
        The result as a string, or an error message.
    """
    # Allowed names for safe evaluation
    allowed_names: dict[str, Any] = {
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "log": math.log,
        "log10": math.log10,
        "pi": math.pi,
        "e": math.e,
        "abs": abs,
        "round": round,
        "min": min,
        "max": max,
    }

    # Only allow safe characters
    allowed_chars = set("0123456789+-*/.() ,")
    cleaned = expression.replace(" ", "")
    for char in cleaned:
        if char not in allowed_chars and char not in "".join(allowed_names):
            # Allow alphabetic chars for function names
            if not char.isalpha() and char != "_":
                return f"Error: unsafe character '{char}' in expression"

    try:
        result = eval(expression, {"__builtins__": {}}, allowed_names)  # noqa: S307
        return str(result)
    except ZeroDivisionError:
        return "Error: division by zero"
    except Exception as exc:
        return f"Error: {exc}"


def web_search(query: str, max_results: int = 5) -> str:
    """Search the web for information.

    In this demo, returns simulated search results.
    Replace with a real search API for production use.

    Args:
        query: The search query string.
        max_results: Maximum number of results (1-10).

    Returns:
        A formatted string of search results.
    """
    # Simulated results — replace with real API call
    simulated_results = [
        {
            "title": f"Search result for: {query}",
            "url": f"https://example.com/search?q={urllib.parse.quote(query)}",
            "snippet": f"This page contains information about {query}. "
                       f"It covers key concepts, practical examples, and best practices.",
        },
        {
            "title": f"Comprehensive guide to {query}",
            "url": f"https://example.com/guide/{urllib.parse.quote(query)}",
            "snippet": f"A detailed guide covering all aspects of {query} "
                       f"with step-by-step tutorials and code examples.",
        },
    ]

    results = simulated_results[:max_results]
    output_lines: list[str] = []
    for i, result in enumerate(results, 1):
        output_lines.append(f"{i}. {result['title']}")
        output_lines.append(f"   URL: {result['url']}")
        output_lines.append(f"   {result['snippet']}")
        output_lines.append("")

    return "\n".join(output_lines)


def file_reader(file_path: str) -> str:
    """Read the contents of a file.

    Supports .txt, .md, .json, and .csv files.

    Args:
        file_path: Path to the file to read.

    Returns:
        The file contents as a string, or an error message.
    """
    path = Path(file_path)

    if not path.exists():
        return f"Error: file not found: {file_path}"

    if not path.is_file():
        return f"Error: not a file: {file_path}"

    ext = path.suffix.lower()
    supported = {".txt", ".md", ".json", ".csv"}

    if ext not in supported:
        return f"Error: unsupported format '{ext}'. Supported: {', '.join(sorted(supported))}"

    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return f"Error: could not decode file as UTF-8: {file_path}"
    except OSError as exc:
        return f"Error reading file: {exc}"

    # For JSON, validate and pretty-print
    if ext == ".json":
        try:
            data = json.loads(content)
            return json.dumps(data, indent=2, ensure_ascii=False)
        except json.JSONDecodeError as exc:
            return f"Error: invalid JSON: {exc}"

    return content


# ---------------------------------------------------------------------------
# Tool definitions for OpenAI function calling
# ---------------------------------------------------------------------------

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluate a mathematical expression. Supports +, -, *, /, **, sqrt, sin, cos, log, pi, e.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The mathematical expression to evaluate, e.g. '2 ** 10' or 'sqrt(144)'",
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for information about a topic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results (1-10)",
                        "default": 5,
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "file_reader",
            "description": "Read the contents of a local file. Supports .txt, .md, .json, .csv.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to read",
                    }
                },
                "required": ["file_path"],
            },
        },
    },
]

# Map tool names to implementations
TOOL_MAP: dict[str, Any] = {
    "calculator": calculator,
    "web_search": web_search,
    "file_reader": file_reader,
}


# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------

class ToolUsingAgent:
    """A minimal agent that uses OpenAI-compatible tool calling.

    The agent runs a loop:
    1. Send messages (including tool results) to the LLM.
    2. If the LLM requests tool calls, execute them and add results.
    3. If the LLM responds without tool calls, return the response.

    Args:
        base_url: OpenAI-compatible API base URL.
        api_key: API key for authentication.
        model: Model identifier.
        max_iterations: Maximum tool-calling iterations before stopping.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        model: str = "gpt-4o-mini",
        max_iterations: int = 10,
    ) -> None:
        self.base_url = (base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")).rstrip("/")
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.model = model
        self.max_iterations = max_iterations

    def run(self, user_message: str) -> str:
        """Run the agent on a user message and return the final response.

        Args:
            user_message: The user's request.

        Returns:
            The agent's final text response.
        """
        messages: list[dict[str, Any]] = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant with access to tools. "
                    "Use tools when they can help answer the user's question. "
                    "Always explain your reasoning before and after using tools."
                ),
            },
            {"role": "user", "content": user_message},
        ]

        for iteration in range(self.max_iterations):
            print(f"\n--- Iteration {iteration + 1} ---")

            # Call the LLM
            response_data = self._call_llm(messages)
            choice = response_data["choices"][0]
            message = choice["message"]

            # Add assistant message to history
            messages.append(message)

            # Check if the model wants to call tools
            tool_calls = message.get("tool_calls")

            if not tool_calls:
                # No more tool calls — return the final response
                return message.get("content", "")

            # Execute each tool call
            for tool_call in tool_calls:
                function_name = tool_call["function"]["name"]
                function_args_str = tool_call["function"]["arguments"]
                tool_call_id = tool_call["id"]

                print(f"  Tool call: {function_name}({function_args_str})")

                try:
                    function_args = json.loads(function_args_str)
                except json.JSONDecodeError:
                    function_args = {}

                # Execute the tool
                tool_fn = TOOL_MAP.get(function_name)
                if tool_fn is None:
                    result = f"Error: unknown tool '{function_name}'"
                else:
                    try:
                        result = tool_fn(**function_args)
                    except Exception as exc:
                        result = f"Error executing {function_name}: {exc}"

                print(f"  Tool result: {result[:200]}{'...' if len(result) > 200 else ''}")

                # Add tool result to messages
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "content": result,
                })

        return "Agent reached maximum iterations without producing a final answer."

    def _call_llm(self, messages: list[dict[str, Any]]) -> dict[str, Any]:
        """Call the OpenAI-compatible chat completion API."""
        url = f"{self.base_url}/chat/completions"
        payload = json.dumps({
            "model": self.model,
            "messages": messages,
            "tools": TOOL_DEFINITIONS,
            "tool_choice": "auto",
            "temperature": 0.3,
        }).encode()

        request = urllib.request.Request(
            url,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
        )

        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode())


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    """Command-line entry point."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python main.py 'your question here'")
        print()
        print("Examples:")
        print("  python main.py 'What is 15% of 847?'")
        print("  python main.py 'Search for Python async patterns'")
        print("  python main.py 'Read data.txt and summarize it'")
        sys.exit(1)

    user_message = " ".join(sys.argv[1:])

    if not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY not set. Set it with:")
        print("  export OPENAI_API_KEY='sk-...'")
        print()

    agent = ToolUsingAgent()
    result = agent.run(user_message)

    print("\n=== Final Answer ===")
    print(result)


if __name__ == "__main__":
    main()
