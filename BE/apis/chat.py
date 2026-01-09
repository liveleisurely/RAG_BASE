from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import StreamingResponse

from BE.schemas.chat import ChatRequest, ChatResponse
from orchestrator.callbacks import build_default_callbacks
from orchestrator.orchestrator.run import run_orchestrator
from orchestrator.orchestrator.stream import orchestrator_stream
from orchestrator.streaming_response.response import stream_response

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat_api(request: ChatRequest) -> ChatResponse:
    """stream 플래그에 따라 스트리밍/비스트리밍을 분기합니다."""

    if request.stream:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="stream=true 요청은 /chat/stream 엔드포인트를 사용하세요.",
        )

    response = run_orchestrator(request.to_state(), callbacks=build_default_callbacks())
    return ChatResponse(
        request_id=request.request_id,
        chat_id=request.chat_id,
        answer=response.answer,
        metadata=response.metadata,
    )


@router.post("/stream")
async def chat_stream_api(request: ChatRequest, http_request: Request) -> StreamingResponse:
    """stream 플래그 기반 스트리밍 응답 엔드포인트입니다."""

    if not request.stream:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="stream=false 요청은 /chat 엔드포인트를 사용하세요.",
        )

    state = request.to_state()
    callbacks = build_default_callbacks()
    return StreamingResponse(
        stream_response(
            orchestrator_stream(state, http_request.is_disconnected, callbacks=callbacks)
        ),
        media_type="text/event-stream",
    )
