"""
Simple in-memory RAG (Retrieval-Augmented Generation) module.

Stores clinical documents and retrieves relevant context
based on a lightweight keyword-matching strategy.

This is intentionally simple and Streamlit-safe.
"""

import re

# =====================================================
# IN-MEMORY KNOWLEDGE STORE
# =====================================================
_RAG_STORE = []


# =====================================================
# ADD DOCUMENT TO RAG
# =====================================================
def add_to_rag(text: str) -> None:
    """
    Add a clinical document to the RAG knowledge base.
    """
    if text and text.strip():
        _RAG_STORE.append(text)


# =====================================================
# QUERY RAG
# =====================================================
def query_rag(query: str, top_k: int = 3) -> list:
    """
    Retrieve top-k relevant documents from RAG
    using simple keyword overlap scoring.

    Args:
        query (str): Search query (e.g., diagnosis)
        top_k (int): Number of documents to return

    Returns:
        list[str]: Relevant clinical context documents
    """

    if not _RAG_STORE or not query:
        return []

    query_tokens = set(
        re.findall(r"\b\w+\b", query.lower())
    )

    scored_docs = []

    for doc in _RAG_STORE:
        doc_tokens = set(
            re.findall(r"\b\w+\b", doc.lower())
        )
        score = len(query_tokens.intersection(doc_tokens))
        scored_docs.append((score, doc))

    # Sort by relevance score (descending)
    scored_docs.sort(key=lambda x: x[0], reverse=True)

    # Return top-k non-zero matches
    results = [
        doc for score, doc in scored_docs if score > 0
    ][:top_k]

    return results
