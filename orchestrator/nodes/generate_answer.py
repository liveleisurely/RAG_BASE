from __future__ import annotations

from typing import Any, Dict, List

from langchain_core.runnables import RunnableConfig

from orchestrator.callbacks import notify_token
from orchestrator.execution.llm import stream_tokens


async def generate_answer(
    state: Dict[str, Any], config: RunnableConfig | None = None
) -> Dict[str, Any]:
    """검색 결과를 바탕으로 응답을 생성합니다."""

    query = state.get("query", "")
    documents: List[str] = state.get("documents", [])
    callbacks = config.get("callbacks") if config else None
    tokens: List[str] = []
    # 실제 구현에서는 LLM 스트리밍 API를 통해 토큰을 순차적으로 생성합니다.
    async for token in stream_tokens(query, documents):
        tokens.append(token)
        if callbacks:
            notify_token(callbacks, token, state)
    return {"answer": " ".join(tokens), "tokens": tokens}
