from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

class DocumentIntelligenceSettings(BaseSettings):
    api_key: str = os.environ.get("DOCUMENT_INTELLIGENCE_API_KEY")
    endpoint: str = os.environ.get("DOCUMENT_INTELLIGENCE_ENDPOINT")

class Settings(BaseSettings):
    app_name: str = "Invoice Extraction"
    env: str = "local"  # Default to local if not specified
    temperature: float = 0.0
    max_tokens: Optional[int] = None
    max_retries: int = 3
    document_intelligence: DocumentIntelligenceSettings = DocumentIntelligenceSettings()
    azure_api_key: Optional[str] = None
    azure_url: Optional[str] = None
    azure_api_version: Optional[str] = os.environ.get("AZURE_API_VERSION")

# @lru_cache(maxsize=None)
def get_settings() -> Settings:
    """Function to get and cache settings.
    The settings are cached to avoid repeated disk I/O.
    """
    return Settings()