from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    API_KEY: str
    EXCEL_FILE: str
    USER: str
    PASSWORD: str

    class Config:
        env_file = ".env"

# New decorator for cache
@lru_cache()
def get_settings():
    return Settings()