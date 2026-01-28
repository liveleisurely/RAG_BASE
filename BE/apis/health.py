from fastapi import APIRouter

from BE.schemas.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def healthcheck() -> HealthResponse:
    """서비스 상태를 확인하기 위한 기본 헬스체크 엔드포인트입니다."""

    return HealthResponse(status="ok")
