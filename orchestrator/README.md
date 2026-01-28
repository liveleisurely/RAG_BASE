# Orchestrator

이 디렉터리는 LangGraph 기반 오케스트레이션 레이어와 관련 자산을 관리합니다.

- `nodes`: LangGraph에서 사용하는 각 노드 로직을 둡니다.
- `prompts`: 프롬프트 템플릿과 관련 자산을 둡니다.
- `orchestrator`: 그래프 구성, 라우팅, 실행 제어 로직을 둡니다.
- `generator`: 응답 생성(LLM 호출 포함) 로직을 둡니다.
- `streaming_response`: 스트리밍 응답 처리 로직을 둡니다.
- `execution`: 검색/재정렬/LLM 호출 등 순수 실행 컴포넌트를 둡니다.
- `persistence.py`: 로깅 및 DB 기록을 연결할 지점을 둡니다.
- `callbacks.py`: LangChain CallbackHandler 기반의 실행 훅과 디스패처를 둡니다.

## DB 기록 규칙 (권장)

1. **Step 시작/종료는 반드시 기록**
   - 각 노드 실행 전후로 `log_step_start` / `log_step_end`를 남깁니다.
   - 실패 시 `log_step_error`를 남겨 재시도/리플레이 시점을 추적합니다.
2. **토큰 기록은 샘플링 전략 권장**
   - 모든 토큰을 기록하면 I/O 병목이 생기므로 샘플링/집계 전략을 권장합니다.
3. **스트리밍 중단 시점 기록**
   - `log_stream_interrupted`로 마지막 정상 스텝과 중단 시점을 남깁니다.
