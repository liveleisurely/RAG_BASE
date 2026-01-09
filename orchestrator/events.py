from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class StepEvent:
    """스텝 단위 진행 상황을 알리기 위한 이벤트입니다."""

    step: str
    status: str
    detail: Dict[str, Any] | None = None

    def to_payload(self) -> Dict[str, Any]:
        return {
            "type": "step",
            "step": self.step,
            "status": self.status,
            "detail": self.detail or {},
        }


@dataclass(frozen=True)
class TokenEvent:
    """토큰 단위 스트리밍을 위한 이벤트입니다."""

    token: str

    def to_payload(self) -> Dict[str, Any]:
        return {
            "type": "token",
            "token": self.token,
        }


@dataclass(frozen=True)
class FinalEvent:
    """최종 응답을 알리기 위한 이벤트입니다."""

    answer: str
    metadata: Dict[str, Any]

    def to_payload(self) -> Dict[str, Any]:
        return {
            "type": "final",
            "answer": self.answer,
            "metadata": self.metadata,
        }
