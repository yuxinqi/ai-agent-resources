#!/usr/bin/env python3
"""RAG Agent Demo.

A minimal demo that runs the RAG-agent workflow from the command line.

Usage:
    python demo.py "your question"
    python demo.py "What are the benefits of microservices?" --style detailed
    python demo.py "Explain RAG" --docs ./knowledge-base/
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
# In-memory vector store (for demo purposes)
# ---------------------------------------------------------------------------

class SimpleVectorStore:
    """A simple in-memory vector store using TF-IDF-like scoring.

    For production, replace with a proper vector database (Pinecone,
    Weaviate, ChromaDB, etc.).
    """

    def __init__(self) -> None:
        self.documents: list[dict[str, Any]] = []

    def add_documents(self, documents: list[dict[str, Any]]) -> None:
        """Add documents to the store."""
        for doc in documents:
            self.documents.append(doc)

    def search(self, query: str, top_k: int = 10, threshold: float = 0.1) -> list[dict[str, Any]]:
        """Search for documents matching the query.

        Uses a simple keyword overlap score. Not a real vector search.
        """
        query_terms = set(re.findall(r"\w+", query.lower()))

        scored: list[tuple[float, dict[str, Any]]] = []
        for doc in self.documents:
            content_terms = set(re.findall(r"\w+", doc.get("content", "").lower()))
            title_terms = set(re.findall(r"\w+", doc.get("title", "").lower()))
            all_terms = content_terms | title_terms

            if not all_terms:
                continue

            # Simple TF-IDF-like score
            overlap = query_terms & all_terms
            score = len(overlap) / math.sqrt(len(query_terms) * len(all_terms))

            if score >= threshold:
                scored.append((score, {**doc, "score": round(score, 4)}))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored[:top_k]]


# ---------------------------------------------------------------------------
# Workflow node implementations
# ---------------------------------------------------------------------------

def process_query(llm: LLMClient, query: str) -> tuple[list[str], str]:
    """Node: query_processor — optimize the query for retrieval."""
    system = (
        "You are a query processor for a RAG system. "
        "Output JSON with: original_query, processed_queries (list of 1-3 strings), "
        "query_type (factual|analytical|procedural|comparative)."
    )
    user = f"Process this query for retrieval: {query}"

    response = llm.chat(system, user)
    try:
        data = json.loads(response)
        return data.get("processed_queries", [query]), data.get("query_type", "factual")
    except json.JSONDecodeError:
        return [query], "factual"


def retrieve_documents(
    store: SimpleVectorStore,
    queries: list[str],
    top_k: int = 10,
) -> list[dict[str, Any]]:
    """Node: retriever — fetch documents from the vector store."""
    all_results: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    for query in queries:
        results = store.search(query, top_k=top_k)
        for result in results:
            doc_id = result.get("doc_id", "")
            if doc_id not in seen_ids:
                seen_ids.add(doc_id)
                all_results.append(result)

    return all_results


def rerank_documents(
    llm: LLMClient,
    query: str,
    query_type: str,
    documents: list[dict[str, Any]],
) -> tuple[list[str], list[str]]:
    """Node: reranker — rank documents by relevance."""
    if not documents:
        return [], []

    # For the demo, sort by score descending
    ranked = sorted(documents, key=lambda d: d.get("score", 0), reverse=True)

    # Use LLM to remove redundancies
    doc_summary = "\n".join(
        f"[{d['doc_id']}] (score: {d.get('score', 'N/A')}) {d.get('content', '')[:150]}"
        for d in ranked
    )

    system = "Output JSON with: ranked_doc_ids (list), removed_doc_ids (list)."
    user = f"Rerank for query '{query}' (type: {query_type}):\n{doc_summary}"

    response = llm.chat(system, user)
    try:
        data = json.loads(response)
        return data.get("ranked_doc_ids", [d["doc_id"] for d in ranked]), data.get("removed_doc_ids", [])
    except json.JSONDecodeError:
        return [d["doc_id"] for d in ranked], []


def generate_answer(
    llm: LLMClient,
    query: str,
    query_type: str,
    documents: list[dict[str, Any]],
    ranked_doc_ids: list[str],
    answer_style: str = "balanced",
) -> dict[str, Any]:
    """Node: generator — produce an answer from context documents."""
    context_docs = [d for d in documents if d.get("doc_id") in ranked_doc_ids]

    if not context_docs:
        return {
            "answer": "I could not find relevant information to answer your question.",
            "confidence": "insufficient",
            "sources_used": [],
            "gaps": ["No relevant documents found in the knowledge base."],
        }

    context_text = "\n\n".join(
        f"[{d['doc_id']}] {d.get('title', 'Untitled')}\n{d.get('content', '')}"
        for d in context_docs
    )

    system = (
        f"You are a RAG answer generator. Answer style: {answer_style}. "
        "Cite sources with [doc_id]. Output JSON with: answer, confidence, "
        "sources_used, gaps, reasoning."
    )
    user = f"Query: {query}\n\nContext:\n{context_text}"

    response = llm.chat(system, user)
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {
            "answer": response,
            "confidence": "medium",
            "sources_used": [d["doc_id"] for d in context_docs],
            "gaps": [],
        }


def verify_answer(
    llm: LLMClient,
    query: str,
    answer: dict[str, Any],
    documents: list[dict[str, Any]],
) -> dict[str, Any]:
    """Node: verifier — check faithfulness of the answer."""
    sources_used = answer.get("sources_used", [])
    source_docs = [d for d in documents if d.get("doc_id") in sources_used]

    source_text = "\n".join(
        f"[{d['doc_id']}]: {d.get('content', '')[:300]}"
        for d in source_docs
    )

    system = (
        "You are a faithfulness verifier. Output JSON with: is_faithful (bool), "
        "hallucinated_claims (list), unsupported_inferences (list), suggestions (list)."
    )
    user = (
        f"Query: {query}\n\nAnswer: {answer.get('answer', '')}\n\n"
        f"Sources:\n{source_text}"
    )

    response = llm.chat(system, user)
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {"is_faithful": True, "hallucinated_claims": [], "unsupported_inferences": [], "suggestions": []}


# ---------------------------------------------------------------------------
# Demo knowledge base
# ---------------------------------------------------------------------------

SAMPLE_DOCUMENTS = [
    {
        "doc_id": "rag-intro",
        "title": "Introduction to RAG",
        "content": (
            "Retrieval-Augmented Generation (RAG) is a technique that enhances "
            "language model outputs by retrieving relevant documents from a knowledge "
            "base before generating a response. RAG reduces hallucinations by grounding "
            "answers in retrieved evidence. Key components include a retriever, a "
            "reranker, and a generator."
        ),
    },
    {
        "doc_id": "rag-vs-finetuning",
        "title": "RAG vs Fine-tuning",
        "content": (
            "RAG is preferred over fine-tuning when knowledge changes frequently, as "
            "it allows updating the document store without retraining. Fine-tuning is "
            "better for adapting model behavior, tone, and domain-specific reasoning "
            "patterns. Hybrid approaches combining both show the best results in "
            "production systems."
        ),
    },
    {
        "doc_id": "rag-challenges",
        "title": "Challenges in RAG Systems",
        "content": (
            "Common challenges in RAG include: retrieval quality (irrelevant documents "
            "degrade answer quality), latency (retrieval adds overhead), chunk "
            "boundaries (splitting documents can lose context), and evaluation "
            "difficulty (measuring RAG quality requires faithfulness metrics). "
            "Reranking helps mitigate retrieval quality issues."
        ),
    },
    {
        "doc_id": "vector-search",
        "title": "Vector Search for RAG",
        "content": (
            "Vector search encodes documents and queries as dense vectors and finds "
            "similar documents using cosine similarity or approximate nearest neighbor "
            "algorithms. Popular vector databases include Pinecone, Weaviate, ChromaDB, "
            "and Milvus. Embedding models like text-embedding-3-small produce "
            "high-quality vectors for semantic search."
        ),
    },
]


# ---------------------------------------------------------------------------
# Main workflow runner
# ---------------------------------------------------------------------------

def run_workflow(
    query: str,
    answer_style: str = "balanced",
    doc_dir: Optional[str] = None,
) -> dict[str, Any]:
    """Run the complete RAG-agent workflow."""
    llm = LLMClient()

    # Build the document store
    store = SimpleVectorStore()
    if doc_dir and os.path.isdir(doc_dir):
        docs = _load_docs_from_dir(doc_dir)
        store.add_documents(docs)
    else:
        store.add_documents(SAMPLE_DOCUMENTS)

    print(f"=== RAG Agent: {query} ===\n")
    print(f"Knowledge base: {len(store.documents)} documents\n")

    # Step 1: Process query
    print("[1/5] Processing query...")
    queries, query_type = process_query(llm, query)
    print(f"       Type: {query_type}")
    print(f"       Processed queries: {queries}\n")

    # Step 2: Retrieve documents
    print("[2/5] Retrieving documents...")
    raw_docs = retrieve_documents(store, queries)
    print(f"       Found {len(raw_docs)} documents\n")

    # Step 3: Rerank
    print("[3/5] Reranking documents...")
    ranked_ids, removed_ids = rerank_documents(llm, query, query_type, raw_docs)
    print(f"       Kept {len(ranked_ids)}, removed {len(removed_ids)}\n")

    # Step 4: Generate answer
    print("[4/5] Generating answer...")
    answer = generate_answer(llm, query, query_type, raw_docs, ranked_ids, answer_style)
    print(f"       Confidence: {answer.get('confidence', 'unknown')}")
    print(f"       Sources: {answer.get('sources_used', [])}\n")

    # Step 5: Verify
    print("[5/5] Verifying answer...")
    verification = verify_answer(llm, query, answer, raw_docs)
    print(f"       Faithful: {verification.get('is_faithful', 'unknown')}\n")

    return {
        "query": query,
        "query_type": query_type,
        "answer": answer,
        "verification": verification,
    }


def _load_docs_from_dir(doc_dir: str) -> list[dict[str, Any]]:
    """Load .txt and .md files from a directory as documents."""
    docs: list[dict[str, Any]] = []
    path = os.path.abspath(doc_dir)

    for filename in os.listdir(path):
        if filename.endswith((".txt", ".md")):
            filepath = os.path.join(path, filename)
            with open(filepath, encoding="utf-8") as f:
                content = f.read()
            docs.append({
                "doc_id": filename.replace(".", "-"),
                "title": filename,
                "content": content,
            })

    return docs


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="RAG Agent Demo")
    parser.add_argument("query", help="Question to answer")
    parser.add_argument(
        "--style",
        default="balanced",
        choices=["concise", "balanced", "detailed"],
        help="Answer style",
    )
    parser.add_argument(
        "--docs",
        default=None,
        help="Directory with .txt/.md documents for the knowledge base",
    )
    args = parser.parse_args()

    result = run_workflow(args.query, answer_style=args.style, doc_dir=args.docs)
    print("\n=== Final Answer ===")
    print(result["answer"].get("answer", "No answer generated"))


if __name__ == "__main__":
    main()
