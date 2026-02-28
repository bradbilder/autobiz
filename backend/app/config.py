"""
Configurações centralizadas do Autobiz
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List, Optional
import os


class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # App
    APP_NAME: str = "Autobiz"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    
    # Segurança
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 horas
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Banco de Dados
    DATABASE_URL: str = "postgresql://autobiz:autobiz@localhost:5432/autobiz"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    
    # Mercado Pago
    MERCADOPAGO_ACCESS_TOKEN: Optional[str] = None
    MERCADOPAGO_PUBLIC_KEY: Optional[str] = None
    MERCADOPAGO_WEBHOOK_SECRET: Optional[str] = None
    
    # Twilio (WhatsApp)
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_WHATSAPP_NUMBER: Optional[str] = None
    
    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    # Frontend
    FRONTEND_URL: str = "http://localhost:5173"
    
    # Storage
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # Plugins
    PLUGINS_DIR: str = "./plugins"
    ENABLED_PLUGINS: List[str] = []
    
    # Admin Master
    ADMIN_MASTER_EMAIL: str = "admin@autobiz.com"
    ADMIN_MASTER_PASSWORD: str = "admin123"  # Mudar em produção!
    
    # Tenant
    DEFAULT_TENANT_PLAN: str = "free"
    TENANT_SUBDOMAIN_ENABLED: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Retorna instância cacheada das configurações"""
    return Settings()


settings = get_settings()
