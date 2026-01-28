from pydantic import BaseModel


class HealthResponse(BaseModel):
    """기본 헬스체크 응답 스키마입니다."""

    status: str
