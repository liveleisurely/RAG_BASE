from __future__ import annotations

from typing import Any, Dict, List


def search_documents(state: Dict[str, Any]) -> Dict[str, Any]:
    """문서 검색을 수행하는 노드입니다."""

    source = state.get("source", "default")
    query = state.get("rewritten_query") or state.get("query", "")
    docs: List[str] = [f"{source} 검색 결과: {query}"]
    return {"documents": docs}
