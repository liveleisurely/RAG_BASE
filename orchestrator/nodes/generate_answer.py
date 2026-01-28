from __future__ import annotations

from typing import Any, Dict, List

from orchestrator.execution.llm import generate_answer as llm_generate_answer


def generate_answer(state: Dict[str, Any]) -> Dict[str, Any]:
    """검색 결과를 바탕으로 응답을 생성합니다."""

    query = state.get("query", "")
    documents: List[str] = state.get("documents", [])
    # 실제 구현에서는 LLM 호출을 통해 최종 답변을 생성합니다.
    answer = llm_generate_answer(query, documents)
    return {"answer": answer}
