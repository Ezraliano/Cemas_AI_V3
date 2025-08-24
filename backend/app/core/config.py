from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/cemas_ai")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-for-jwt")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # AI Services
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL_NAME: str = os.getenv("GROQ_MODEL_NAME", "meta-llama/llama-4-maverick-17b-128e-instruct")
    
    # Application
    APP_NAME: str = "Cemas.AI"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "AI-powered mental health assistant"
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "https://cemas-ai.vercel.app"]
    
    # JWT specific settings (to handle environment variables)
    JWT_SECRET: str = "supersecretkey"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60
    DEBUG: bool = False
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "ignore"
    }

settings = Settings()