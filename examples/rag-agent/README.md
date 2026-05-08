# RAG Agent Example

A complete minimal RAG (Retrieval-Augmented Generation) agent with document loading, in-memory vector store, and a query-retrieve-generate loop.

## What It Demonstrates

- **Document loading** from `.txt` and `.md` files
- **In-memory vector store** with TF-IDF-like scoring
- **Query-retrieve-generate** pipeline
- **Source attribution** in generated answers
- **Interactive mode** for multi-turn querying

## Quick Start

```bash
# Set your API key
export OPENAI_API_KEY="sk-..."

# Ask a single question (uses built-in demo knowledge base)
python main.py "What is RAG?"

# Use custom documents
python main.py "What is our refund policy?" --docs ./knowledge-base/

# Interactive mode
python main.py

# Different answer styles
python main.py "Explain RAG challenges" --style detailed
```

## Architecture

```
User Question
      │
      ▼
┌──────────────┐
│   Retriever  │  Search vector store for relevant documents
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Context    │  Build context from top-k documents with [doc_id] citations
│   Builder    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Generator   │  LLM generates answer grounded in context
│    (LLM)     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Response   │  Answer + confidence + source list
└──────────────┘
```

## Key Components

### InMemoryVectorStore

A simple vector store using TF-IDF-like keyword overlap scoring. Suitable for demos — replace with a real vector database for production.

```python
store = InMemoryVectorStore()
store.add_documents([Document(doc_id="1", title="Guide", content="...")])

results = store.search("how to deploy", top_k=5)
# Returns: [(Document, score), ...]
```

### RAGAgent

The main agent class that orchestrates retrieval and generation.

```python
agent = RAGAgent(store=store, llm=llm, top_k=5, answer_style="balanced")
result = agent.query("What is RAG?")
# Returns: {"answer": "...", "confidence": "high", "sources": ["rag-intro"]}
```

### Document Loading

Load documents from a directory of `.txt` and `.md` files:

```python
documents = load_documents_from_directory("./my-docs/")
```

Each file becomes a `Document` with:
- `doc_id` — derived from filename (stem)
- `title` — first `#` heading or filename
- `content` — full file text
- `source` — file path

## Demo Knowledge Base

The built-in demo includes 5 documents about RAG:

1. **Introduction to RAG** — Core concepts
2. **RAG System Components** — Architecture overview
3. **RAG vs Fine-tuning** — Comparison guide
4. **Vector Search for RAG** — Embedding and similarity
5. **Challenges in RAG Systems** — Pitfalls and solutions

## Customization

### Using a Real Vector Database

Replace `InMemoryVectorStore` with ChromaDB:

```python
import chromadb

client = chromadb.PersistentClient(path="./chroma-db")
collection = client.get_or_create_collection("documents")

# Ingest
for doc in documents:
    collection.add(ids=[doc.doc_id], documents=[doc.content], metadatas=[{"title": doc.title}])

# Search
results = collection.query(query_texts=["your question"], n_results=5)
```

### Using Real Embeddings

Replace the TF-IDF scoring with dense embeddings:

```python
from openai import OpenAI
client = OpenAI()

def get_embedding(text: str) -> list[float]:
    response = client.embeddings.create(input=text, model="text-embedding-3-small")
    return response.data[0].embedding
```

### Adding Chunking

For long documents, split into chunks before indexing:

```python
def chunk_document(doc: Document, chunk_size: int = 500, overlap: int = 50) -> list[Document]:
    chunks = []
    for i in range(0, len(doc.content), chunk_size - overlap):
        chunk = doc.content[i:i + chunk_size]
        chunks.append(Document(
            doc_id=f"{doc.doc_id}-chunk-{i}",
            title=doc.title,
            content=chunk,
            source=doc.source,
        ))
    return chunks
```

## Requirements

- Python 3.10+
- OpenAI API key
- No external pip packages required (uses stdlib only)
