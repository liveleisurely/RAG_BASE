from __future__ import annotations

from typing import Any, Dict, Iterable, List
from uuid import UUID

from langchain_core.callbacks import BaseCallbackHandler

from orchestrator import persistence


class StreamInterruptedError(RuntimeError):
    """클라이언트 연결 종료 등으로 스트리밍이 중단되었음을 나타냅니다."""


class PersistenceCallbackHandler(BaseCallbackHandler):
    """LangChain 콜백을 사용해 오케스트레이터 스텝 기록을 위임합니다."""

    def on_chain_start(  # type: ignore[override]
        self,
        serialized: Dict[str, Any],
        inputs: Dict[str, Any],
        run_id: UUID,
        **kwargs: Any,
    ) -> None:
        step = serialized.get("name", "unknown")
        persistence.log_step_start(step, inputs.get("state", {}))

    def on_chain_end(  # type: ignore[override]
        self,
        outputs: Dict[str, Any],
        run_id: UUID,
        **kwargs: Any,
    ) -> None:
        step = outputs.get("name", "unknown")
        persistence.log_step_end(step, outputs.get("state", {}))

    def on_chain_error(  # type: ignore[override]
        self,
        error: BaseException,
        run_id: UUID,
        **kwargs: Any,
    ) -> None:
        step = kwargs.get("name", "unknown")
        state = kwargs.get("state", {})
        persistence.log_step_error(step, error, state)

    def on_llm_new_token(  # type: ignore[override]
        self,
        token: str,
        **kwargs: Any,
    ) -> None:
        state = kwargs.get("state", {})
        persistence.log_token(token, state)

def build_default_handlers() -> List[BaseCallbackHandler]:
    """기본 콜백 핸들러 리스트를 구성합니다."""

    return [PersistenceCallbackHandler()]


def notify_token(
    handlers: Iterable[BaseCallbackHandler],
    token: str,
    state: Dict[str, Any],
) -> None:
    for handler in handlers:
        handler.on_llm_new_token(  # type: ignore[call-arg]
            token=token,
            state=state,
        )


def notify_stream_interrupted(
    handlers: Iterable[BaseCallbackHandler],
    state: Dict[str, Any],
) -> None:
    for handler in handlers:
        handler.on_chain_error(  # type: ignore[call-arg]
            error=StreamInterruptedError("streaming interrupted"),
            run_id=UUID(int=0),
            name="streaming",
            state=state,
        )
    persistence.log_stream_interrupted(state)
