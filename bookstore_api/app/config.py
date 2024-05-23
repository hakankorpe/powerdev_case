"""
Configuration settings for the application.
"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Settings configuration for the application."""
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./test.db"

settings = Settings()
