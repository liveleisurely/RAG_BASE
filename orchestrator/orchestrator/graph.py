from __future__ import annotations

import operator
from typing import Any, Annotated, Dict, List, TypedDict

from langgraph.graph import END, Send, StateGraph

from orchestrator.nodes.generate_answer import generate_answer
from orchestrator.nodes.rewrite_query import rewrite_query
from orchestrator.nodes.search_documents import search_documents


class GraphState(TypedDict, total=False):
    request_id: str
    chat_id: str
    query: str
    user: Dict[str, Any]
    rewritten_query: str
    documents: Annotated[List[str], operator.add]
    answer: str


def _fan_out_search(state: Dict[str, Any]) -> List[Send]:
    """검색 노드를 병렬로 실행하도록 Send 작업을 구성합니다."""

    return [
        Send("search_documents", {"source": "alpha"}),
        Send("search_documents", {"source": "beta"}),
    ]


def build_graph() -> StateGraph:
    """질의 재작성 -> 병렬 검색 -> 답변 생성 구조를 구성합니다."""

    graph = StateGraph(GraphState)
    graph.add_node("rewrite_query", rewrite_query)
    graph.add_node("search_documents", search_documents)
    graph.add_node("generate_answer", generate_answer)

    graph.set_entry_point("rewrite_query")
    graph.add_conditional_edges("rewrite_query", _fan_out_search)
    graph.add_edge("search_documents", "generate_answer")
    graph.add_edge("generate_answer", END)

    return graph.compile()
