
# ==========================================
# 간단한 Mock RAG
# ==========================================


import asyncio
import json
import uvicorn
import operator
import logging
from typing import TypedDict, List, Annotated
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, JSONResponse, FileResponse
from pydantic import BaseModel, Field

# LangGraph 관련 임포트
from langgraph.graph import StateGraph, END

# ==========================================
# [0] 로깅(Logging) 설정 (Fix: handlers 오타 수정)
# ==========================================
# print() 대신 운영 환경에 남길 로그를 설정합니다.
logger = logging.getLogger("RAG_BASE")
logger.setLevel(logging.INFO)

# 핸들러 설정 (콘솔 출력)
console_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# ==========================================
# [1] 데이터 모델 정의 (Schema & State)
# ==========================================
class ChatRequest(BaseModel):
    question: str = Field(..., description="사용자 질문", example="LangGraph 병렬 처리")
    stream: bool = Field(False, description="스트리밍 여부", example=True)

class GraphState(TypedDict):
    question: str
    rewritten_query: str
    # 💡 핵심: 병렬 노드 결과가 덮어씌워지지 않고 합쳐지도록(Add) 설정
    context: Annotated[List[str], operator.add]
    answer: str

# ==========================================
# [2] Mock 로직 (실제 연동 시 LLM/DB 코드로 교체)
# ==========================================
async def mock_rewrite_logic(question: str) -> str:
    # logger.info(f"쿼리 최적화 로직 수행 중: {question}")
    await asyncio.sleep(0.5)
    return f"최적화된 쿼리: {question}"

async def mock_search_source_a(query: str) -> List[str]:
    await asyncio.sleep(1.0)
    return [f"[Wiki] '{query}' 검색 결과"]

async def mock_search_source_b(query: str) -> List[str]:
    await asyncio.sleep(1.0)
    return [f"[CorpDB] '{query}' 사내 문서"]

async def mock_answer_generator(context: List[str]):
    full_context = " | ".join(context)
    response_text = f"수집된 {len(context)}개의 문서를 바탕으로 답변합니다.\n(출처: {full_context})"
    
    # 토큰 단위 스트리밍 시뮬레이션
    for char in response_text:
        await asyncio.sleep(0.05)
        yield char

# ==========================================
# [3] LangGraph 노드 정의
# ==========================================
async def rewrite_node(state: GraphState):
    logger.info(f"🔄 [Rewrite] 시작 - 질문: {state['question']}")
    new_query = await mock_rewrite_logic(state['question'])
    return {"rewritten_query": new_query}

async def search_node_1(state: GraphState):
    logger.info(f"🔍 [Search1] 위키 검색 시작")
    docs = await mock_search_source_a(state['rewritten_query'])
    return {"context": docs}

async def search_node_2(state: GraphState):
    logger.info(f"🔍 [Search2] 사내 DB 검색 시작")
    docs = await mock_search_source_b(state['rewritten_query'])
    return {"context": docs}

async def generate_node(state: GraphState):
    logger.info(f"🧠 [Generate] 답변 생성 시작 (Context: {len(state['context'])}개)")
    # Non-stream 요청을 위해 전체 텍스트 생성
    chunks = [c async for c in mock_answer_generator(state['context'])]
    return {"answer": "".join(chunks)}

# ==========================================
# [4] 그래프 조립 (Topology)
# ==========================================
workflow = StateGraph(GraphState)

# 노드 등록
workflow.add_node("rewrite", rewrite_node)
workflow.add_node("search1", search_node_1)
workflow.add_node("search2", search_node_2)
workflow.add_node("generate", generate_node)

# 엣지 연결 (병렬 처리 구조)
workflow.set_entry_point("rewrite")
workflow.add_edge("rewrite", "search1") # Fan-out
workflow.add_edge("rewrite", "search2") # Fan-out
workflow.add_edge("search1", "generate") # Fan-in
workflow.add_edge("search2", "generate") # Fan-in
workflow.add_edge("generate", END)

app_graph = workflow.compile()

# ==========================================
# [5] FastAPI 애플리케이션
# ==========================================
app = FastAPI(title="RAG_BASE Service")

@app.get("/")
async def root():
    return {"message": "RAG_BASE Server Running. Visit /docs"}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("favicon.ico")

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    # 초기 상태 (Context는 빈 리스트로 시작)
    initial_state = {"question": req.question, "context": []}

    # CASE A: 스트리밍 (SSE)
    if req.stream:
        async def event_generator():
            # [트랙 1] LangGraph 이벤트 감지 (서버 로깅 + 상태 메시지 전송)
            async for event in app_graph.astream_events(initial_state, version="v2"):
                kind = event["event"]
                name = event["name"]
                meta = event.get("metadata", {})
                node_id = meta.get("langgraph_node")

                # ✨ 거울 기법: 진짜 노드의 시작만 필터링
                if kind == "on_chain_start" and node_id and name == node_id:
                    # 프론트엔드용 상태 메시지 생성
                    status_msg = ""
                    if node_id == "rewrite": status_msg = "✍️ 질문을 최적화하고 있습니다..."
                    elif "search" in node_id: status_msg = f"🔎 {node_id}에서 자료 검색 중..."
                    elif node_id == "generate": status_msg = "🤖 답변을 작성하고 있습니다..."
                    
                    if status_msg:
                        payload = json.dumps({'type': 'status', 'content': status_msg}, ensure_ascii=False)
                        yield f"data: {payload}\n\n"

            # [트랙 2] 실제 답변 스트리밍 (Mock)
            # (실제 구현 시엔 위 astream_events 루프 내 on_chat_model_stream 사용)
            dummy_context = ["Mock Data"]
            async for char in mock_answer_generator(dummy_context):
                payload = json.dumps({'type': 'token', 'content': char}, ensure_ascii=False)
                yield f"data: {payload}\n\n"

            yield "data: [DONE]\n\n"

        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            }
        )

    # CASE B: 일반 요청 (JSON)
    else:
        result = await app_graph.ainvoke(initial_state)
        return JSONResponse(content={
            "question": result["question"],
            "answer": result["answer"],
            "sources": result["context"]
        })

if __name__ == "__main__":
    print("🚀 [RAG_BASE] 서버 시작: http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
