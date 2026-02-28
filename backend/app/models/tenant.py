"""
Modelos de Tenant e configurações multi-tenant
"""
from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, JSON, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.base import BaseModel


class Tenant(BaseModel):
    """Modelo de Tenant (cliente/empresa)"""
    __tablename__ = "tenants"
    
    # Identificação
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    subdomain = Column(String(100), unique=True, nullable=True)
    
    # Dados do negócio
    business_type = Column(String(50), nullable=False)
    business_size = Column(String(20), default="small")
    document = Column(String(20), nullable=True)  # CNPJ/CPF
    
    # Contato
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    
    # Endereço
    address = Column(JSON, nullable=True)
    
    # Configurações
    settings = Column(JSON, default=dict)
    features_enabled = Column(JSON, default=list)
    
    # Plano e faturamento
    plan = Column(String(20), default="free")
    plan_expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Onboarding
    onboarding_completed = Column(Boolean, default=False)
    onboarding_data = Column(JSON, default=dict)
    
    # Branding
    logo_url = Column(String(500), nullable=True)
    primary_color = Column(String(7), default="#2563eb")
    
    # Relacionamentos
    users = relationship("TenantUser", back_populates="tenant", cascade="all, delete-orphan")
    config = relationship("TenantConfig", back_populates="tenant", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Tenant {self.name}>"


class TenantConfig(BaseModel):
    """Configurações específicas do tenant"""
    __tablename__ = "tenant_configs"
    
    tenant_id = Column(String(36), ForeignKey("tenants.id"), nullable=False, unique=True)
    
    # Configurações de UI
    ui_config = Column(JSON, default=dict)
    theme = Column(JSON, default=dict)
    
    # Configurações de API
    api_config = Column(JSON, default=dict)
    
    # Schema de banco de dados
    database_schema = Column(JSON, default=dict)
    
    # Integrações
    integrations = Column(JSON, default=dict)
    
    # Webhooks
    webhooks = Column(JSON, default=list)
    
    # Relacionamento
    tenant = relationship("Tenant", back_populates="config")


class TenantUser(BaseModel):
    """Usuários vinculados a um tenant"""
    __tablename__ = "tenant_users"
    
    tenant_id = Column(String(36), ForeignKey("tenants.id"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    
    # Permissões no tenant
    role = Column(String(50), default="member")  # admin, manager, member
    permissions = Column(JSON, default=list)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Relacionamentos
    tenant = relationship("Tenant", back_populates="users")
    user = relationship("User", back_populates="tenant_memberships")


class User(BaseModel):
    """Modelo de Usuário (global)"""
    __tablename__ = "users"
    
    # Dados pessoais
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    
    # Autenticação
    password_hash = Column(String(255), nullable=False)
    
    # Perfil
    avatar_url = Column(String(500), nullable=True)
    preferences = Column(JSON, default=dict)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_email_verified = Column(Boolean, default=False)
    is_master_admin = Column(Boolean, default=False)
    
    # Segurança
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    last_login_ip = Column(String(45), nullable=True)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime(timezone=True), nullable=True)
    
    # 2FA
    two_factor_enabled = Column(Boolean, default=False)
    two_factor_secret = Column(String(255), nullable=True)
    
    # Relacionamentos
    tenant_memberships = relationship("TenantUser", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.email}>"
