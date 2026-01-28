from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from pydantic import BaseModel, Field


class UserInfo(BaseModel):
    """사용자 메타데이터를 담는 구조입니다."""

    user_id: str = Field(..., description="내부 사용자 식별자")
    locale: str | None = Field(default=None, description="사용자 로케일 정보")
    attributes: Dict[str, Any] = Field(default_factory=dict, description="추가 속성")


class ChatRequest(BaseModel):
    """채팅 요청에 필요한 최소 식별자와 질의를 포함합니다."""

    request_id: str = Field(..., description="요청 단위 식별자")
    chat_id: str = Field(..., description="대화 세션 식별자")
    query: str = Field(..., description="사용자 질의")
    user: UserInfo
    stream: bool = Field(default=False, description="스트리밍 응답 여부")

    def to_state(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "chat_id": self.chat_id,
            "query": self.query,
            "user": self.user.model_dump(),
        }


class ChatResponse(BaseModel):
    """비스트리밍 응답을 위한 구조입니다."""

    request_id: str
    chat_id: str
    answer: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


@dataclass
class GeneratedResponse:
    answer: str
    metadata: Dict[str, Any]
