from __future__ import annotations

from typing import Any, Dict


def validate_input(state: Dict[str, Any]) -> Dict[str, Any]:
    """입력 값을 검증하고 기본 메타데이터를 반환합니다."""

    if not state.get("query"):
        raise ValueError("query는 필수 값입니다.")
    if not state.get("user"):
        raise ValueError("user는 필수 값입니다.")

    validation = {
        "has_query": bool(state.get("query")),
        "has_user": bool(state.get("user")),
    }
    return {"validation": validation}
