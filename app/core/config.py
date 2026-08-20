from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "SentriqVision AI Platform"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = Field(
        "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7",
        validation_alias="SECRET_KEY",
    )
    REFRESH_SECRET_KEY: str = Field(
        "8c0e18dbcfd36a3f9e9d638706857fb1e52d3a3d5b78b548b261bd7f4955bd9c",
        validation_alias="REFRESH_SECRET_KEY",
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "*",
    ]

    # Database
    POSTGRES_SERVER: str = Field("localhost", validation_alias="POSTGRES_SERVER")
    POSTGRES_USER: str = Field("postgres", validation_alias="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field("postgres", validation_alias="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field("sentriqvision_db", validation_alias="POSTGRES_DB")
    POSTGRES_PORT: str = Field("5432", validation_alias="POSTGRES_PORT")
    DATABASE_URL: str | None = None

    # SQLite Fallback for testing/dev if postgres unavailable
    USE_SQLITE_FALLBACK: bool = Field(True, validation_alias="USE_SQLITE_FALLBACK")
    SQLITE_DB_PATH: str = "./sentriqvision_dev.db"

    # Redis
    REDIS_HOST: str = Field("localhost", validation_alias="REDIS_HOST")
    REDIS_PORT: int = Field(6379, validation_alias="REDIS_PORT")
    REDIS_DB: int = Field(0, validation_alias="REDIS_DB")
    REDIS_URL: str | None = None

    # Storage
    STORAGE_DIR: str = "./data/storage"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    def get_async_database_url(self) -> str:
        if self.USE_SQLITE_FALLBACK:
            return f"sqlite+aiosqlite:///{self.SQLITE_DB_PATH}"
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    def get_sync_database_url(self) -> str:
        if self.USE_SQLITE_FALLBACK:
            return f"sqlite:///{self.SQLITE_DB_PATH}"
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    def get_redis_url(self) -> str:
        if self.REDIS_URL:
            return self.REDIS_URL
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


settings = Settings()
