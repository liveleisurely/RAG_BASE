from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from orchestrator import persistence


@dataclass
class OrchestratorCallbacks:
    """오케스트레이터 실행 중 호출되는 훅을 묶은 구조입니다."""

    def on_step_start(self, step: str, state: Dict[str, Any]) -> None:
        return None

    def on_step_end(self, step: str, state: Dict[str, Any]) -> None:
        return None

    def on_token(self, token: str, state: Dict[str, Any]) -> None:
        return None

    def on_final(self, answer: str, metadata: Dict[str, Any], state: Dict[str, Any]) -> None:
        return None

    def on_interrupt(self, state: Dict[str, Any]) -> None:
        return None


class PersistenceCallbacks(OrchestratorCallbacks):
    """DB/로깅 연동을 위한 기본 콜백 구현입니다."""

    def on_step_start(self, step: str, state: Dict[str, Any]) -> None:
        persistence.log_step_start(step, state)

    def on_step_end(self, step: str, state: Dict[str, Any]) -> None:
        persistence.log_step_end(step, state)

    def on_interrupt(self, state: Dict[str, Any]) -> None:
        persistence.log_stream_interrupted(state)


def build_default_callbacks() -> OrchestratorCallbacks:
    return PersistenceCallbacks()
