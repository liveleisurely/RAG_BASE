from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from BE.schemas.chat import ChatRequest, ChatResponse
from orchestrator.callbacks import build_default_handlers
from orchestrator.orchestrator.run import run_orchestrator
from orchestrator.orchestrator.stream import orchestrator_stream
from orchestrator.streaming_response.response import stream_response

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat_api(request: ChatRequest, http_request: Request) -> ChatResponse | StreamingResponse:
    """stream 플래그에 따라 스트리밍/비스트리밍 응답을 자동으로 선택합니다."""

    state = request.to_state()
    handlers = build_default_handlers()
    if request.stream:
        return StreamingResponse(
            stream_response(
                orchestrator_stream(state, http_request.is_disconnected, handlers=handlers)
            ),
            media_type="text/event-stream",
        )

    response = run_orchestrator(state, handlers=handlers)
    return ChatResponse(
        request_id=request.request_id,
        chat_id=request.chat_id,
        answer=response.answer,
        metadata=response.metadata,
    )
