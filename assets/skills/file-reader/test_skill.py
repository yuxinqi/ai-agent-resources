"""Tests for FileReaderSkill."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

import pytest

from skill import FileContent, FileReaderSkill, FileReadError, SUPPORTED_EXTENSIONS


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def skill() -> FileReaderSkill:
    """Return a FileReaderSkill with default settings."""
    return FileReaderSkill()


@pytest.fixture
def tmp_dir() -> Path:
    """Create and return a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as d:
        yield Path(d)


def _write_file(directory: Path, name: str, content: str) -> Path:
    """Write content to a file and return the path."""
    path = directory / name
    path.write_text(content, encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Text file tests
# ---------------------------------------------------------------------------

class TestTextFiles:
    """Tests for reading .txt and .md files."""

    def test_read_txt_file(self, skill: FileReaderSkill, tmp_dir: Path) -> None:
        path = _write_file(tmp_dir, "hello.txt", "Hello, World!")
        result = skill.execute(str(path))

        assert isinstance(result, FileContent)
        assert result.format == "txt"
        assert result.content == "Hello, World!"
        assert result.size_bytes > 0

    def test_read_md_file(self, skill: FileReaderSkill, tmp_dir: Path) -> None:
        md_content = "# Title\n\nSome **bold** text.\n"
        path = _write_file(tmp_dir, "doc.md", md_content)
        result = skill.execute(str(path))

        assert result.format == "md"
        assert "# Title" in result.content
        assert "**bold**" in result.content

    def test_read_empty_txt_file(self, skill: FileReaderSkill, tmp_dir: Path) -> None:
        path = _write_file(tmp_dir, "empty.txt", "")
        result = skill.execute(str(path))

        assert result.content == ""
        assert result.size_bytes == 0


# ---------------------------------------------------------------------------
# JSON file tests
# ---------------------------------------------------------------------------

class TestJsonFiles:
    """Tests for reading .json files."""

    def test_read_json_object(self, skill: FileReaderSkill, tmp_dir: Path) -> None:
        data = {"name": "test", "value": 42}
        path = _write_file(tmp_dir, "data.json", json.dumps(data))
        result = skill.execute(str(path))

        assert result.format == "json"
        assert isinstance(result.content, dict)
        assert result.content["name"] == "test"
        assert result.content["value"] == 42

    def test_read_json_array(self, skill: FileReaderSkill, tmp_dir: Path) -> None:
        data = [1, 2, 3]
        path = _write_file(tmp_dir, "list.json", json.dumps(data))
        result = skill.execute(str(path))

        assert isinstance(result.content, list)
        assert result.content == [1, 2, 3]

    def test_read_nested_json(self, skill: FileReaderSkill, tmp_dir: Path) -> None:
        data = {"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]}
        path = _write_file(tmp_dir, "nested.json", json.dumps(data))
        result = skill.execute(str(path))

        assert result.content["users"][0]["name"] == "Alice"

    def test_invalid_json_raises_file_read_error(self, skill: FileReaderSkill, tmp_dir: Path) -> None:
        path = _write_file(tmp_dir, "bad.json", "{not valid json}")

        with pytest.raises(FileReadError, match="Failed to parse"):
            skill.execute(str(path))


# ---------------------------------------------------------------------------
# CSV file tests
# ---------------------------------------------------------------------------

class TestCsvFiles:
    """Tests for reading .csv files."""

    def test_read_csv_file(self, skill: FileReaderSkill, tmp_dir: Path) -> None:
        csv_content = "name,age,city\nAlice,30,NYC\nBob,25,LA\n"
        path = _write_file(tmp_dir, "people.csv", csv_content)
        result = skill.execute(str(path))

        assert result.format == "csv"
        assert isinstance(result.content, list)
        assert len(result.content) == 2
        assert result.content[0]["name"] == "Alice"
        assert result.content[0]["age"] == "30"
        assert result.content[1]["city"] == "LA"

    def test_read_csv_with_quotes(self, skill: FileReaderSkill, tmp_dir: Path) -> None:
        csv_content = 'name,desc\nAlice,"Has a, comma"\n'
        path = _write_file(tmp_dir, "quoted.csv", csv_content)
        result = skill.execute(str(path))

        assert result.content[0]["desc"] == "Has a, comma"

    def test_read_empty_csv(self, skill: FileReaderSkill, tmp_dir: Path) -> None:
        csv_content = "name,age\n"
        path = _write_file(tmp_dir, "empty_rows.csv", csv_content)
        result = skill.execute(str(path))

        assert isinstance(result.content, list)
        assert len(result.content) == 0


# ---------------------------------------------------------------------------
# Validation tests
# ---------------------------------------------------------------------------

class TestValidation:
    """Tests for file validation."""

    def test_file_not_found_raises_error(self, skill: FileReaderSkill) -> None:
        with pytest.raises(FileNotFoundError, match="File not found"):
            skill.execute("/nonexistent/file.txt")

    def test_unsupported_format_raises_value_error(self, skill: FileReaderSkill, tmp_dir: Path) -> None:
        path = _write_file(tmp_dir, "image.png", "fake binary data")

        with pytest.raises(ValueError, match="Unsupported file format"):
            skill.execute(str(path))

    def test_directory_raises_value_error(self, skill: FileReaderSkill, tmp_dir: Path) -> None:
        with pytest.raises(ValueError, match="Not a file"):
            skill.execute(str(tmp_dir))

    def test_file_too_large_raises_value_error(self, tmp_dir: Path) -> None:
        skill = FileReaderSkill(max_file_size=10)  # 10 bytes max
        path = _write_file(tmp_dir, "big.txt", "This is more than ten bytes long")

        with pytest.raises(ValueError, match="File too large"):
            skill.execute(str(path))


# ---------------------------------------------------------------------------
# Metadata tests
# ---------------------------------------------------------------------------

class TestMetadata:
    """Tests for file metadata extraction."""

    def test_metadata_includes_name_and_extension(self, skill: FileReaderSkill, tmp_dir: Path) -> None:
        path = _write_file(tmp_dir, "report.json", '{"key": "value"}')
        result = skill.execute(str(path))

        assert result.metadata["name"] == "report.json"
        assert result.metadata["extension"] == ".json"
        assert "modified" in result.metadata
        assert "size_bytes" in result.metadata

    def test_to_dict(self, skill: FileReaderSkill, tmp_dir: Path) -> None:
        path = _write_file(tmp_dir, "test.txt", "content")
        result = skill.execute(str(path))
        d = result.to_dict()

        assert "path" in d
        assert "format" in d
        assert "content" in d
        assert "metadata" in d
        assert "size_bytes" in d
