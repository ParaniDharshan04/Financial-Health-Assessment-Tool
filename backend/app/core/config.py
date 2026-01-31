from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    GEMINI_API_KEY: str
    ENVIRONMENT: str = "development"
    
    # Plaid Banking API (Optional)
    PLAID_CLIENT_ID: Optional[str] = None
    PLAID_SECRET: Optional[str] = None
    PLAID_ENV: Optional[str] = "https://sandbox.plaid.com"
    
    class Config:
        env_file = ".env"
        extra = "allow"  # Allow extra fields

settings = Settings()
