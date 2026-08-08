from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    # Бд
    DB_HOST: str = Field(default="localhost")
    DB_USER: str = Field(default="postgres")
    DB_PORT: int = Field(default="5432")
    DB_PASSWORD: str
    DB_NAME: str 
    
    # JWT 
    SECRET_KEY: str
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=30)


    TEST_DATABASE_URL: str

    
    model_config = SettingsConfigDict(
        env_file=".env", # ../.env # .env (для миграций для докера а также для вставки фейк данных)
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @property
    def database_url(self):
        """Собирает URL для подключения к PostgreSQL"""
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

settings = Settings()

