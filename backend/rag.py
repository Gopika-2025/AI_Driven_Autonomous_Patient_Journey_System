"""
rag.py

ROLE
----
Lightweight Retrieval-Augmented Generation (RAG) module.

PURPOSE
-------
- Store previously processed medical reports in memory
- Retrieve relevant past cases based on diagnosis
- Improve treatment plan consistency

NOTE
----
This is an in-memory RAG:
✔ Works perfectly on Streamlit Cloud
✔ No external database needed
✔ Resets automatically on app restart (acceptable for demo/project)
"""

from typing import List, Dict

# =====================================================
# IN-MEMORY KNOWLEDGE BASE
# =====================================================
_KNOWLEDGE_BASE: List[Dict[str, str]] = []


# =====================================================
# ADD REPORT TO RAG
# =====================================================
def add_to_rag(text: str, diagnosis: str) -> None:
    """
    Add extracted report text to the knowledge base.

    Args:
        text (str): Full extracted text from report
        diagnosis (str): Final diagnosis or inferred condition
    """

    if not text:
        return

    _KNOWLEDGE_BASE.append({
        "diagnosis": (diagnosis or "").lower(),
        "text": text[:3000]   # limit size for safety/performance
    })


# =====================================================
# QUERY RAG
# =====================================================
def query_rag(query: str, top_k: int = 3) -> List[str]:
    """
    Retrieve relevant report snippets based on diagnosis.

    Args:
        query (str): Diagnosis / condition to search for
        top_k (int): Number of similar reports to return

    Returns:
        List[str]: Relevant report text snippets
    """

    if not query:
        return []

    query = query.lower()
    matches = []

    for item in _KNOWLEDGE_BASE:
        if query in item["diagnosis"]:
            matches.append(item["text"])

    # Return most recent matches
    return matches[-top_k:]
