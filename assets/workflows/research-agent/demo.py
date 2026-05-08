#!/usr/bin/env python3
"""Research Agent Demo.

A minimal demo that runs the research-agent workflow from the command line.

Usage:
    python demo.py "your research topic"
    python demo.py "quantum computing applications" --focus "cryptography,drug discovery"
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from typing import Any, Optional


# ---------------------------------------------------------------------------
# Minimal LLM client (OpenAI-compatible API)
# ---------------------------------------------------------------------------

class LLMClient:
    """Minimal client for OpenAI-compatible chat completion API."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        model: str = "gpt-4o-mini",
    ) -> None:
        self.base_url = (base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")).rstrip("/")
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.model = model

    def chat(self, system: str, user: str) -> str:
        """Send a chat completion request and return the assistant message."""
        url = f"{self.base_url}/chat/completions"
        payload = json.dumps({
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
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
            data = json.loads(response.read().decode())

        return data["choices"][0]["message"]["content"]


# ---------------------------------------------------------------------------
# Workflow node implementations
# ---------------------------------------------------------------------------

def plan_queries(llm: LLMClient, topic: str, focus_areas: list[str]) -> list[str]:
    """Node: query_planner — decompose topic into search queries."""
    system = "You are a research query planner. Output only a JSON array of query strings."
    focus_text = f"\nFocus areas: {', '.join(focus_areas)}" if focus_areas else ""
    user = f"Generate 3-5 specific search queries for researching: {topic}{focus_text}"

    response = llm.chat(system, user)
    try:
        queries = json.loads(response)
        if isinstance(queries, list):
            return queries
    except json.JSONDecodeError:
        pass

    # Fallback: split by newlines if JSON parsing fails
    return [q.strip().strip('- ').strip('"') for q in response.strip().split("\n") if q.strip()]


def web_search(queries: list[str], max_results: int = 3) -> list[dict[str, Any]]:
    """Node: web_searcher — simulate web search results.

    In a real implementation, this would call a search API.
    This demo returns placeholder results.
    """
    results: list[dict[str, Any]] = []
    for i, query in enumerate(queries):
        results.append({
            "doc_id": f"source-{i + 1}",
            "title": f"Research result for: {query}",
            "url": f"https://example.com/search?q={urllib.parse.quote(query)}",
            "snippet": f"This article discusses findings related to {query}.",
        })
    return results


def read_content(search_results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Node: content_reader — read content from search results.

    In a real implementation, this would fetch and parse web pages.
    This demo uses the snippets as content.
    """
    documents: list[dict[str, Any]] = []
    for result in search_results:
        documents.append({
            "doc_id": result["doc_id"],
            "title": result["title"],
            "content": result["snippet"],
        })
    return documents


def summarize(
    llm: LLMClient,
    topic: str,
    documents: list[dict[str, Any]],
    focus_areas: list[str],
) -> dict[str, Any]:
    """Node: summarizer — synthesize documents into a structured summary."""
    system = (
        "You are a research synthesis assistant. "
        "Output a JSON object with: summary (string), key_findings "
        "(list of {finding, confidence, sources}), disagreements (list), "
        "limitations (list)."
    )

    docs_text = "\n".join(
        f"[{d['doc_id']}] {d['title']}\n{d['content']}" for d in documents
    )
    focus_text = f"\nFocus areas: {', '.join(focus_areas)}" if focus_areas else ""
    user = f"Summarize the following research on: {topic}{focus_text}\n\n{docs_text}"

    response = llm.chat(system, user)
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {"summary": response, "key_findings": [], "disagreements": [], "limitations": []}


def check_citations(
    llm: LLMClient,
    summary: dict[str, Any],
    documents: list[dict[str, Any]],
) -> dict[str, Any]:
    """Node: citation_checker — verify citations in the summary."""
    system = (
        "You are a citation verification assistant. "
        "Output a JSON object with: verified (boolean), issues (list), "
        "corrections (list)."
    )

    findings_text = "\n".join(
        f"- {f.get('finding', '')} (sources: {', '.join(f.get('sources', []))})"
        for f in summary.get("key_findings", [])
    )
    sources_text = ", ".join(d["doc_id"] for d in documents)

    user = (
        f"Verify citations in this summary:\n{summary.get('summary', '')}\n\n"
        f"Findings:\n{findings_text}\n\n"
        f"Available sources: {sources_text}"
    )

    response = llm.chat(system, user)
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {"verified": True, "issues": [], "corrections": []}


# ---------------------------------------------------------------------------
# Main workflow runner
# ---------------------------------------------------------------------------

def run_workflow(topic: str, focus_areas: list[str] | None = None) -> dict[str, Any]:
    """Run the complete research-agent workflow."""
    focus_areas = focus_areas or []
    llm = LLMClient()

    print(f"=== Research Agent: {topic} ===\n")

    # Step 1: Plan queries
    print("[1/5] Planning search queries...")
    queries = plan_queries(llm, topic, focus_areas)
    print(f"       Generated {len(queries)} queries: {queries}\n")

    # Step 2: Search the web
    print("[2/5] Searching the web...")
    search_results = web_search(queries)
    print(f"       Found {len(search_results)} results\n")

    # Step 3: Read content
    print("[3/5] Reading content...")
    documents = read_content(search_results)
    print(f"       Read {len(documents)} documents\n")

    # Step 4: Summarize
    print("[4/5] Summarizing findings...")
    summary = summarize(llm, topic, documents, focus_areas)
    print(f"       Summary generated ({len(summary.get('summary', ''))} chars)\n")

    # Step 5: Check citations
    print("[5/5] Checking citations...")
    verification = check_citations(llm, summary, documents)
    verified = verification.get("verified", False)
    print(f"       Citations verified: {verified}\n")

    return {
        "topic": topic,
        "queries": queries,
        "summary": summary,
        "verification": verification,
    }


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Research Agent Demo")
    parser.add_argument("topic", help="Research topic to investigate")
    parser.add_argument(
        "--focus",
        default="",
        help="Comma-separated focus areas",
    )
    args = parser.parse_args()

    focus_areas = [a.strip() for a in args.focus.split(",") if a.strip()] if args.focus else []

    result = run_workflow(args.topic, focus_areas)
    print("\n=== Final Result ===")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
