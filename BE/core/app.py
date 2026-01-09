from fastapi import FastAPI

from BE.apis.chat import router as chat_router
from BE.apis.health import router as health_router


def create_app() -> FastAPI:
    app = FastAPI(title="RAG Orchestrator API")
    app.include_router(health_router)
    app.include_router(chat_router)
    return app
