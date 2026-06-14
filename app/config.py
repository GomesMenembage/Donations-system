from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "sqlite:///./donations.db"
    SECRET_KEY: str = "change-this-to-a-random-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: str = "*"

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    @property
    def cors_origins_list(self) -> list[str]:
        if self.CORS_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"


settings = Settings()
