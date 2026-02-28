"""
Router de Webhooks - Autobiz
Gerenciamento de webhooks para eventos
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Dict, List, Any, Optional
import structlog
import hmac
import hashlib

from app.config import settings
from app.models.base import get_db
from app.models.tenant import Tenant, TenantConfig, TenantUser
from app.routers.auth import get_current_active_user

logger = structlog.get_logger()
router = APIRouter()


@router.get("/{tenant_id}")
async def list_webhooks(
    tenant_id: str,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Lista webhooks configurados"""
    
    membership = db.query(TenantUser).filter(
        TenantUser.tenant_id == tenant_id,
        TenantUser.user_id == current_user.id,
        TenantUser.role.in_(["admin"]),
        TenantUser.is_active == True
    ).first()
    
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado"
        )
    
    config = db.query(TenantConfig).filter(
        TenantConfig.tenant_id == tenant_id
    ).first()
    
    webhooks = config.webhooks if config else []
    
    return {"webhooks": webhooks}


@router.post("/{tenant_id}")
async def create_webhook(
    tenant_id: str,
    data: Dict[str, Any],
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Cria novo webhook"""
    
    membership = db.query(TenantUser).filter(
        TenantUser.tenant_id == tenant_id,
        TenantUser.user_id == current_user.id,
        TenantUser.role.in_(["admin"]),
        TenantUser.is_active == True
    ).first()
    
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado"
        )
    
    config = db.query(TenantConfig).filter(
        TenantConfig.tenant_id == tenant_id
    ).first()
    
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuração não encontrada"
        )
    
    import uuid
    
    webhook = {
        "id": str(uuid.uuid4()),
        "url": data["url"],
        "events": data.get("events", []),
        "secret": data.get("secret", ""),
        "active": True,
        "created_at": "2024-01-01T00:00:00Z",  # TODO: usar datetime real
    }
    
    if not config.webhooks:
        config.webhooks = []
    
    config.webhooks.append(webhook)
    db.commit()
    
    logger.info(
        "webhook_created",
        tenant_id=tenant_id,
        webhook_id=webhook["id"],
    )
    
    return webhook


@router.put("/{tenant_id}/{webhook_id}")
async def update_webhook(
    tenant_id: str,
    webhook_id: str,
    data: Dict[str, Any],
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Atualiza webhook"""
    
    membership = db.query(TenantUser).filter(
        TenantUser.tenant_id == tenant_id,
        TenantUser.user_id == current_user.id,
        TenantUser.role.in_(["admin"]),
        TenantUser.is_active == True
    ).first()
    
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado"
        )
    
    config = db.query(TenantConfig).filter(
        TenantConfig.tenant_id == tenant_id
    ).first()
    
    if not config or not config.webhooks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Webhook não encontrado"
        )
    
    webhook = None
    for w in config.webhooks:
        if w["id"] == webhook_id:
            webhook = w
            break
    
    if not webhook:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Webhook não encontrado"
        )
    
    # Atualizar campos
    if "url" in data:
        webhook["url"] = data["url"]
    if "events" in data:
        webhook["events"] = data["events"]
    if "active" in data:
        webhook["active"] = data["active"]
    
    db.commit()
    
    logger.info(
        "webhook_updated",
        tenant_id=tenant_id,
        webhook_id=webhook_id,
    )
    
    return webhook


@router.delete("/{tenant_id}/{webhook_id}")
async def delete_webhook(
    tenant_id: str,
    webhook_id: str,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Remove webhook"""
    
    membership = db.query(TenantUser).filter(
        TenantUser.tenant_id == tenant_id,
        TenantUser.user_id = current_user.id,
        TenantUser.role.in_(["admin"]),
        TenantUser.is_active == True
    ).first()
    
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado"
        )
    
    config = db.query(TenantConfig).filter(
        TenantConfig.tenant_id == tenant_id
    ).first()
    
    if not config or not config.webhooks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Webhook não encontrado"
        )
    
    config.webhooks = [w for w in config.webhooks if w["id"] != webhook_id]
    db.commit()
    
    logger.info(
        "webhook_deleted",
        tenant_id=tenant_id,
        webhook_id=webhook_id,
    )
    
    return {"message": "Webhook removido com sucesso"}


@router.post("/{tenant_id}/test/{webhook_id}")
async def test_webhook(
    tenant_id: str,
    webhook_id: str,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Testa webhook enviando evento de teste"""
    
    membership = db.query(TenantUser).filter(
        TenantUser.tenant_id == tenant_id,
        TenantUser.user_id == current_user.id,
        TenantUser.role.in_(["admin"]),
        TenantUser.is_active == True
    ).first()
    
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado"
        )
    
    config = db.query(TenantConfig).filter(
        TenantConfig.tenant_id == tenant_id
    ).first()
    
    if not config or not config.webhooks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Webhook não encontrado"
        )
    
    webhook = None
    for w in config.webhooks:
        if w["id"] == webhook_id:
            webhook = w
            break
    
    if not webhook:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Webhook não encontrado"
        )
    
    # Enviar evento de teste
    import httpx
    
    payload = {
        "event": "test",
        "timestamp": "2024-01-01T00:00:00Z",
        "data": {"message": "Teste de webhook"},
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                webhook["url"],
                json=payload,
                timeout=30
            )
        
        return {
            "success": response.status_code < 400,
            "status_code": response.status_code,
            "response": response.text[:200],
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


@router.get("/events")
async def get_available_events(
    current_user = Depends(get_current_active_user)
):
    """Retorna eventos disponíveis para webhooks"""
    
    events = [
        {
            "category": "Entidades",
            "events": [
                {"name": "entity.created", "description": "Quando qualquer entidade é criada"},
                {"name": "entity.updated", "description": "Quando qualquer entidade é atualizada"},
                {"name": "entity.deleted", "description": "Quando qualquer entidade é removida"},
            ]
        },
        {
            "category": "Vendas",
            "events": [
                {"name": "venda.confirmada", "description": "Quando uma venda é confirmada"},
                {"name": "venda.cancelada", "description": "Quando uma venda é cancelada"},
                {"name": "pagamento.recebido", "description": "Quando um pagamento é recebido"},
            ]
        },
        {
            "category": "Clientes",
            "events": [
                {"name": "cliente.criado", "description": "Quando um cliente é cadastrado"},
                {"name": "cliente.atualizado", "description": "Quando dados do cliente são atualizados"},
            ]
        },
        {
            "category": "Agendamentos",
            "events": [
                {"name": "agendamento.criado", "description": "Novo agendamento criado"},
                {"name": "agendamento.confirmado", "description": "Agendamento confirmado"},
                {"name": "agendamento.cancelado", "description": "Agendamento cancelado"},
            ]
        },
        {
            "category": "Estoque",
            "events": [
                {"name": "estoque.baixo", "description": "Quando estoque fica abaixo do mínimo"},
                {"name": "produto.sem_estoque", "description": "Quando produto fica sem estoque"},
            ]
        },
    ]
    
    return {"events": events}
