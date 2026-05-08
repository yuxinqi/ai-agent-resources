# RAG Agent Workflow

A Retrieval-Augmented Generation workflow that processes a query through retrieval, reranking, generation, and verification stages.

## Workflow Architecture

```
query_processor → retriever → reranker → generator → verifier
```

### Nodes

| Node              | Type   | Description                                        |
|-------------------|--------|----------------------------------------------------|
| `query_processor` | LLM    | Optimize and expand the query for retrieval        |
| `retriever`       | Skill  | Fetch relevant documents from the vector store     |
| `reranker`        | LLM    | Re-rank by relevance, remove duplicates            |
| `generator`       | LLM    | Generate answer with citations from context        |
| `verifier`        | LLM    | Check answer faithfulness to source documents      |

## Quick Start

```bash
# Set your OpenAI API key
export OPENAI_API_KEY="sk-..."

# Run with built-in demo knowledge base
python demo.py "What is RAG?"
python demo.py "RAG vs fine-tuning" --style detailed

# Run with custom documents
python demo.py "Explain our refund policy" --docs ./knowledge-base/
```

## Workflow Inputs

| Parameter             | Type    | Required | Default    | Description              |
|-----------------------|---------|----------|------------|--------------------------|
| `query`               | string  | Yes      | —          | The user's question      |
| `conversation_history`| array   | No       | []         | Previous messages        |
| `answer_style`        | string  | No       | "balanced" | concise / balanced / detailed |

## Workflow Outputs

| Output          | Type   | Description                      |
|-----------------|--------|----------------------------------|
| `answer`        | string | The generated answer with citations |
| `confidence`    | string | high / medium / low / insufficient |
| `sources_used`  | list   | Document IDs referenced          |
| `verification`  | dict   | Faithfulness verification results|

### Verification Structure

```json
{
  "is_faithful": true,
  "hallucinated_claims": [],
  "unsupported_inferences": [],
  "suggestions": []
}
```

## Demo Knowledge Base

The demo includes 4 sample documents about RAG systems:

1. **Introduction to RAG** — Core concepts and components
2. **RAG vs Fine-tuning** — When to use each approach
3. **Challenges in RAG Systems** — Common pitfalls and solutions
4. **Vector Search for RAG** — Embedding and similarity search

Load your own documents with `--docs ./path/` (reads `.txt` and `.md` files).

## Customization

### Using a Real Vector Database

Replace `SimpleVectorStore` in `demo.py`:

```python
import chromadb

def retrieve_documents(queries, top_k=10):
    client = chromadb.PersistentClient(path="./chroma-db")
    collection = client.get_collection("documents")
    results = collection.query(query_texts=queries, n_results=top_k)
    return results
```

### Adding a Reranking Model

Use a cross-encoder for more accurate reranking:

```python
from sentence_transformers import CrossEncoder
model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
scores = model.predict([(query, doc["content"]) for doc in documents])
```

## Requirements

- Python 3.10+
- OpenAI API key (for LLM calls)
- Optional: `openai`, `chromadb`, `sentence-transformers` (see requirements.txt)
