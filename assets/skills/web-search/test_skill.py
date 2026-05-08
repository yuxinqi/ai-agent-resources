"""Tests for WebSearchSkill."""

from __future__ import annotations

import json
import urllib.error
from unittest.mock import MagicMock, patch

import pytest

from skill import SearchError, SearchResult, WebSearchSkill


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def skill() -> WebSearchSkill:
    """Return a WebSearchSkill instance with a test API key."""
    return WebSearchSkill(api_key="test-key", base_url="https://api.test.example.com/v1/search")


@pytest.fixture
def mock_api_response() -> list[dict]:
    """Return a mock API response with 3 results."""
    return {
        "results": [
            {
                "title": "Python Async Patterns",
                "url": "https://example.com/async",
                "snippet": "Learn async patterns in Python.",
                "metadata": {"source": "docs"},
            },
            {
                "title": "AsyncIO Tutorial",
                "url": "https://example.com/asyncio",
                "snippet": "Complete asyncio tutorial for beginners.",
                "metadata": {},
            },
            {
                "title": "Concurrency in Python",
                "url": "https://example.com/concurrency",
                "snippet": "Understanding concurrency models.",
                "metadata": {"source": "blog"},
            },
        ]
    }


# ---------------------------------------------------------------------------
# Input validation tests
# ---------------------------------------------------------------------------

class TestInputValidation:
    """Tests for input validation in execute()."""

    def test_empty_query_raises_value_error(self, skill: WebSearchSkill) -> None:
        with pytest.raises(ValueError, match="non-empty"):
            skill.execute("")

    def test_whitespace_query_raises_value_error(self, skill: WebSearchSkill) -> None:
        with pytest.raises(ValueError, match="non-empty"):
            skill.execute("   ")

    def test_max_results_below_one_raises_value_error(self, skill: WebSearchSkill) -> None:
        with pytest.raises(ValueError, match="between 1 and 20"):
            skill.execute("test", max_results=0)

    def test_max_results_above_twenty_raises_value_error(self, skill: WebSearchSkill) -> None:
        with pytest.raises(ValueError, match="between 1 and 20"):
            skill.execute("test", max_results=21)


# ---------------------------------------------------------------------------
# Successful search tests
# ---------------------------------------------------------------------------

class TestSuccessfulSearch:
    """Tests for successful search execution."""

    @patch("skill.urllib.request.urlopen")
    def test_execute_returns_search_results(
        self,
        mock_urlopen: MagicMock,
        skill: WebSearchSkill,
        mock_api_response: dict,
    ) -> None:
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(mock_api_response).encode()
        mock_response.__enter__ = lambda s: s
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response

        results = skill.execute("python async", max_results=3)

        assert len(results) == 3
        assert all(isinstance(r, SearchResult) for r in results)
        assert results[0].title == "Python Async Patterns"
        assert results[0].rank == 1
        assert results[1].rank == 2
        assert results[2].rank == 3

    @patch("skill.urllib.request.urlopen")
    def test_execute_respects_max_results(
        self,
        mock_urlopen: MagicMock,
        skill: WebSearchSkill,
        mock_api_response: dict,
    ) -> None:
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(mock_api_response).encode()
        mock_response.__enter__ = lambda s: s
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response

        results = skill.execute("python async", max_results=2)

        assert len(results) == 2

    @patch("skill.urllib.request.urlopen")
    def test_execute_handles_empty_results(
        self,
        mock_urlopen: MagicMock,
        skill: WebSearchSkill,
    ) -> None:
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({"results": []}).encode()
        mock_response.__enter__ = lambda s: s
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response

        results = skill.execute("obscure query xyz", max_results=5)

        assert len(results) == 0


# ---------------------------------------------------------------------------
# Error handling tests
# ---------------------------------------------------------------------------

class TestErrorHandling:
    """Tests for error handling in execute()."""

    @patch("skill.urllib.request.urlopen")
    def test_network_error_raises_search_error(
        self,
        mock_urlopen: MagicMock,
        skill: WebSearchSkill,
    ) -> None:
        mock_urlopen.side_effect = urllib.error.URLError("Connection refused")

        with pytest.raises(SearchError, match="Network error"):
            skill.execute("test query")

    @patch("skill.urllib.request.urlopen")
    def test_invalid_json_raises_search_error(
        self,
        mock_urlopen: MagicMock,
        skill: WebSearchSkill,
    ) -> None:
        mock_response = MagicMock()
        mock_response.read.return_value = b"not valid json"
        mock_response.__enter__ = lambda s: s
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response

        with pytest.raises(SearchError, match="Invalid response"):
            skill.execute("test query")


# ---------------------------------------------------------------------------
# SearchResult tests
# ---------------------------------------------------------------------------

class TestSearchResult:
    """Tests for SearchResult data class."""

    def test_to_dict(self) -> None:
        result = SearchResult(
            title="Test",
            url="https://example.com",
            snippet="A test result.",
            rank=1,
            metadata={"source": "test"},
        )

        d = result.to_dict()
        assert d["title"] == "Test"
        assert d["url"] == "https://example.com"
        assert d["snippet"] == "A test result."
        assert d["rank"] == 1
        assert d["metadata"] == {"source": "test"}

    def test_default_values(self) -> None:
        result = SearchResult(
            title="Test",
            url="https://example.com",
            snippet="A test result.",
        )

        assert result.rank == 0
        assert result.metadata == {}


# ---------------------------------------------------------------------------
# Initialization tests
# ---------------------------------------------------------------------------

class TestInitialization:
    """Tests for WebSearchSkill initialization."""

    def test_default_base_url(self) -> None:
        skill = WebSearchSkill()
        assert skill.base_url == WebSearchSkill.DEFAULT_BASE_URL

    def test_custom_base_url(self) -> None:
        skill = WebSearchSkill(base_url="https://custom.api.com/search")
        assert skill.base_url == "https://custom.api.com/search"

    def test_default_timeout(self) -> None:
        skill = WebSearchSkill()
        assert skill.timeout == 10

    def test_custom_timeout(self) -> None:
        skill = WebSearchSkill(timeout=30)
        assert skill.timeout == 30
