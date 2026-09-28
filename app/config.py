from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "PocketSmart AI"
    secret_key: str = "change-me"
    database_url: str = "sqlite:///./data/pocketsmart.db"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    cors_origins: str = "http://127.0.0.1:8000,http://localhost:8000"
    access_token_expire_minutes: int = 1440
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)
    @property
    def origins(self): return [x.strip() for x in self.cors_origins.split(",") if x.strip()]

@lru_cache
def get_settings(): return Settings()
settings = get_settings()
