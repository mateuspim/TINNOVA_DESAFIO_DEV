from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", ".env.prod"), env_file_encoding="utf-8"
    )

    DATABASE_URL: str = None

    API_PREFIX: str = "/api"
    DEBUG: bool = True
    ALLOWED_ORIGINS: str = ""

    @field_validator("ALLOWED_ORIGINS")
    def parse_allowed_origins(cls, v: str) -> List[str]:
        if v == "*":
            return ["*"]
        return [u for u in v.split(",") if u.startswith("http")] if v else []


settings = Settings()
