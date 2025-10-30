import os
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import secrets

# Load environment variables
load_dotenv()

class Config:
    """Enhanced configuration with security and scalability"""
    
    # ==================== Project Paths ====================
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    LOGS_DIR = BASE_DIR / "logs"
    CACHE_DIR = BASE_DIR / "cache"
    
    # ==================== Environment ====================
    class Environment:
        DEVELOPMENT = "development"
        STAGING = "staging"
        PRODUCTION = "production"
    
    ENVIRONMENT = os.getenv("ENVIRONMENT", Environment.DEVELOPMENT)
    
    # ==================== API Keys - Secure Loading ====================
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # ==================== Weather API Configuration ====================
    WEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5"
    WEATHER_FORECAST_DAYS = int(os.getenv("MAX_FORECAST_DAYS", "5"))
    WEATHER_API_TIMEOUT = int(os.getenv("WEATHER_API_TIMEOUT", "10"))
    
    # ==================== Database Configuration ====================
    # FIX: Put database in data directory
    _default_db_path = DATA_DIR / "energy_system.db"
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{_default_db_path}")
    DATABASE_CONNECTION_TIMEOUT = 5  # seconds
    
    # ==================== Security Settings ====================
    SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    JWT_SECRET = os.getenv("JWT_SECRET", secrets.token_urlsafe(32))
    JWT_ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60
    
    # Session management
    SESSION_TIMEOUT = 3600  # 1 hour
    MAX_SESSIONS = 100
    
    # ==================== System Settings ====================
    MAX_AGENTS = int(os.getenv("MAX_CONCURRENT_AGENTS", "10"))
    FORECAST_HORIZON = 24  # hours
    
    # Model settings
    DEVICE = "cuda" if os.getenv("CUDA_AVAILABLE") == "True" else "cpu"
    MODEL_CACHE_DIR = BASE_DIR / "model_cache"
    
    # ==================== AI Service Configuration ====================
    # FIXED: Updated model names and fallback strategy
    AVAILABLE_MODELS = {
        'claude-sonnet-4.5': 'claude-sonnet-4.5-20250929',     # Latest & Best
        'claude-sonnet-3.5': 'claude-3-5-sonnet-20241022',     # Previous version
        'claude-haiku-3': 'claude-3-haiku-20240307',           # Fast/cheap
        'gpt-4-turbo': 'gpt-4-turbo-preview',                  # OpenAI backup
        'gpt-3.5-turbo': 'gpt-3.5-turbo'                       # Cheap backup
    }
    
    DEFAULT_MODEL = 'claude-sonnet-4.5'
    LLM_MODEL = os.getenv("LLM_MODEL", AVAILABLE_MODELS.get(DEFAULT_MODEL))
    
    # LLM Providers with priority
    LLM_PROVIDERS = [
        {
            'name': 'anthropic',
            'models': ['claude-sonnet-4.5', 'claude-sonnet-3.5', 'claude-haiku-3'],
            'api_key_env': 'ANTHROPIC_API_KEY',
            'priority': 1
        },
        {
            'name': 'openai',
            'models': ['gpt-4-turbo', 'gpt-3.5-turbo'],
            'api_key_env': 'OPENAI_API_KEY',
            'priority': 2
        }
    ]
    
    LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "4096"))
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    LLM_API_TIMEOUT = int(os.getenv("LLM_API_TIMEOUT", "30"))
    
    # ==================== Cache Configuration ====================
    CACHE_ENABLED = os.getenv("CACHE_ENABLED", "True") == "True"
    CACHE_TTL = int(os.getenv("CACHE_TTL", "300"))  # 5 minutes
    
    # ==================== Logging Configuration ====================
    DEBUG_MODE = os.getenv("DEBUG_MODE", "False") == "True"
    
    # Adjust based on environment
    if ENVIRONMENT == Environment.PRODUCTION:
        LOG_LEVEL = os.getenv("LOG_LEVEL", "WARNING")
        DEBUG_MODE = False
    else:
        LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # ==================== Responsible AI Settings ====================
    ENABLE_BIAS_DETECTION = os.getenv("ENABLE_BIAS_DETECTION", "True") == "True"
    ENABLE_EXPLAINABILITY = os.getenv("ENABLE_EXPLAINABILITY", "True") == "True"
    ENABLE_AUDIT_LOGGING = os.getenv("ENABLE_AUDIT_LOGGING", "True") == "True"
    
    # ==================== Rate Limiting ====================
    API_RATE_LIMIT = int(os.getenv("API_RATE_LIMIT", "100"))  # requests per minute
    
    # ==================== Energy System Parameters ====================
    GRID_TOTAL_CAPACITY = int(os.getenv("GRID_TOTAL_CAPACITY", "5000"))  # MW
    GRID_RENEWABLE_CAPACITY = int(os.getenv("GRID_RENEWABLE_CAPACITY", "2000"))  # MW
    SOLAR_CAPACITY = int(os.getenv("SOLAR_CAPACITY", "1000"))  # MW
    WIND_CAPACITY = int(os.getenv("WIND_CAPACITY", "1000"))  # MW
    STORAGE_CAPACITY = int(os.getenv("STORAGE_CAPACITY", "500"))  # MWh
    
    # ==================== Forecast Parameters ====================
    CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.7"))
    ALERT_THRESHOLD_DEFICIT = float(os.getenv("ALERT_THRESHOLD_DEFICIT", "0.9"))
    ALERT_THRESHOLD_SURPLUS = float(os.getenv("ALERT_THRESHOLD_SURPLUS", "1.2"))
    
    # ==================== Monitoring & Performance ====================
    ENABLE_METRICS = os.getenv("ENABLE_METRICS", "True") == "True"
    METRICS_RETENTION_DAYS = int(os.getenv("METRICS_RETENTION_DAYS", "30"))
    PERFORMANCE_TRACKING = os.getenv("PERFORMANCE_TRACKING", "True") == "True"
    
    # Health checks
    HEALTH_CHECK_ENABLED = os.getenv("HEALTH_CHECK_ENABLED", "True") == "True"
    HEALTH_CHECK_INTERVAL = int(os.getenv("HEALTH_CHECK_INTERVAL", "60"))  # seconds
    
    # Alerts
    ALERT_EMAIL = os.getenv("ALERT_EMAIL", "")
    ALERT_ON_API_FAILURE = os.getenv("ALERT_ON_API_FAILURE", "True") == "True"
    ALERT_ON_HIGH_LOAD = os.getenv("ALERT_ON_HIGH_LOAD", "True") == "True"
    
    # ==================== Class Methods ====================
    
    @classmethod
    def validate_config(cls) -> Dict[str, Any]:
        """Validate configuration and return detailed status"""
        issues = []
        warnings = []
        
        # Critical checks
        if not cls.OPENWEATHER_API_KEY:
            issues.append("OPENWEATHER_API_KEY not set - Weather data will fail")
        
        if not cls.ANTHROPIC_API_KEY and not cls.OPENAI_API_KEY:
            warnings.append("No AI API key set - Will use fallback responses")
        
        if cls.SECRET_KEY == secrets.token_urlsafe(32):
            warnings.append("SECRET_KEY using default - Generate secure key for production")
        
        if cls.ENVIRONMENT == cls.Environment.PRODUCTION and cls.DEBUG_MODE:
            warnings.append("DEBUG_MODE enabled in production - Security risk!")
        
        # Check directories
        required_dirs = [cls.DATA_DIR, cls.LOGS_DIR, cls.CACHE_DIR]
        for directory in required_dirs:
            if not directory.exists():
                warnings.append(f"Directory {directory} does not exist - will be created")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings,
            'environment': cls.ENVIRONMENT
        }
    
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist"""
        directories = [
            cls.DATA_DIR,
            cls.LOGS_DIR,
            cls.CACHE_DIR,
            cls.MODEL_CACHE_DIR
        ]
        
        for directory in directories:
            directory.mkdir(exist_ok=True, parents=True)
    
    @classmethod
    def get_api_key(cls, service: str) -> Optional[str]:
        """Safely get API key for a service"""
        key_mapping = {
            'openweather': cls.OPENWEATHER_API_KEY,
            'anthropic': cls.ANTHROPIC_API_KEY,
            'openai': cls.OPENAI_API_KEY
        }
        return key_mapping.get(service.lower(), "")
    
    @classmethod
    def get_available_llm_provider(cls) -> Optional[Dict[str, Any]]:
        """Get first available LLM provider with valid API key"""
        for provider in sorted(cls.LLM_PROVIDERS, key=lambda x: x['priority']):
            api_key = os.getenv(provider['api_key_env'])
            if api_key:
                # Get the first available model for this provider
                model_key = provider['models'][0]
                return {
                    'name': provider['name'],
                    'model': cls.AVAILABLE_MODELS.get(model_key),
                    'api_key': api_key
                }
        return None
    
    @classmethod
    def get_llm_config(cls) -> Dict[str, Any]:
        """Get LLM configuration with fallback"""
        provider = cls.get_available_llm_provider()
        
        if provider:
            return {
                'provider': provider['name'],
                'model': provider['model'],
                'max_tokens': cls.LLM_MAX_TOKENS,
                'temperature': cls.LLM_TEMPERATURE,
                'timeout': cls.LLM_API_TIMEOUT,
                'available': True
            }
        else:
            return {
                'provider': 'fallback',
                'model': 'template-based',
                'available': False,
                'message': 'No API keys configured - using template responses'
            }
    
    @classmethod
    def print_status(cls):
        """Print configuration status"""
        status = cls.validate_config()
        llm_config = cls.get_llm_config()
        
        print("\n" + "="*60)
        print(" SYSTEM CONFIGURATION STATUS")
        print("="*60)
        print(f"\nEnvironment: {status['environment']}")
        print(f"Debug Mode: {cls.DEBUG_MODE}")
        print(f"Log Level: {cls.LOG_LEVEL}")
        
        print(f"\n API Keys:")
        print(f"  Weather: {'✓' if cls.OPENWEATHER_API_KEY else '✗'}")
        print(f"  Anthropic: {'✓' if cls.ANTHROPIC_API_KEY else '✗'}")
        print(f"  OpenAI: {'✓' if cls.OPENAI_API_KEY else '✗'}")
        
        print(f"\n LLM Configuration:")
        print(f"  Provider: {llm_config['provider']}")
        print(f"  Model: {llm_config['model']}")
        print(f"  Available: {'✓' if llm_config['available'] else '✗'}")
        
        print(f"\n Database:")
        print(f"  URL: {cls.DATABASE_URL}")
        
        if status['issues']:
            print(f"\n ❌ CRITICAL ISSUES:")
            for issue in status['issues']:
                print(f"   - {issue}")
        
        if status['warnings']:
            print(f"\n ⚠️  WARNINGS:")
            for warning in status['warnings']:
                print(f"   - {warning}")
        
        if status['valid'] and not status['warnings']:
            print(f"\n ✓ Configuration is valid!")
        
        print("="*60 + "\n")


# ==================== Auto-validation on Import ====================
config_status = Config.validate_config()

if not config_status['valid']:
    print("\n⚠️  CONFIGURATION ISSUES DETECTED:")
    for issue in config_status['issues']:
        print(f"   ❌ {issue}")
    print("\n💡 Please check your .env file\n")
elif config_status['warnings']:
    print("\n⚠️  Configuration Warnings:")
    for warning in config_status['warnings']:
        print(f"   ⚠️  {warning}")
    print()

# Ensure directories exist
Config.ensure_directories()
