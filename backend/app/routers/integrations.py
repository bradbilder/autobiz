"""
Router de Integrações - Autobiz
WhatsApp, Mercado Pago e outras integrações
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.orm import Session
from typing import Dict, List, Any, Optional
import structlog

from app.config import settings
from app.models.base import get_db
from app.models.tenant import Tenant, TenantConfig, TenantUser
from app.routers.auth import get_current_active_user
from app.services.integration_service import IntegrationService

logger = structlog.get_logger()
router = APIRouter()

integration_service = IntegrationService()


# ==================== WHATSAPP ====================

@router.get("/{tenant_id}/whatsapp/status")
async def whatsapp_status(
    tenant_id: str,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Retorna status da integração com WhatsApp"""
    
    membership = db.query(TenantUser).filter(
        TenantUser.tenant_id == tenant_id,
        TenantUser.user_id == current_user.id,
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
    
    whatsapp_config = config.integrations.get("whatsapp", {}) if config else {}
    
    return {
        "enabled": whatsapp_config.get("enabled", False),
        "connected": whatsapp_config.get("connected", False),
        "phone_number": whatsapp_config.get("phone_number"),
        "message_templates_count": len(whatsapp_config.get("templates", [])),
    }


@router.post("/{tenant_id}/whatsapp/connect")
async def whatsapp_connect(
    tenant_id: str,
    data: Dict[str, Any],
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Conecta conta do WhatsApp Business"""
    
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
    
    # Configurar Twilio/WhatsApp
    result = await integration_service.configure_whatsapp(
        tenant_id=tenant_id,
        phone_number=data.get("phone_number"),
        api_key=data.get("api_key"),
    )
    
    logger.info("whatsapp_connected", tenant_id=tenant_id)
    
    return result


@router.post("/{tenant_id}/whatsapp/send")
async def whatsapp_send_message(
    tenant_id: str,
    data: Dict[str, Any],
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Envia mensagem via WhatsApp"""
    
    membership = db.query(TenantUser).filter(
        TenantUser.tenant_id == tenant_id,
        TenantUser.user_id == current_user.id,
        TenantUser.is_active == True
    ).first()
    
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado"
        )
    
    result = await integration_service.send_whatsapp_message(
        tenant_id=tenant_id,
        to=data.get("to"),
        message=data.get("message"),
        template=data.get("template"),
    )
    
    return result


@router.get("/{tenant_id}/whatsapp/templates")
async def whatsapp_get_templates(
    tenant_id: str,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Retorna templates de mensagens do WhatsApp"""
    
    membership = db.query(TenantUser).filter(
        TenantUser.tenant_id == tenant_id,
        TenantUser.user_id == current_user.id,
        TenantUser.is_active == True
    ).first()
    
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado"
        )
    
    templates = await integration_service.get_whatsapp_templates(tenant_id)
    
    return {"templates": templates}


# ==================== MERCADO PAGO ====================

@router.get("/{tenant_id}/mercadopago/status")
async def mercadopago_status(
    tenant_id: str,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Retorna status da integração com Mercado Pago"""
    
    membership = db.query(TenantUser).filter(
        TenantUser.tenant_id == tenant_id,
        TenantUser.user_id == current_user.id,
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
    
    mp_config = config.integrations.get("mercadopago", {}) if config else {}
    
    return {
        "enabled": mp_config.get("enabled", False),
        "connected": mp_config.get("connected", False),
        "public_key": mp_config.get("public_key"),
        "sandbox_mode": mp_config.get("sandbox_mode", True),
    }


@router.post("/{tenant_id}/mercadopago/connect")
async def mercadopago_connect(
    tenant_id: str,
    data: Dict[str, Any],
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Conecta conta do Mercado Pago"""
    
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
    
    result = await integration_service.configure_mercadopago(
        tenant_id=tenant_id,
        access_token=data.get("access_token"),
        public_key=data.get("public_key"),
        sandbox_mode=data.get("sandbox_mode", True),
    )
    
    logger.info("mercadopago_connected", tenant_id=tenant_id)
    
    return result


@router.post("/{tenant_id}/mercadopago/create-preference")
async def mercadopago_create_preference(
    tenant_id: str,
    data: Dict[str, Any],
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Cria preferência de pagamento no Mercado Pago"""
    
    membership = db.query(TenantUser).filter(
        TenantUser.tenant_id == tenant_id,
        TenantUser.user_id == current_user.id,
        TenantUser.is_active == True
    ).first()
    
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado"
        )
    
    result = await integration_service.create_mercadopago_preference(
        tenant_id=tenant_id,
        items=data.get("items", []),
        payer=data.get("payer", {}),
        external_reference=data.get("external_reference"),
    )
    
    return result


@router.post("/webhooks/mercadopago")
async def mercadopago_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """Webhook para notificações do Mercado Pago"""
    
    payload = await request.json()
    
    logger.info("mercadopago_webhook_received", data=payload)
    
    # Processar notificação
    await integration_service.process_mercadopago_notification(payload)
    
    return {"status": "ok"}


# ==================== GOOGLE CALENDAR ====================

@router.get("/{tenant_id}/google-calendar/status")
async def google_calendar_status(
    tenant_id: str,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Retorna status da integração com Google Calendar"""
    
    membership = db.query(TenantUser).filter(
        TenantUser.tenant_id == tenant_id,
        TenantUser.user_id == current_user.id,
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
    
    gc_config = config.integrations.get("google_calendar", {}) if config else {}
    
    return {
        "enabled": gc_config.get("enabled", False),
        "connected": gc_config.get("connected", False),
        "email": gc_config.get("email"),
    }


@router.post("/{tenant_id}/google-calendar/connect")
async def google_calendar_connect(
    tenant_id: str,
    data: Dict[str, Any],
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Conecta conta do Google Calendar"""
    
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
    
    result = await integration_service.configure_google_calendar(
        tenant_id=tenant_id,
        credentials=data.get("credentials"),
    )
    
    logger.info("google_calendar_connected", tenant_id=tenant_id)
    
    return result


# ==================== EMAIL MARKETING ====================

@router.get("/{tenant_id}/email/status")
async def email_status(
    tenant_id: str,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Retorna status da integração de Email"""
    
    membership = db.query(TenantUser).filter(
        TenantUser.tenant_id == tenant_id,
        TenantUser.user_id == current_user.id,
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
    
    email_config = config.integrations.get("email", {}) if config else {}
    
    return {
        "enabled": email_config.get("enabled", False),
        "provider": email_config.get("provider"),
        "from_email": email_config.get("from_email"),
    }


@router.post("/{tenant_id}/email/send")
async def email_send(
    tenant_id: str,
    data: Dict[str, Any],
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Envia email"""
    
    membership = db.query(TenantUser).filter(
        TenantUser.tenant_id == tenant_id,
        TenantUser.user_id == current_user.id,
        TenantUser.is_active == True
    ).first()
    
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado"
        )
    
    result = await integration_service.send_email(
        tenant_id=tenant_id,
        to=data.get("to"),
        subject=data.get("subject"),
        body=data.get("body"),
        template=data.get("template"),
        variables=data.get("variables", {}),
    )
    
    return result


# ==================== GERAL ====================

@router.get("/{tenant_id}/available")
async def get_available_integrations(
    tenant_id: str,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Retorna integrações disponíveis para o tenant"""
    
    membership = db.query(TenantUser).filter(
        TenantUser.tenant_id == tenant_id,
        TenantUser.user_id == current_user.id,
        TenantUser.is_active == True
    ).first()
    
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado"
        )
    
    integrations = [
        {
            "id": "whatsapp",
            "name": "WhatsApp Business",
            "description": "Envie mensagens e notificações via WhatsApp",
            "icon": "MessageCircle",
            "category": "comunicacao",
            "configured": bool(settings.TWILIO_ACCOUNT_SID),
        },
        {
            "id": "mercadopago",
            "name": "Mercado Pago",
            "description": "Receba pagamentos online",
            "icon": "CreditCard",
            "category": "pagamento",
            "configured": bool(settings.MERCADOPAGO_ACCESS_TOKEN),
        },
        {
            "id": "google_calendar",
            "name": "Google Calendar",
            "description": "Sincronize agendamentos",
            "icon": "Calendar",
            "category": "produtividade",
            "configured": True,
        },
        {
            "id": "email",
            "name": "Email Marketing",
            "description": "Envie campanhas de email",
            "icon": "Mail",
            "category": "marketing",
            "configured": bool(settings.SMTP_USER),
        },
    ]
    
    return {"integrations": integrations}


@router.get("/{tenant_id}/configured")
async def get_configured_integrations(
    tenant_id: str,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Retorna integrações configuradas do tenant"""
    
    membership = db.query(TenantUser).filter(
        TenantUser.tenant_id == tenant_id,
        TenantUser.user_id == current_user.id,
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
    
    integrations = config.integrations if config else {}
    
    configured = []
    for key, value in integrations.items():
        if value.get("enabled"):
            configured.append({
                "id": key,
                "name": key.replace("_", " ").title(),
                "connected": value.get("connected", False),
            })
    
    return {"integrations": configured}
