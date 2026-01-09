from __future__ import annotations

from typing import Any, Dict

from BE.schemas.chat import GeneratedResponse
from orchestrator.execution.llm import generate_answer
from orchestrator.execution.reranker import rerank
from orchestrator.execution.retriever import retrieve
from orchestrator.nodes.enrich_metadata import enrich_metadata
from orchestrator.nodes.validate_input import validate_input
from orchestrator.callbacks import OrchestratorCallbacks, build_default_callbacks


def _build_metadata(state: Dict[str, Any]) -> Dict[str, Any]:
    return enrich_metadata(state).get("metadata", {})


def run_orchestrator(
    state: Dict[str, Any],
    callbacks: OrchestratorCallbacks | None = None,
) -> GeneratedResponse:
    """비스트리밍 처리용 오케스트레이터 실행 함수입니다."""

    # 실행 시점마다 콜백을 통해 로깅/DB 저장을 위임합니다.
    callbacks = callbacks or build_default_callbacks()
    # 입력 검증 단계
    callbacks.on_step_start("validate", state)
    validate_input(state)
    callbacks.on_step_end("validate", state)
    # 문서 검색 단계
    callbacks.on_step_start("retrieve", state)
    docs = retrieve(state)
    callbacks.on_step_end("retrieve", state)
    # 재정렬 단계
    callbacks.on_step_start("rerank", state)
    ranked = rerank(docs)
    callbacks.on_step_end("rerank", state)
    # 답변 생성 단계
    callbacks.on_step_start("generate", state)
    answer = generate_answer(state.get("query", ""), ranked)
    callbacks.on_step_end("generate", state)
    metadata = _build_metadata(state)
    # 최종 결과 전달
    callbacks.on_final(answer, metadata, state)
    return GeneratedResponse(answer=answer, metadata=metadata)
