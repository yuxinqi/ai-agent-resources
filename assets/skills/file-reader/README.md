# File Reader Skill

A file reader skill for AI agents that reads and parses files in common formats (txt, md, json, csv) with encoding detection and structured output.

## Installation

No external dependencies beyond the Python standard library.

```bash
# No pip install needed — uses only stdlib (csv, json, io, pathlib, logging)
```

## Quick Start

```python
from skill import FileReaderSkill

skill = FileReaderSkill()

# Read a text file
result = skill.execute("notes.txt")
print(result.content)  # "Hello, World!"

# Read a JSON file
result = skill.execute("data/config.json")
print(result.content)  # {'key': 'value'} (parsed dict)

# Read a CSV file
result = skill.execute("data/users.csv")
for row in result.content:
    print(row["name"], row["email"])
```

## Supported Formats

| Format | Extension | Output Type                      |
|--------|-----------|----------------------------------|
| Text   | `.txt`    | `str`                            |
| Markdown | `.md`  | `str`                            |
| JSON   | `.json`   | `dict` or `list` (parsed)        |
| CSV    | `.csv`    | `list[dict[str, str]]` (rows)    |

## API Reference

### `FileReaderSkill`

```python
FileReaderSkill(
    encoding: str = "utf-8",
    max_file_size: int = 10_485_760,  # 10 MB
)
```

| Parameter       | Type  | Default   | Description              |
|-----------------|-------|-----------|--------------------------|
| `encoding`      | `str` | `"utf-8"` | File encoding to use     |
| `max_file_size` | `int` | `10485760`| Max file size in bytes   |

#### `execute(file_path)`

Read and parse a file.

```python
result: FileContent = skill.execute("data/report.json")
```

- **file_path** (`str`) — Path to the file.
- **Returns** — `FileContent` with parsed content.
- **Raises**:
  - `FileNotFoundError` — File does not exist.
  - `ValueError` — Unsupported format or file too large.
  - `FileReadError` — Parse or encoding error.

### `FileContent`

| Field        | Type                | Description           |
|--------------|---------------------|-----------------------|
| `path`       | `str`               | File path             |
| `format`     | `str`               | File format (txt, md, json, csv) |
| `content`    | `str \| dict \| list` | Parsed file content |
| `metadata`   | `dict`              | File metadata (name, extension, modified, size_bytes) |
| `size_bytes` | `int`               | File size in bytes    |

#### `to_dict()`

Convert to a plain dictionary.

## Running Tests

```bash
cd assets/skills/file-reader
python -m pytest test_skill.py -v
```

## Error Handling

| Error Type         | When                                      |
|--------------------|-------------------------------------------|
| `FileNotFoundError`| File does not exist                       |
| `ValueError`       | Unsupported format, not a file, or too large |
| `FileReadError`    | Parse failure (invalid JSON/CSV) or encoding error |
