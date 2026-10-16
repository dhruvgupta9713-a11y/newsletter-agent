import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = Path(__file__).resolve().parent

raw_output_dir = os.getenv("OUTPUT_DIR", "outputs")
OUTPUT_DIR = (BASE_DIR / raw_output_dir).resolve() if not Path(raw_output_dir).is_absolute() else Path(raw_output_dir)

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "").strip()
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o").strip()
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "").strip()
    
    # Auto-detect demo mode: if API keys are missing, demo mode is automatically enabled
    FORCE_DEMO: bool = os.getenv("DEMO_MODE", "false").lower() in ("true", "1", "yes")
    
    @property
    def is_demo_mode(self) -> bool:
        if self.FORCE_DEMO:
            return True
        # If neither OpenAI key nor Tavily key is provided, run in demo mode
        return not bool(self.OPENAI_API_KEY)
    
    DEFAULT_SUBSCRIBER_COUNT: int = int(os.getenv("DEFAULT_SUBSCRIBER_COUNT", "1420"))
    BACKEND_HOST: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", "8000"))
    OUTPUT_DIRECTORY: Path = OUTPUT_DIR

settings = Settings()

def get_system_status() -> Dict[str, Any]:
    """Returns configuration and provider connection statuses."""
    has_openai = bool(settings.OPENAI_API_KEY)
    has_tavily = bool(settings.TAVILY_API_KEY)
    
    return {
        "demo_mode": settings.is_demo_mode,
        "openai_configured": has_openai,
        "openai_model": settings.OPENAI_MODEL if has_openai else "simulation-fallback",
        "tavily_configured": has_tavily,
        "search_provider": "Tavily Search API" if has_tavily else "Curated AI Agent News Intelligence (Demo)",
        "output_directory": str(settings.OUTPUT_DIRECTORY),
        "default_subscribers": settings.DEFAULT_SUBSCRIBER_COUNT,
        "status": "operational"
    }
