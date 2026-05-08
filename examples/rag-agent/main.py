#!/usr/bin/env python3
"""RAG Agent Example.

A complete minimal RAG (Retrieval-Augmented Generation) agent with:
- Document loading from .txt/.md files
- In-memory vector store with TF-IDF-like scoring
- Query-retrieve-generate loop
- Source attribution in answers

Usage:
    python main.py "What is RAG?"
    python main.py "How does vector search work?" --docs ./my-docs/
    python main.py "Explain the challenges" --style detailed

Requires:
    export OPENAI_API_KEY="sk-..."
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional


# ---------------------------------------------------------------------------
# Document and vector store
# ---------------------------------------------------------------------------

@dataclass
class Document:
    """A document chunk with metadata."""

    doc_id: str
    title: str
    content: str
    source: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


class InMemoryVectorStore:
    """Simple in-memory vector store using keyword overlap scoring.

    For production, replace with a proper vector database (ChromaDB,
    Pinecone, Weaviate, Milvus, etc.) with real embeddings.

    This implementation uses TF-IDF-like scoring based on term overlap,
    which is sufficient for demonstration but not for production use.
    """

    def __init__(self) -> None:
        self.documents: list[Document] = []
        self._term_index: dict[str, set[int]] = {}  # term -> set of doc indices
        self._idf: dict[str, float] = {}

    def add_documents(self, documents: list[Document]) -> None:
        """Add documents to the store and update the term index."""
        start_idx = len(self.documents)
        self.documents.extend(documents)

        for i, doc in enumerate(documents):
            idx = start_idx + i
            terms = self._tokenize(f"{doc.title} {doc.content}")
            for term in terms:
                if term not in self._term_index:
                    self._term_index[term] = set()
                self._term_index[term].add(idx)

        # Recompute IDF
        n = len(self.documents)
        self._idf = {
            term: math.log((n + 1) / (len(doc_ids) + 1)) + 1
            for term, doc_ids in self._term_index.items()
        }

    def search(
        self,
        query: str,
        top_k: int = 5,
        threshold: float = 0.05,
    ) -> list[tuple[Document, float]]:
        """Search for documents matching the query.

        Args:
            query: The search query.
            top_k: Maximum number of results.
            threshold: Minimum relevance score.

        Returns:
            List of (document, score) tuples, sorted by score descending.
        """
        query_terms = self._tokenize(query)
        if not query_terms:
            return []

        # Score each document
        scores: dict[int, float] = {}
        for term in query_terms:
            if term not in self._term_index:
                continue
            idf = self._idf.get(term, 1.0)
            for doc_idx in self._term_index[term]:
                doc = self.documents[doc_idx]
                doc_terms = self._tokenize(f"{doc.title} {doc.content}")
                tf = doc_terms.count(term) / max(len(doc_terms), 1)
                scores[doc_idx] = scores.get(doc_idx, 0) + tf * idf

        # Sort by score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        results: list[tuple[Document, float]] = []
        for doc_idx, score in ranked[:top_k]:
            if score >= threshold:
                results.append((self.documents[doc_idx], round(score, 4)))

        return results

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        """Simple tokenization: lowercase, split on non-word chars."""
        return re.findall(r"\w+", text.lower())


# ---------------------------------------------------------------------------
# Document loader
# ---------------------------------------------------------------------------

def load_documents_from_directory(directory: str) -> list[Document]:
    """Load .txt and .md files from a directory into Document objects.

    Args:
        directory: Path to the directory containing documents.

    Returns:
        List of Document objects.

    Raises:
        FileNotFoundError: If the directory does not exist.
    """
    path = Path(directory)
    if not path.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    documents: list[Document] = []
    for filepath in sorted(path.rglob("*")):
        if filepath.suffix.lower() not in (".txt", ".md"):
            continue
        if not filepath.is_file():
            continue

        try:
            content = filepath.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print(f"Warning: skipping {filepath} (encoding error)")
            continue

        # Use the first line as title if it starts with #
        lines = content.strip().split("\n")
        title = filepath.stem.replace("-", " ").replace("_", " ").title()
        if lines and lines[0].startswith("#"):
            title = lines[0].lstrip("# ").strip()

        doc = Document(
            doc_id=filepath.stem,
            title=title,
            content=content,
            source=str(filepath),
        )
        documents.append(doc)

    return documents


def create_default_documents() -> list[Document]:
    """Create default sample documents for the demo."""
    return [
        Document(
            doc_id="rag-intro",
            title="Introduction to RAG",
            content=(
                "Retrieval-Augmented Generation (RAG) is a technique that enhances "
                "language model outputs by retrieving relevant documents from a knowledge "
                "base before generating a response. RAG reduces hallucinations by grounding "
                "answers in retrieved evidence. The core pipeline consists of three steps: "
                "query processing, document retrieval, and answer generation."
            ),
        ),
        Document(
            doc_id="rag-components",
            title="RAG System Components",
            content=(
                "A RAG system has four main components: (1) Query Processor — optimizes "
                "the user query for retrieval, handles ambiguity and multi-part questions. "
                "(2) Retriever — finds relevant documents using vector similarity search. "
                "(3) Reranker — re-sorts results by relevance and removes duplicates. "
                "(4) Generator — produces the final answer using the retrieved context."
            ),
        ),
        Document(
            doc_id="rag-vs-finetuning",
            title="RAG vs Fine-tuning",
            content=(
                "RAG is preferred when knowledge changes frequently, as updating the "
                "document store is cheaper than retraining. Fine-tuning is better for "
                "adapting model behavior, style, and domain reasoning. Hybrid approaches "
                "that combine RAG with fine-tuning achieve the best results. RAG excels "
                "at factual accuracy while fine-tuning excels at task performance."
            ),
        ),
        Document(
            doc_id="vector-search",
            title="Vector Search for RAG",
            content=(
                "Vector search encodes documents and queries as dense vectors using "
                "embedding models. Similarity is computed using cosine similarity or "
                "dot product. Popular vector databases include ChromaDB, Pinecone, "
                "Weaviate, and Milvus. Embedding models like text-embedding-3-small "
                "produce 1536-dimensional vectors optimized for semantic search."
            ),
        ),
        Document(
            doc_id="rag-challenges",
            title="Challenges in RAG Systems",
            content=(
                "Key challenges include: (1) Retrieval quality — irrelevant documents "
                "degrade answer quality. (2) Chunk boundaries — splitting documents can "
                "lose context across chunks. (3) Latency — retrieval adds overhead to "
                "each query. (4) Evaluation — measuring RAG quality requires faithfulness "
                "and relevance metrics. Reranking and query expansion help mitigate "
                "retrieval quality issues."
            ),
        ),
    ]


# ---------------------------------------------------------------------------
# LLM client
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
        """Send a chat completion request."""
        url = f"{self.base_url}/chat/completions"
        payload = json.dumps({
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0.2,
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
# RAG Agent
# ---------------------------------------------------------------------------

class RAGAgent:
    """A minimal RAG agent with query-retrieve-generate loop.

    Args:
        store: The vector store to retrieve documents from.
        llm: The LLM client for generation.
        top_k: Number of documents to retrieve.
        answer_style: concise, balanced, or detailed.
    """

    def __init__(
        self,
        store: InMemoryVectorStore,
        llm: LLMClient,
        top_k: int = 5,
        answer_style: str = "balanced",
    ) -> None:
        self.store = store
        self.llm = llm
        self.top_k = top_k
        self.answer_style = answer_style

    def query(self, question: str) -> dict[str, Any]:
        """Answer a question using RAG.

        Args:
            question: The user's question.

        Returns:
            A dictionary with answer, sources, and confidence.
        """
        # Step 1: Retrieve relevant documents
        search_results = self.store.search(question, top_k=self.top_k)

        if not search_results:
            return {
                "answer": "I couldn't find any relevant information in the knowledge base to answer your question.",
                "confidence": "insufficient",
                "sources": [],
            }

        # Step 2: Build context from retrieved documents
        context_parts: list[str] = []
        source_ids: list[str] = []

        for doc, score in search_results:
            context_parts.append(f"[{doc.doc_id}] {doc.title}\n{doc.content}")
            source_ids.append(doc.doc_id)

        context = "\n\n".join(context_parts)

        # Step 3: Generate answer using LLM
        system_prompt = (
            f"You are a RAG assistant. Answer the question using ONLY the "
            f"provided context documents. Answer style: {self.answer_style}. "
            f"Cite sources using [doc_id] references. If the context is "
            f"insufficient, say so explicitly."
        )

        user_prompt = f"Question: {question}\n\nContext:\n{context}"

        answer_text = self.llm.chat(system_prompt, user_prompt)

        # Step 4: Determine confidence
        confidence = self._estimate_confidence(search_results, answer_text)

        return {
            "answer": answer_text,
            "confidence": confidence,
            "sources": source_ids,
        }

    @staticmethod
    def _estimate_confidence(
        search_results: list[tuple[Document, float]],
        answer: str,
    ) -> str:
        """Estimate answer confidence based on retrieval scores."""
        if not search_results:
            return "insufficient"

        top_score = search_results[0][1]
        if top_score >= 0.5:
            return "high"
        elif top_score >= 0.2:
            return "medium"
        else:
            return "low"


# ---------------------------------------------------------------------------
# Interactive loop
# ---------------------------------------------------------------------------

def interactive_mode(agent: RAGAgent) -> None:
    """Run an interactive query loop."""
    print("RAG Agent Interactive Mode")
    print("Type your question or 'quit' to exit.\n")

    while True:
        try:
            question = input("Question: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not question or question.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        result = agent.query(question)

        print(f"\nAnswer (confidence: {result['confidence']}):")
        print(result["answer"])
        print(f"\nSources: {', '.join(result['sources'])}")
        print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description="RAG Agent Example")
    parser.add_argument("question", nargs="?", help="Question to ask (omit for interactive mode)")
    parser.add_argument("--docs", default=None, help="Directory with .txt/.md documents")
    parser.add_argument(
        "--style",
        default="balanced",
        choices=["concise", "balanced", "detailed"],
        help="Answer style",
    )
    parser.add_argument("--top-k", type=int, default=5, help="Number of documents to retrieve")
    args = parser.parse_args()

    # Load documents
    if args.docs:
        print(f"Loading documents from {args.docs}...")
        documents = load_documents_from_directory(args.docs)
    else:
        print("Using built-in demo knowledge base...")
        documents = create_default_documents()

    print(f"Loaded {len(documents)} documents.")

    # Build vector store
    store = InMemoryVectorStore()
    store.add_documents(documents)

    # Create agent
    llm = LLMClient()
    agent = RAGAgent(store=store, llm=llm, top_k=args.top_k, answer_style=args.style)

    # Run
    if args.question:
        result = agent.query(args.question)
        print(f"\nAnswer (confidence: {result['confidence']}):")
        print(result["answer"])
        print(f"\nSources: {', '.join(result['sources'])}")
    else:
        interactive_mode(agent)


if __name__ == "__main__":
    main()
