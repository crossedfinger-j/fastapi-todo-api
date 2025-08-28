# app/core/config.py
from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "To-do List API"
    API_V1_STR: str = "/api/v1"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    SECRET_KEY: str = None

    POSTGRES_SERVER: str = None
    POSTGRES_USER: str = None
    POSTGRES_PASSWORD: str = None
    POSTGRES_DB: str = None

    # DATABASE_URL: PostgresDsn | None = None

    model_config = SettingsConfigDict(env_file=".env", extra='ignore')

    @computed_field
    @property
    def database_url(self) -> PostgresDsn:
        url = PostgresDsn.build(
            scheme="postgresql",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            path=f"{self.POSTGRES_DB or ''}",
        )
        print(f"Computed DATABASE_URL: {url}")
        return url

settings = Settings()
