from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))  # Load environment variables from .env relative to the running file
class DocumentIntelligenceSettings(BaseSettings):
    api_key: str = os.environ.get("DOCUMENT_INTELLIGENCE_API_KEY", "")
    endpoint: str = os.environ.get("DOCUMENT_INTELLIGENCE_ENDPOINT", "")

class Settings(BaseSettings):
    app_name: str = "Invoice Extraction"
    env: str = "local"  # Default to local if not specified
    temperature: float = 0.0
    max_tokens: Optional[int] = None
    max_retries: int = 3
    document_intelligence: DocumentIntelligenceSettings = DocumentIntelligenceSettings()
    azure_api_key: Optional[str] = os.environ.get("AZURE_API_KEY", "")
    azure_url: Optional[str] = os.environ.get("AZURE_URL", "")
    azure_api_version: Optional[str] = os.environ.get("AZURE_API_VERSION", "")

def get_settings() -> Settings:
    """Function to get settings."""
    return Settings()
