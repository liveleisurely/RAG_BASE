from __future__ import annotations

import json
from typing import AsyncGenerator

from orchestrator.events import FinalEvent, StepEvent, TokenEvent


async def stream_response(
    events: AsyncGenerator[StepEvent | TokenEvent | FinalEvent, None],
) -> AsyncGenerator[str, None]:
    """이벤트를 SSE 포맷으로 변환하는 어댑터입니다."""

    # 오케스트레이터 이벤트를 HTTP SSE 규격으로 변환해 전달합니다.
    async for event in events:
        payload = json.dumps(event.to_payload(), ensure_ascii=False)
        yield f"data: {payload}\n\n"
