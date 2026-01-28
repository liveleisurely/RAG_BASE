from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    """애플리케이션 환경별 설정을 담는 구조입니다."""

    env: str
    debug: bool
    log_level: str
    api_timeout_seconds: int


def _config_local() -> AppConfig:
    return AppConfig(env="local", debug=True, log_level="DEBUG", api_timeout_seconds=30)


def _config_dev() -> AppConfig:
    return AppConfig(env="dev", debug=False, log_level="INFO", api_timeout_seconds=20)


def _config_prd() -> AppConfig:
    return AppConfig(env="prd", debug=False, log_level="WARNING", api_timeout_seconds=10)


def get_app_config() -> AppConfig:
    """APP_ENV 값에 따라 환경별 설정을 반환합니다."""

    env = os.getenv("APP_ENV", "local").lower()
    if env == "dev":
        return _config_dev()
    if env == "prd":
        return _config_prd()
    return _config_local()
