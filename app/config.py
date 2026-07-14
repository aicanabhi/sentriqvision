
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # API settings
    API_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "SentriQVision AI Camera Platform"
    
    # MongoDB
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = "visionx_db"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production-please-very-important"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Super Admin
    SUPER_ADMIN_EMAIL: str = "admin@sentriqvision.com"
    SUPER_ADMIN_PASSWORD: str = "SuperAdmin123!"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
