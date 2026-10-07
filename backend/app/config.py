import os
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "litlens.db"

class Settings(BaseSettings):
    PROJECT_NAME: str = "LitLens AI Book Discovery"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    # Database Settings
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")
    
    # AI Model Settings
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "auto") # auto, nvidia, gemini, ollama, fallback
    AI_MODEL: str = os.getenv("AI_MODEL", "gemini-1.5-flash")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # NVIDIA NIM Low-Latency Free Models
    NVIDIA_API_KEY: str = os.getenv("NVIDIA_API_KEY", "")
    NVIDIA_MODEL: str = os.getenv("NVIDIA_MODEL", "meta/llama-3.1-8b-instruct") # Low latency free model
    NVIDIA_BASE_URL: str = "https://integrate.api.nvidia.com/v1"
    
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3")
    
    # Vector Embedding Settings
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
