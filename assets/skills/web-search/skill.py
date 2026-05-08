"""Web Search Skill for AI agents.

Provides a WebSearchSkill class that wraps web search functionality
with configurable result limits, error handling, and structured output.
"""

from __future__ import annotations

import json
import logging
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from typing import Any, Optional

logger = logging.getLogger(__name__)


@dataclass
class SearchResult:
    """A single search result entry."""

    title: str
    url: str
    snippet: str
    rank: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "title": self.title,
            "url": self.url,
            "snippet": self.snippet,
            "rank": self.rank,
            "metadata": self.metadata,
        }


class WebSearchSkill:
    """Web search skill that retrieves search results for a given query.

    This skill provides a simple interface for AI agents to search the web.
    It uses a pluggable backend architecture — the default implementation
    uses a JSON-over-HTTP API, but can be subclassed for custom backends.

    Args:
        api_key: API key for the search backend.
        base_url: Base URL for the search API endpoint.
        timeout: Request timeout in seconds.

    Example:
        >>> skill = WebSearchSkill(api_key="your-key")
        >>> results = skill.execute("python async patterns", max_results=3)
        >>> for r in results:
        ...     print(f"[{r.rank}] {r.title}: {r.snippet}")
    """

    DEFAULT_BASE_URL = "https://api.search.example.com/v1/search"

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 10,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url or self.DEFAULT_BASE_URL
        self.timeout = timeout

    def execute(
        self,
        query: str,
        max_results: int = 5,
    ) -> list[SearchResult]:
        """Execute a web search and return structured results.

        Args:
            query: The search query string.
            max_results: Maximum number of results to return (1-20).

        Returns:
            A list of SearchResult objects sorted by rank.

        Raises:
            ValueError: If query is empty or max_results is out of range.
            SearchError: If the search API returns an error.
        """
        self._validate_inputs(query, max_results)

        logger.info("Searching for: %s (max_results=%d)", query, max_results)

        try:
            raw_results = self._call_api(query, max_results)
        except urllib.error.URLError as exc:
            raise SearchError(f"Network error during search: {exc}") from exc
        except json.JSONDecodeError as exc:
            raise SearchError(f"Invalid response from search API: {exc}") from exc

        results = self._parse_results(raw_results, max_results)
        logger.info("Found %d results for query: %s", len(results), query)
        return results

    def _validate_inputs(self, query: str, max_results: int) -> None:
        """Validate search inputs."""
        if not query or not query.strip():
            raise ValueError("Query must be a non-empty string.")
        if not 1 <= max_results <= 20:
            raise ValueError("max_results must be between 1 and 20, got %d" % max_results)

    def _call_api(self, query: str, max_results: int) -> list[dict[str, Any]]:
        """Call the search API and return raw JSON results.

        Override this method to integrate with a different search backend.
        """
        params = urllib.parse.urlencode({
            "q": query,
            "num": max_results,
            "key": self.api_key or "",
        })
        url = f"{self.base_url}?{params}"

        request = urllib.request.Request(url, headers={"Accept": "application/json"})

        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            data = json.loads(response.read().decode("utf-8"))

        return data.get("results", [])

    def _parse_results(
        self,
        raw_results: list[dict[str, Any]],
        max_results: int,
    ) -> list[SearchResult]:
        """Parse raw API results into SearchResult objects."""
        results: list[SearchResult] = []
        for i, item in enumerate(raw_results[:max_results]):
            result = SearchResult(
                title=item.get("title", ""),
                url=item.get("url", ""),
                snippet=item.get("snippet", ""),
                rank=i + 1,
                metadata=item.get("metadata", {}),
            )
            results.append(result)
        return results


class SearchError(Exception):
    """Raised when the search operation fails."""

    pass
