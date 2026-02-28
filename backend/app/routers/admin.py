"""
Router de Administração Master - Autobiz
Painel de controle para administradores da plataforma
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import structlog

from app.config import settings
from app.models.base import get_db
from app.models.tenant import Tenant, User, TenantUser
from app.routers.auth import get_current_active_user

logger = structlog.get_logger()
router = APIRouter()


def require_master_admin(current_user: User = Depends(get_current_active_user)):
    """Verifica se usuário é admin master"""
    if not current_user.is_master_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores master"
        )
    return current_user


# Schemas
class TenantStats(BaseModel):
    total_tenants: int
    active_tenants: int
    new_today: int
    new_this_week: int
    new_this_month: int
    by_plan: dict
    by_business_type: dict


class UserStats(BaseModel):
    total_users: int
    active_users: int
    new_today: int
    new_this_month: int


class SystemStats(BaseModel):
    tenants: TenantStats
    users: UserStats
    server_health: dict


class TenantDetail(BaseModel):
    id: str
    name: str
    business_type: str
    plan: str
    is_active: bool
    created_at: datetime
    user_count: int


# Endpoints de Dashboard
@router.get("/dashboard/stats", response_model=SystemStats)
async def get_system_stats(
    current_user: User = Depends(require_master_admin),
    db: Session = Depends(get_db)
):
    """Retorna estatísticas gerais do sistema"""
    
    # Tenant stats
    total_tenants = db.query(Tenant).count()
    active_tenants = db.query(Tenant).filter(Tenant.is_active == True).count()
    
    today = datetime.utcnow().date()
    new_today = db.query(Tenant).filter(
        func.date(Tenant.created_at) == today
    ).count()
    
    week_ago = datetime.utcnow() - timedelta(days=7)
    new_this_week = db.query(Tenant).filter(
        Tenant.created_at >= week_ago
    ).count()
    
    month_ago = datetime.utcnow() - timedelta(days=30)
    new_this_month = db.query(Tenant).filter(
        Tenant.created_at >= month_ago
    ).count()
    
    # Tenants por plano
    by_plan = {}
    for plan in ["free", "starter", "pro", "enterprise"]:
        count = db.query(Tenant).filter(Tenant.plan == plan).count()
        by_plan[plan] = count
    
    # Tenants por tipo de negócio
    by_type = {}
    types = db.query(Tenant.business_type, func.count(Tenant.id)).group_by(Tenant.business_type).all()
    for t, count in types:
        by_type[t] = count
    
    # User stats
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    new_users_today = db.query(User).filter(
        func.date(User.created_at) == today
    ).count()
    new_users_month = db.query(User).filter(
        User.created_at >= month_ago
    ).count()
    
    return {
        "tenants": {
            "total_tenants": total_tenants,
            "active_tenants": active_tenants,
            "new_today": new_today,
            "new_this_week": new_this_week,
            "new_this_month": new_this_month,
            "by_plan": by_plan,
            "by_business_type": by_type,
        },
        "users": {
            "total_users": total_users,
            "active_users": active_users,
            "new_today": new_users_today,
            "new_this_month": new_users_month,
        },
        "server_health": {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
        }
    }


# Endpoints de Tenants
@router.get("/tenants", response_model=List[TenantDetail])
async def list_tenants(
    search: Optional[str] = Query(None, description="Busca por nome"),
    business_type: Optional[str] = Query(None, description="Filtrar por tipo"),
    plan: Optional[str] = Query(None, description="Filtrar por plano"),
    is_active: Optional[bool] = Query(None, description="Filtrar por status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(require_master_admin),
    db: Session = Depends(get_db)
):
    """Lista todos os tenants com filtros"""
    
    query = db.query(Tenant)
    
    if search:
        query = query.filter(Tenant.name.ilike(f"%{search}%"))
    
    if business_type:
        query = query.filter(Tenant.business_type == business_type)
    
    if plan:
        query = query.filter(Tenant.plan == plan)
    
    if is_active is not None:
        query = query.filter(Tenant.is_active == is_active)
    
    tenants = query.order_by(Tenant.created_at.desc()).offset(skip).limit(limit).all()
    
    result = []
    for tenant in tenants:
        user_count = db.query(TenantUser).filter(
            TenantUser.tenant_id == tenant.id
        ).count()
        
        result.append({
            "id": tenant.id,
            "name": tenant.name,
            "business_type": tenant.business_type,
            "plan": tenant.plan,
            "is_active": tenant.is_active,
            "created_at": tenant.created_at,
            "user_count": user_count,
        })
    
    return result


@router.get("/tenants/{tenant_id}")
async def get_tenant_detail(
    tenant_id: str,
    current_user: User = Depends(require_master_admin),
    db: Session = Depends(get_db)
):
    """Retorna detalhes completos de um tenant"""
    
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant não encontrado"
        )
    
    # Contar usuários
    user_count = db.query(TenantUser).filter(
        TenantUser.tenant_id == tenant_id
    ).count()
    
    # Listar usuários
    users = []
    for tu in tenant.users:
        users.append({
            "id": tu.user.id,
            "name": tu.user.name,
            "email": tu.user.email,
            "role": tu.role,
            "is_active": tu.is_active,
        })
    
    return {
        "id": tenant.id,
        "name": tenant.name,
        "slug": tenant.slug,
        "business_type": tenant.business_type,
        "business_size": tenant.business_size,
        "document": tenant.document,
        "email": tenant.email,
        "phone": tenant.phone,
        "plan": tenant.plan,
        "plan_expires_at": tenant.plan_expires_at,
        "is_active": tenant.is_active,
        "is_verified": tenant.is_verified,
        "onboarding_completed": tenant.onboarding_completed,
        "features_enabled": tenant.features_enabled,
        "primary_color": tenant.primary_color,
        "created_at": tenant.created_at,
        "updated_at": tenant.updated_at,
        "user_count": user_count,
        "users": users,
    }


@router.put("/tenants/{tenant_id}")
async def update_tenant(
    tenant_id: str,
    updates: dict,
    current_user: User = Depends(require_master_admin),
    db: Session = Depends(get_db)
):
    """Atualiza dados de um tenant"""
    
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant não encontrado"
        )
    
    # Campos permitidos para atualização
    allowed_fields = ["name", "plan", "is_active", "features_enabled", "primary_color"]
    
    for field, value in updates.items():
        if field in allowed_fields:
            setattr(tenant, field, value)
    
    db.commit()
    db.refresh(tenant)
    
    logger.info("tenant_updated", tenant_id=tenant_id, updated_by=current_user.id)
    
    return {"message": "Tenant atualizado com sucesso"}


@router.delete("/tenants/{tenant_id}")
async def delete_tenant(
    tenant_id: str,
    current_user: User = Depends(require_master_admin),
    db: Session = Depends(get_db)
):
    """Remove um tenant e todos seus dados"""
    
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant não encontrado"
        )
    
    # TODO: Fazer backup antes de deletar
    
    db.delete(tenant)
    db.commit()
    
    logger.info("tenant_deleted", tenant_id=tenant_id, deleted_by=current_user.id)
    
    return {"message": "Tenant removido com sucesso"}


# Endpoints de Usuários
@router.get("/users")
async def list_users(
    search: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(require_master_admin),
    db: Session = Depends(get_db)
):
    """Lista todos os usuários"""
    
    query = db.query(User)
    
    if search:
        query = query.filter(
            (User.name.ilike(f"%{search}%")) |
            (User.email.ilike(f"%{search}%"))
        )
    
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    
    users = query.order_by(User.created_at.desc()).offset(skip).limit(limit).all()
    
    return [
        {
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "phone": u.phone,
            "is_active": u.is_active,
            "is_email_verified": u.is_email_verified,
            "last_login_at": u.last_login_at,
            "created_at": u.created_at,
            "tenant_count": len([m for m in u.tenant_memberships if m.is_active]),
        }
        for u in users
    ]


@router.get("/users/{user_id}")
async def get_user_detail(
    user_id: str,
    current_user: User = Depends(require_master_admin),
    db: Session = Depends(get_db)
):
    """Retorna detalhes de um usuário"""
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    tenants = []
    for membership in user.tenant_memberships:
        tenants.append({
            "id": membership.tenant.id,
            "name": membership.tenant.name,
            "role": membership.role,
            "is_active": membership.is_active,
        })
    
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "avatar_url": user.avatar_url,
        "is_active": user.is_active,
        "is_email_verified": user.is_email_verified,
        "is_master_admin": user.is_master_admin,
        "last_login_at": user.last_login_at,
        "last_login_ip": user.last_login_ip,
        "created_at": user.created_at,
        "tenants": tenants,
    }


@router.put("/users/{user_id}")
async def update_user(
    user_id: str,
    updates: dict,
    current_user: User = Depends(require_master_admin),
    db: Session = Depends(get_db)
):
    """Atualiza dados de um usuário"""
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    allowed_fields = ["name", "phone", "is_active", "is_master_admin"]
    
    for field, value in updates.items():
        if field in allowed_fields:
            setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    logger.info("user_updated", user_id=user_id, updated_by=current_user.id)
    
    return {"message": "Usuário atualizado com sucesso"}


# Endpoints de Configurações
@router.get("/settings")
async def get_platform_settings(
    current_user: User = Depends(require_master_admin)
):
    """Retorna configurações da plataforma"""
    
    return {
        "app_name": settings.APP_NAME,
        "app_version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "default_tenant_plan": settings.DEFAULT_TENANT_PLAN,
        "features": {
            "tenant_subdomain": settings.TENANT_SUBDOMAIN_ENABLED,
        },
        "integrations": {
            "mercadopago": bool(settings.MERCADOPAGO_ACCESS_TOKEN),
            "twilio": bool(settings.TWILIO_ACCOUNT_SID),
            "openai": bool(settings.OPENAI_API_KEY),
        }
    }


@router.post("/settings")
async def update_platform_settings(
    settings_update: dict,
    current_user: User = Depends(require_master_admin)
):
    """Atualiza configurações da plataforma"""
    
    # TODO: Implementar atualização de configurações
    
    logger.info("settings_updated", updated_by=current_user.id)
    
    return {"message": "Configurações atualizadas"}


# Endpoints de Logs
@router.get("/logs")
async def get_system_logs(
    level: Optional[str] = Query(None, description="Nível do log"),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(require_master_admin)
):
    """Retorna logs do sistema"""
    
    # TODO: Implementar consulta a logs
    
    return {
        "logs": [],
        "total": 0,
    }


# Endpoints de Manutenção
@router.post("/maintenance/backup")
async def create_backup(
    current_user: User = Depends(require_master_admin)
):
    """Inicia backup do sistema"""
    
    logger.info("backup_started", started_by=current_user.id)
    
    # TODO: Implementar backup
    
    return {"message": "Backup iniciado", "backup_id": "backup_001"}


@router.post("/maintenance/cleanup")
async def run_cleanup(
    current_user: User = Depends(require_master_admin)
):
    """Executa limpeza de dados antigos"""
    
    logger.info("cleanup_started", started_by=current_user.id)
    
    # TODO: Implementar limpeza
    
    return {"message": "Limpeza concluída"}
