from __future__ import annotations

from typing import Any, Dict, List


def retrieve(state: Dict[str, Any]) -> List[str]:
    """검색 결과를 반환하는 순수 함수입니다."""

    query = state.get("query", "")
    return [f"문서 후보: {query}"]
