# Orchestrator

이 디렉터리는 LangGraph 기반 오케스트레이션 레이어와 관련 자산을 관리합니다.

- `nodes`: LangGraph에서 사용하는 각 노드 로직을 둡니다.
- `prompts`: 프롬프트 템플릿과 관련 자산을 둡니다.
- `orchestrator`: 그래프 구성, 라우팅, 실행 제어 로직을 둡니다.
- `generator`: 응답 생성(LLM 호출 포함) 로직을 둡니다.
- `streaming_response`: 스트리밍 응답 처리 로직을 둡니다.
- `execution`: 검색/재정렬/LLM 호출 등 순수 실행 컴포넌트를 둡니다.
- `persistence.py`: 로깅 및 DB 기록을 연결할 지점을 둡니다.
- `callbacks.py`: 오케스트레이터 실행 훅(콜백) 정의를 둡니다.
