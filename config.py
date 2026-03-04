from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Get the directory where this file lives
DOTENV = Path(__file__).resolve().parent / ".env"

class Settings(BaseSettings):
    port: int = 8000
    host: str = "0.0.0.0"
    db_url: str | None = None  # Example of an optional setting

    model_config = SettingsConfigDict(
        env_file=DOTENV, 
        env_file_encoding="utf-8",
        # This prevents the app from crashing if the .env file is missing 
        # (useful for Docker/Production environments)
        extra="ignore" 
    )

settings = Settings()