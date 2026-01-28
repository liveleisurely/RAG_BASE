from __future__ import annotations

from typing import Any, Dict


def log_step_start(step: str, state: Dict[str, Any]) -> None:
    """스텝 시작 시점을 기록합니다. (DB 연동 지점)"""

    _ = (step, state)


def log_step_end(step: str, state: Dict[str, Any]) -> None:
    """스텝 종료 시점을 기록합니다. (DB 연동 지점)"""

    _ = (step, state)


def log_step_error(step: str, error: Exception, state: Dict[str, Any]) -> None:
    """스텝 실패 시점을 기록합니다. (DB 연동 지점)"""

    _ = (step, error, state)


def log_token(token: str, state: Dict[str, Any]) -> None:
    """토큰 단위 이벤트를 기록합니다. (DB 연동 지점)"""

    _ = (token, state)


def log_stream_interrupted(state: Dict[str, Any]) -> None:
    """스트리밍 중단 상황을 기록합니다. (DB 연동 지점)"""

    _ = state
