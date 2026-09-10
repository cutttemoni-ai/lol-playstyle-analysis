from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict, Field, field_validator


class Settings(BaseModel):
    """실행 설정. 비밀키를 repr에서 숨겨 로그 유출을 방지한다."""

    model_config = ConfigDict(frozen=True)

    riot_api_key: str = Field(repr=False, min_length=1)
    timeout: float = Field(default=15.0, gt=0)
    request_interval: float = Field(default=0.15, ge=0)
    max_retries: int = Field(default=3, ge=0, le=10)

    @field_validator("riot_api_key")
    @classmethod
    def key_must_not_be_placeholder(cls, value: str) -> str:
        value = value.strip()
        if not value or value in {"RGAPI-여기에_발급받은_키", "RGAPI-발급받은키"}:
            raise ValueError("유효한 RIOT_API_KEY를 .env에 입력하세요.")
        return value


def load_settings(project_root: Path) -> Settings:
    load_dotenv(project_root / ".env")
    return Settings(riot_api_key=os.getenv("RIOT_API_KEY", ""))
