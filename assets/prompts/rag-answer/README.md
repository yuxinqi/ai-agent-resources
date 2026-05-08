# RAG Answer Prompt

Answer a question using retrieved context documents with source attribution, confidence scoring, and explicit handling of insufficient information.

## Overview

This prompt is designed for Retrieval-Augmented Generation (RAG) pipelines. It ensures:

1. **Strict grounding** — Answers based only on provided context
2. **Source attribution** — Every claim cites a `[doc_id]` reference
3. **Confidence scoring** — Explicit rating of how well context supports the answer
4. **Gap identification** — Flags missing information rather than fabricating

## Parameters

| Parameter           | Type    | Required | Default   | Description                        |
|---------------------|---------|----------|-----------|------------------------------------|
| `question`          | string  | Yes      | —         | The user's question                |
| `context_documents` | array   | Yes      | —         | Retrieved documents to use         |
| `answer_style`      | string  | No       | "balanced"| concise / balanced / detailed       |
| `language`          | string  | No       | "en"      | ISO 639-1 language code            |

### Context Document Object

- `doc_id` (string) — Unique identifier for citation
- `content` (string) — The document chunk text
- `source` (string) — Origin (URL, file path, etc.)
- `relevance_score` (number, optional) — Retrieval score (0-1)

## Output Structure

- **answer** — The answer with `[doc_id]` inline citations
- **confidence** — high / medium / low / insufficient
- **sources_used** — List of doc_ids referenced in the answer
- **gaps** — Information needed but not found in context
- **reasoning** — Brief explanation of derivation

## Usage Example

```python
from jinja2 import Template
import yaml

with open("prompt.yaml") as f:
    prompt_config = yaml.safe_load(f)

data = {
    "question": "What is the return policy?",
    "context_documents": [
        {
            "doc_id": "faq-12",
            "content": "Returns are accepted within 30 days of purchase.",
            "source": "faq.html",
            "relevance_score": 0.92
        }
    ],
    "answer_style": "concise",
    "language": "en"
}

template = Template(prompt_config["user_prompt_template"])
rendered = template.render(**data)

# Use with your LLM
# response = llm.chat(
#     system=prompt_config["system_prompt"],
#     user=rendered
# )
```

## Test Cases

The `examples.jsonl` file contains 5 test cases covering:

1. Factual question with strong context — high confidence
2. Comparison question — medium confidence, balanced style
3. Question with insufficient context — should flag gaps
4. Medical question with rich context — detailed answer
5. Subjective question with weak context — low confidence

## Design Principles

- **Grounded**: Never uses knowledge outside the provided context
- **Honest about gaps**: Explicitly states when context is insufficient
- **Attributable**: Every claim traces to a specific document
- **Confidence-calibrated**: Ratings reflect actual evidence strength
