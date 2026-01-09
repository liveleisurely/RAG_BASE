from __future__ import annotations

from typing import Any, Dict


def enrich_metadata(state: Dict[str, Any]) -> Dict[str, Any]:
    """기본 메타데이터를 확장합니다."""

    metadata = {
        "request_id": state.get("request_id"),
        "chat_id": state.get("chat_id"),
        "user_id": (state.get("user") or {}).get("user_id"),
    }
    return {"metadata": metadata}
