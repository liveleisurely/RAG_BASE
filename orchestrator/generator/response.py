from __future__ import annotations

from typing import Any, Dict

from BE.schemas.chat import GeneratedResponse


def generate_response(state: Dict[str, Any]) -> GeneratedResponse:
    """가장 단순한 형태의 응답 생성 로직입니다."""

    # 실제 구현에서는 LLM 호출 및 후처리를 수행합니다.
    answer = f"요청을 수신했습니다: {state.get('query', '')}"
    metadata = state.get("metadata", {})
    return GeneratedResponse(answer=answer, metadata=metadata)
