from __future__ import annotations

from typing import Any, Dict, List

from orchestrator.execution.llm import search_documents as llm_search_documents


def search_documents(state: Dict[str, Any]) -> Dict[str, Any]:
    """문서 검색을 수행하는 노드입니다."""

    source = state.get("source", "default")
    query = state.get("rewritten_query") or state.get("query", "")
    # 실제 구현에서는 LLM 호출 또는 검색 시스템 호출을 통해 문서를 조회합니다.
    docs: List[str] = llm_search_documents(query, source)
    return {"documents": docs}
