from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Central application configuration.
    Values are loaded from environment variables.
    Example:
        DATABASE_HOST=localhost
    Keeping configuration here means we don't hard-code credentials or infrastructure settings throughout the code.
    """

    #PostgreSQL configuration
    database_host: str = 'localhost'
    database_port: int = 5432
    database_name: str = "cctv_platform"
    database_user: str = "cctv"
    database_password: str = "cctv_password"

    #Application information
    app_name: str = "CCTV AI Platform"
    app_version: str = "0.1.0"

    #JWT authentication configuration
    jwt_secret_key: str = "change-this-in-production"
    access_token_expire_minutes: int = 60

    model_config = SettingsConfigDict(
        env_file="../../.env",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        """
        Build the asynchronous PostgreSQL connection URL.
        SQLAlchemy will use asyncpg as the  PostgreSQL driver.
        """
        return(
            f"postgresql+asyncpg://"
            f"{self.database_user}:"
            f"{self.database_password}@"
            f"{self.database_host}:"
            f"{self.database_port}/"
            f"{self.database_name}"
        )

settings = Settings()