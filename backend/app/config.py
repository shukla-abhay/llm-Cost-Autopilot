"""
Central settings file. Sab environment variables yahan se load hote hain.
Kahin aur `os.environ` mat likhna — hamesha `settings` yahan se import karo.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Cheap tier — Gemini Flash
    gemini_api_key: str = ""
    gemini_flash_model: str = "gemini-3.6-flash"

    # Strong tier — DeepSeek
    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com/v1"
    deepseek_strong_model: str = "deepseek-chat"

    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/llm_autopilot"
    redis_url: str = "redis://localhost:6379/0"

    env: str = "development"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
