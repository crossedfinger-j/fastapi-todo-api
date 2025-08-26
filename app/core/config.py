# app/core/config.py
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "To-do List API"
    API_V1_STR: str = "/api/v1"
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    DATABASE_URL: PostgresDsn | None = None

    model_config = SettingsConfigDict(env_file=".env", extra='ignore')

    @classmethod
    def model_validate(cls, values, **kwargs):
        if isinstance(values, dict) and 'DATABASE_URL' not in values:
            values['DATABASE_URL'] = PostgresDsn.build(
                scheme="postgresql",
                username=values.get("POSTGRES_USER"),
                password=values.get("POSTGRES_PASSWORD"),
                host=values.get("POSTGRES_SERVER"),
                path=f"/{values.get('POSTGRES_DB') or ''}",
            )
        return super().model_validate(values, **kwargs)


settings = Settings()
