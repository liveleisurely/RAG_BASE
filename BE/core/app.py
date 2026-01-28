from fastapi import FastAPI

from BE.apis.chat import router as chat_router
from BE.apis.health import router as health_router
from BE.constants.config import get_app_config


def create_app() -> FastAPI:
    config = get_app_config()
    app = FastAPI(title="RAG Orchestrator API", debug=config.debug)
    app.include_router(health_router)
    app.include_router(chat_router)
    return app
