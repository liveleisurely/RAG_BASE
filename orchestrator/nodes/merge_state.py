from __future__ import annotations

from typing import Any, Dict


def merge_state(state: Dict[str, Any]) -> Dict[str, Any]:
    """병렬 노드 결과를 병합합니다."""

    merged = {
        "validation": state.get("validation", {}),
        "metadata": state.get("metadata", {}),
    }
    return merged
