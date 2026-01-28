from __future__ import annotations

from typing import Any, AsyncGenerator, Awaitable, Callable, Dict

from langchain_core.callbacks import BaseCallbackHandler

from orchestrator.callbacks import (
    build_default_handlers,
    StreamInterruptedError,
    notify_stream_interrupted,
    notify_token,
)
from orchestrator.events import FinalEvent, StepEvent, TokenEvent
from orchestrator.nodes.enrich_metadata import enrich_metadata
from orchestrator.orchestrator.graph import build_graph


async def orchestrator_stream(
    state: Dict[str, Any],
    is_disconnected: Callable[[], Awaitable[bool]],
    handlers: list[BaseCallbackHandler] | None = None,
) -> AsyncGenerator[StepEvent | TokenEvent | FinalEvent, None]:
    """스트리밍 처리용 오케스트레이터 실행 함수입니다."""

    # 콜백을 통해 로깅/DB 저장 지점을 통합 관리합니다.
    handlers = handlers or build_default_handlers()
    graph = build_graph()
    metadata = enrich_metadata(state).get("metadata", {})
    final_answer = ""

    try:
        async for event in graph.astream_events(state, config={"callbacks": handlers}, version="v1"):
            if await is_disconnected():
                raise StreamInterruptedError("streaming interrupted")

            event_type = event.get("event")
            name = event.get("name") or event.get("data", {}).get("name", "unknown")
            if event_type == "on_chain_start":
                yield StepEvent(step=name, status="start")
                continue
            if event_type == "on_chain_end":
                output = event.get("data", {}).get("output") or event.get("data", {}).get("outputs")
                if isinstance(output, dict) and "answer" in output:
                    final_answer = output["answer"]
                yield StepEvent(step=name, status="done")
                continue
            if event_type == "on_chain_error":
                error = event.get("data", {}).get("error")
                yield StepEvent(step=name, status="error", detail={"error": str(error)})
                continue
            if event_type in {"on_llm_new_token", "on_chat_model_stream"}:
                data = event.get("data", {})
                token = data.get("token") or data.get("text") or data.get("chunk")
                if isinstance(token, dict):
                    token = token.get("content", "")
                if token:
                    notify_token(handlers, str(token), state)
                    yield TokenEvent(token=str(token))
    except StreamInterruptedError:
        notify_stream_interrupted(handlers, state)
        return

    yield FinalEvent(answer=final_answer, metadata=metadata)
