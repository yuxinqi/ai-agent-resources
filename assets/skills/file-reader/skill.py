"""File Reader Skill for AI agents.

Provides a FileReaderSkill class that reads and parses files in
common formats (txt, md, json, csv) with encoding detection and
structured output.
"""

from __future__ import annotations

import csv
import io
import json
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional, Union

logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = {".txt", ".md", ".json", ".csv"}


@dataclass
class FileContent:
    """Structured content read from a file."""

    path: str
    format: str
    content: Union[str, list[dict[str, Any]], dict[str, Any]]
    metadata: dict[str, Any] = field(default_factory=dict)
    size_bytes: int = 0

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "path": self.path,
            "format": self.format,
            "content": self.content,
            "metadata": self.metadata,
            "size_bytes": self.size_bytes,
        }


class FileReaderSkill:
    """File reader skill that reads and parses common file formats.

    Supports:
    - `.txt` / `.md` — Plain text and Markdown files
    - `.json` — JSON files (parsed into Python objects)
    - `.csv` — CSV files (parsed into list of row dicts)

    Args:
        encoding: File encoding to use (default: utf-8).
        max_file_size: Maximum file size in bytes (default: 10 MB).

    Example:
        >>> skill = FileReaderSkill()
        >>> result = skill.execute("data/report.json")
        >>> print(result.format)  # "json"
        >>> print(result.content)  # Parsed JSON object
    """

    DEFAULT_ENCODING = "utf-8"
    DEFAULT_MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

    def __init__(
        self,
        encoding: str = DEFAULT_ENCODING,
        max_file_size: int = DEFAULT_MAX_FILE_SIZE,
    ) -> None:
        self.encoding = encoding
        self.max_file_size = max_file_size

    def execute(self, file_path: str) -> FileContent:
        """Read and parse a file.

        Args:
            file_path: Path to the file to read.

        Returns:
            A FileContent object with the parsed file content.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file format is not supported or file is too large.
            FileReadError: If the file cannot be parsed.
        """
        path = Path(file_path)
        self._validate_file(path)

        ext = path.suffix.lower()
        file_size = path.stat().st_size

        logger.info("Reading file: %s (format=%s, size=%d)", path, ext, file_size)

        try:
            if ext in (".txt", ".md"):
                content = self._read_text(path)
            elif ext == ".json":
                content = self._read_json(path)
            elif ext == ".csv":
                content = self._read_csv(path)
            else:
                raise ValueError(f"Unsupported file format: {ext}")
        except (json.JSONDecodeError, csv.Error) as exc:
            raise FileReadError(f"Failed to parse {path}: {exc}") from exc
        except UnicodeDecodeError as exc:
            raise FileReadError(f"Encoding error reading {path}: {exc}") from exc

        return FileContent(
            path=str(path),
            format=ext.lstrip("."),
            content=content,
            metadata=self._extract_metadata(path),
            size_bytes=file_size,
        )

    def _validate_file(self, path: Path) -> None:
        """Validate that the file exists, is readable, and format is supported."""
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        if not path.is_file():
            raise ValueError(f"Not a file: {path}")

        ext = path.suffix.lower()
        if ext not in SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file format: {ext}. "
                f"Supported formats: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
            )

        file_size = path.stat().st_size
        if file_size > self.max_file_size:
            raise ValueError(
                f"File too large: {file_size} bytes "
                f"(max: {self.max_file_size} bytes)"
            )

    def _read_text(self, path: Path) -> str:
        """Read a text or markdown file."""
        return path.read_text(encoding=self.encoding)

    def _read_json(self, path: Path) -> Union[dict[str, Any], list[Any]]:
        """Read and parse a JSON file."""
        text = path.read_text(encoding=self.encoding)
        return json.loads(text)

    def _read_csv(self, path: Path) -> list[dict[str, str]]:
        """Read and parse a CSV file into a list of row dictionaries."""
        text = path.read_text(encoding=self.encoding)
        reader = csv.DictReader(io.StringIO(text))
        return list(reader)

    def _extract_metadata(self, path: Path) -> dict[str, Any]:
        """Extract file metadata."""
        stat = path.stat()
        return {
            "name": path.name,
            "extension": path.suffix.lower(),
            "modified": stat.st_mtime,
            "size_bytes": stat.st_size,
        }


class FileReadError(Exception):
    """Raised when a file cannot be read or parsed."""

    pass
