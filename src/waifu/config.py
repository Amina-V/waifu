"""Configuration management for the waifu assistant."""
import os
from typing import Dict, Any
from dotenv import load_dotenv

class Config:
    """Manages configuration settings."""
    def __init__(self):
        self.load_env()
        self.validate()

    def load_env(self) -> None:
        """Loads environment variables from .env file."""
        load_dotenv()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("MODEL", "gpt-4")
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.voice_enabled = os.getenv("VOICE_ENABLED", "false").lower() == "true"
        self.theme = os.getenv("THEME", "kawaii")

    def validate(self) -> None:
        """Validates that required environment variables are set."""
        if not self.openai_api_key:
            raise ValueError("Missing OpenAI API Key! Make sure it's set in .env")

    def get(self, key: str) -> Any:
        """Gets a configuration value."""
        return getattr(self, key, None)

    def set(self, key: str, value: Any) -> None:
        """Sets a configuration value."""
        setattr(self, key, value) 