from __future__ import annotations

from typing import Any, Dict

from orchestrator.execution.llm import rewrite_query as llm_rewrite_query


def rewrite_query(state: Dict[str, Any]) -> Dict[str, Any]:
    """사용자 질의를 재작성합니다."""

    # 실제 구현에서는 LLM 호출을 통해 질의를 재작성합니다.
    query = state.get("query", "")
    rewritten = llm_rewrite_query(query)
    return {"rewritten_query": rewritten}
