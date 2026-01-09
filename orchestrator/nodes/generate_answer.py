from __future__ import annotations

from typing import Any, Dict, List


def generate_answer(state: Dict[str, Any]) -> Dict[str, Any]:
    """검색 결과를 바탕으로 응답을 생성합니다."""

    query = state.get("query", "")
    documents: List[str] = state.get("documents", [])
    context = " ".join(documents)
    answer = f"응답: {query} | 근거: {context}"
    return {"answer": answer}
