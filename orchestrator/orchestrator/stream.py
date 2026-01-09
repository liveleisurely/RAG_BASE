from __future__ import annotations

from typing import Any, AsyncGenerator, Awaitable, Callable, Dict, List

from orchestrator.callbacks import OrchestratorCallbacks, build_default_callbacks
from orchestrator.events import FinalEvent, StepEvent, TokenEvent
from orchestrator.execution.llm import stream_tokens
from orchestrator.execution.reranker import rerank
from orchestrator.execution.retriever import retrieve
from orchestrator.nodes.enrich_metadata import enrich_metadata
from orchestrator.nodes.validate_input import validate_input


async def orchestrator_stream(
    state: Dict[str, Any],
    is_disconnected: Callable[[], Awaitable[bool]],
    callbacks: OrchestratorCallbacks | None = None,
) -> AsyncGenerator[StepEvent | TokenEvent | FinalEvent, None]:
    """스트리밍 처리용 오케스트레이터 실행 함수입니다."""

    # 콜백을 통해 로깅/DB 저장 지점을 통합 관리합니다.
    callbacks = callbacks or build_default_callbacks()
    # 입력 검증 단계
    callbacks.on_step_start("validate", state)
    yield StepEvent(step="validate", status="start")
    validate_input(state)
    callbacks.on_step_end("validate", state)
    yield StepEvent(step="validate", status="done")

    if await is_disconnected():
        callbacks.on_interrupt(state)
        return

    # 문서 검색 단계
    callbacks.on_step_start("retrieve", state)
    yield StepEvent(step="retrieve", status="start")
    docs = retrieve(state)
    callbacks.on_step_end("retrieve", state)
    yield StepEvent(step="retrieve", status="done")

    if await is_disconnected():
        callbacks.on_interrupt(state)
        return

    # 재정렬 단계
    callbacks.on_step_start("rerank", state)
    yield StepEvent(step="rerank", status="start")
    ranked = rerank(docs)
    callbacks.on_step_end("rerank", state)
    yield StepEvent(step="rerank", status="done")

    if await is_disconnected():
        callbacks.on_interrupt(state)
        return

    metadata = enrich_metadata(state).get("metadata", {})
    # 답변 생성 단계 (토큰 스트리밍)
    yield StepEvent(step="generate", status="start")
    callbacks.on_step_start("generate", state)
    collected_tokens: List[str] = []
    async for token in stream_tokens(state.get("query", ""), ranked):
        if await is_disconnected():
            callbacks.on_interrupt(state)
            return
        collected_tokens.append(token)
        # 토큰 단위 이벤트 기록
        callbacks.on_token(token, state)
        yield TokenEvent(token=token)

    callbacks.on_step_end("generate", state)
    yield StepEvent(step="generate", status="done")
    final_answer = " ".join(collected_tokens)
    # 최종 응답 이벤트 기록
    callbacks.on_final(final_answer, metadata, state)
    yield FinalEvent(answer=final_answer, metadata=metadata)
