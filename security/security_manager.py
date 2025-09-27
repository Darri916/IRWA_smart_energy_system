import os
from pathlib import Path

class Config:
    # Project paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    
    # Weather API configuration
    WEATHER_API_KEY = "1da2d4b96cace6806188f6fc84a2551b"  # Consider using environment variable
    WEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5"
    
    # System settings
    MAX_AGENTS = 5
    FORECAST_HORIZON = 24
    
    # Model settings
    DEVICE = "cuda" if os.getenv("CUDA_AVAILABLE") else "cpu"
    MODEL_CACHE_DIR = BASE_DIR / "model_cache"
    
    # Security settings
    SESSION_TIMEOUT = 3600  # 1 hour in seconds
    MAX_SESSIONS = 100
    
    @classmethod
    def get_weather_api_key(cls):
        """Get weather API key from environment or config"""
        return os.getenv("WEATHER_API_KEY", cls.WEATHER_API_KEY)
    
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist"""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.MODEL_CACHE_DIR.mkdir(exist_ok=True)