# RAG BASE ASSET 구축 프로젝트

## 1) 오프라인/제한 환경 설치 절차 (WHL 기반)

> 전제: 네트워크가 제한된 환경(air-gapped)을 고려해, 프로젝트에 필요한 WHL 파일을 미리 확보합니다.

### 1.1 필요한 WHL 버전 목록 예시
아래는 예시이며, 실제 사용 버전은 운영 정책에 맞게 고정하세요.

- `fastapi==0.110.0`
- `uvicorn==0.29.0`
- `pydantic==2.6.4`
- `langgraph==0.0.40`
- `sqlalchemy==2.0.28`

### 1.1.1 최신 버전 기준으로 고정하는 절차 (온라인 환경에서 수행)
> 네트워크가 가능한 환경에서만 실행 가능합니다. 오프라인 환경에서는 아래 절차로 미리 준비한 WHL을 사용하세요.

1. 최신 버전 확인
```bash
pip index versions langgraph
```

2. 요구 버전 확정 후 `requirements.lock` 갱신
```bash
# 예시: 최신 버전을 확인해 반영한 뒤, 요구 버전을 직접 수정합니다.
sed -i 's/^langgraph==.*/langgraph==<latest>/' requirements.lock
```

3. WHL 재다운로드
```bash
pip download --dest wheelhouse -r requirements.lock
```

### 1.2 WHL 파일 준비
1. 온라인 환경에서 `wheelhouse/` 폴더를 준비합니다.
2. 필요한 버전의 WHL 파일을 모두 다운로드합니다.
3. 오프라인 환경으로 `wheelhouse/` 전체를 이동합니다.

```bash
mkdir -p wheelhouse
# 예시: pip download --dest wheelhouse fastapi==0.110.0
```

### 1.3 가상환경 생성 및 WHL 설치
```bash
python -m venv .venv
source .venv/bin/activate
pip install --no-index --find-links=wheelhouse -r requirements.lock
```

> `requirements.lock`에는 정확한 버전을 고정해두는 것을 권장합니다.

---

## 2) 실행 환경 구분 (local / dev / prd)

### 2.1 환경 선택 방식
`APP_ENV` 환경 변수로 실행 환경을 구분합니다.

- `local`: 로컬 개발용
- `dev`: 개발 서버용
- `prd`: 운영 서버용

```bash
export APP_ENV=local  # 또는 dev / prd
```

### 2.2 환경별 설정 사용
`BE/constants/config.py`에서 환경별 설정을 관리합니다.

- 디버그 여부
- 로그 레벨
- API 타임아웃 등

현재는 아래 기본값으로 동작합니다:

- local: `debug=True`, `log_level=DEBUG`, `api_timeout_seconds=30`
- dev: `debug=False`, `log_level=INFO`, `api_timeout_seconds=20`
- prd: `debug=False`, `log_level=WARNING`, `api_timeout_seconds=10`

---

## 3) 애플리케이션 실행 예시
```bash
export APP_ENV=local
uvicorn BE.core.app:create_app --factory --host 0.0.0.0 --port 8000
```
