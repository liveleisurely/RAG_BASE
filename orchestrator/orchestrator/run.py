from __future__ import annotations

from typing import Any, Dict

from BE.schemas.chat import GeneratedResponse
from orchestrator.nodes.enrich_metadata import enrich_metadata
from langchain_core.callbacks import BaseCallbackHandler

from orchestrator.callbacks import (
    build_default_handlers,
)
from orchestrator.orchestrator.graph import build_graph


def _build_metadata(state: Dict[str, Any]) -> Dict[str, Any]:
    return enrich_metadata(state).get("metadata", {})


def run_orchestrator(
    state: Dict[str, Any],
    handlers: list[BaseCallbackHandler] | None = None,
) -> GeneratedResponse:
    """비스트리밍 처리용 오케스트레이터 실행 함수입니다."""

    # 실행 시점마다 콜백을 통해 로깅/DB 저장을 위임합니다.
    handlers = handlers or build_default_handlers()
    graph = build_graph()
    result = graph.invoke(state, config={"callbacks": handlers})
    metadata = _build_metadata(state)
    return GeneratedResponse(
        answer=result.get("answer", ""),
        metadata=metadata,
    )
