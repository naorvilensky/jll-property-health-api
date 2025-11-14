from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path

class Settings(BaseSettings):
    PROPERTY_FILE: Path = Path("./data/property_data.json")
    MARKET_FILE: Path = Path("./data/market_data.json")

    ENV: str = "local"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
