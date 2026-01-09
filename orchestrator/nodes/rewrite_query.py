from __future__ import annotations

from typing import Any, Dict


def rewrite_query(state: Dict[str, Any]) -> Dict[str, Any]:
    """사용자 질의를 재작성합니다."""

    query = state.get("query", "")
    rewritten = f"정제된 질의: {query}" if query else ""
    return {"rewritten_query": rewritten}
