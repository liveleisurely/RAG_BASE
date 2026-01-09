from __future__ import annotations

from typing import AsyncGenerator, List


def generate_answer(query: str, docs: List[str]) -> str:
    """LLM 호출 결과를 반환하는 순수 함수입니다."""

    # 실제 구현에서는 여기서 LLM 호출 결과를 반환합니다.
    context = " ".join(docs)
    return f"요청을 수신했습니다: {query} | 컨텍스트: {context}"


async def stream_tokens(query: str, docs: List[str]) -> AsyncGenerator[str, None]:
    """토큰 스트리밍을 위한 순수 제너레이터입니다."""

    # 실제 구현에서는 LLM 스트리밍 API를 호출해 토큰을 순차적으로 반환합니다.
    answer = generate_answer(query, docs)
    for token in answer.split():
        yield token
