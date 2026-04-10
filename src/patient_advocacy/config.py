"""Configuration — local-first, no cloud."""

from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    db_path: Path = Path.home() / ".patient-advocate" / "data.db"
    host: str = "127.0.0.1"
    port: int = 8000

    model_config = {"env_prefix": "PATIENT_ADVOCATE_"}


settings = Settings()
