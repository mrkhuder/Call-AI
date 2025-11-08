from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    environment: str = "development"
    version: str = "0.1.0"
    api_prefix: str = "/api/v1"
    cors_allow_origins: List[str] = ["*"]

    db_url: str = "sqlite:///./careflow.db"
    db_echo: bool = False
    message_broker_url: str | None = None
    ehr_api_base_url: str | None = None
    no_show_model_path: str = "ml/models/no_show_v1/pipeline.pkl"
    feature_flags: dict[str, bool] = {"use_mock_ehr": True, "use_mock_messaging": True, "enable_phone_ai": False}

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
