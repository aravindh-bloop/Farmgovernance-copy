"""
Global settings and environment configurations for the Cooperative AI Portal.
"""
import os
from typing import List, Optional

try:
    from pydantic_settings import BaseSettings
    class Settings(BaseSettings):
        APP_NAME: str = "Multilingual Cooperative Governance & Legal Assistance Portal"
        APP_VERSION: str = "1.0.0"
        API_V1_STR: str = "/api/v1"
        PORT: int = 8000
        HOST: str = "0.0.0.0"
        SUPPORTED_LANGUAGES: List[str] = [
            "en", "hi", "ta", "te", "mr", "gu", "bn", "kn", "ml", "pa", "or"
        ]
        DEFAULT_LANGUAGE: str = "en"
        OFFLINE_MODE: bool = True
        DEFAULT_LLM_PROVIDER: str = "gemini"
        GROQ_API_KEY: Optional[str] = None
        GEMINI_API_KEY: Optional[str] = None
        SARVAM_API_KEY: Optional[str] = None
        OPENAI_API_KEY: Optional[str] = None
        BHASHINI_API_KEY: Optional[str] = None
        BHASHINI_USER_ID: Optional[str] = None
        BHASHINI_INFERENCE_API_KEY: Optional[str] = None
        BHASHINI_PIPELINE_ID: Optional[str] = None
        EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

        BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        DATABASE_PATH: str = os.path.join(BASE_DIR, "database", "data")
        AUTHORITIES_PATH: str = os.path.join(BASE_DIR, "database", "authorities", "authorities.json")
        VECTOR_DB_PATH: str = os.path.join(BASE_DIR, "database", "vector_db")
        OFFICER_DIRECTORY_PATH: str = os.path.join(BASE_DIR, "database", "data", "officers", "officer_directory.json")

        class Config:
            env_file = ".env"
            extra = "ignore"
    settings = Settings()
except ImportError:
    class FallbackSettings:
        APP_NAME = "Multilingual Cooperative Governance & Legal Assistance Portal"
        APP_VERSION = "1.0.0"
        API_V1_STR = "/api/v1"
        PORT = 8000
        HOST = "0.0.0.0"
        SUPPORTED_LANGUAGES = ["en", "hi", "ta", "te", "mr", "gu", "bn", "kn", "ml", "pa", "or"]
        DEFAULT_LANGUAGE = "en"
        OFFLINE_MODE = True
        DEFAULT_LLM_PROVIDER = "gemini"
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        BHASHINI_API_KEY = os.getenv("BHASHINI_API_KEY")
        BHASHINI_USER_ID = os.getenv("BHASHINI_USER_ID")
        BHASHINI_INFERENCE_API_KEY = os.getenv("BHASHINI_INFERENCE_API_KEY")
        BHASHINI_PIPELINE_ID = os.getenv("BHASHINI_PIPELINE_ID")
        EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        DATABASE_PATH = os.path.join(BASE_DIR, "database", "data")
        AUTHORITIES_PATH = os.path.join(BASE_DIR, "database", "authorities", "authorities.json")
        VECTOR_DB_PATH = os.path.join(BASE_DIR, "database", "vector_db")
        OFFICER_DIRECTORY_PATH = os.path.join(BASE_DIR, "database", "data", "officers", "officer_directory.json")

    settings = FallbackSettings()
