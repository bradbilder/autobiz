"""
Router de Onboarding - Fluxo de criação de sistema personalizado
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import structlog

from app.config import settings
from app.models.base import get_db
from app.models.tenant import Tenant, TenantConfig, TenantUser, User
from app.core.engine import AutoModelEngine
from app.routers.auth import get_current_active_user

logger = structlog.get_logger()
router = APIRouter()

# Inicializar motor
engine = AutoModelEngine()


# Schemas
class BusinessInfo(BaseModel):
    business_type: str = Field(..., description="Tipo de negócio")
    business_size: str = Field(default="small", description="Tamanho do negócio")
    name: str = Field(..., description="Nome da empresa")
    document: Optional[str] = Field(None, description="CNPJ/CPF")
    phone: Optional[str] = Field(None, description="Telefone")
    email: Optional[str] = Field(None, description="Email comercial")


class OnboardingAnswers(BaseModel):
    business_info: BusinessInfo
    custom_fields: Optional[List[Dict[str, Any]]] = []
    branding: Optional[Dict[str, Any]] = {}
    features: Optional[List[str]] = []
    integrations: Optional[List[str]] = []


class OnboardingResponse(BaseModel):
    tenant_id: str
    status: str
    message: str
    system_config: Optional[Dict[str, Any]] = None


class QuestionStep(BaseModel):
    id: str
    title: str
    description: str
    fields: List[Dict[str, Any]]


@router.get("/questions")
async def get_onboarding_questions():
    """Retorna as perguntas do fluxo de onboarding"""
    steps = [
        {
            "id": "business_type",
            "title": "Qual é o seu tipo de negócio?",
            "description": "Selecione a categoria que melhor descreve sua empresa",
            "fields": [
                {
                    "name": "business_type",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": "varejo", "label": "Varejo/Loja", "icon": "ShoppingBag"},
                        {"value": "ecommerce", "label": "E-commerce", "icon": "Globe"},
                        {"value": "servicos", "label": "Prestação de Serviços", "icon": "Briefcase"},
                        {"value": "consultoria", "label": "Consultoria", "icon": "Users"},
                        {"value": "restaurante", "label": "Restaurante/Delivery", "icon": "Utensils"},
                        {"value": "clinica", "label": "Clínica Médica", "icon": "Heart"},
                        {"value": "imobiliaria", "label": "Imobiliária", "icon": "Home"},
                        {"value": "construcao", "label": "Construção Civil", "icon": "Building"},
                        {"value": "escola", "label": "Escola/Instituição", "icon": "GraduationCap"},
                        {"value": "academia", "label": "Academia", "icon": "Dumbbell"},
                        {"value": "salao", "label": "Salão de Beleza", "icon": "Scissors"},
                        {"value": "oficina", "label": "Oficina Mecânica", "icon": "Wrench"},
                    ]
                }
            ]
        },
        {
            "id": "business_info",
            "title": "Informações da Empresa",
            "description": "Conte-nos um pouco sobre sua empresa",
            "fields": [
                {
                    "name": "name",
                    "type": "string",
                    "label": "Nome da Empresa",
                    "required": True,
                    "placeholder": "Ex: Minha Empresa LTDA"
                },
                {
                    "name": "business_size",
                    "type": "select",
                    "label": "Tamanho da Empresa",
                    "required": True,
                    "options": [
                        {"value": "small", "label": "Pequena (1-10 funcionários)"},
                        {"value": "medium", "label": "Média (11-50 funcionários)"},
                        {"value": "large", "label": "Grande (51+ funcionários)"},
                    ]
                },
                {
                    "name": "document",
                    "type": "string",
                    "label": "CNPJ/CPF",
                    "required": False,
                    "placeholder": "00.000.000/0000-00"
                },
                {
                    "name": "phone",
                    "type": "phone",
                    "label": "Telefone",
                    "required": False,
                    "placeholder": "(00) 00000-0000"
                },
            ]
        },
        {
            "id": "features",
            "title": "Quais funcionalidades você precisa?",
            "description": "Selecione os recursos que deseja utilizar",
            "fields": [
                {
                    "name": "features",
                    "type": "multiselect",
                    "required": True,
                    "options": [
                        {"value": "vendas", "label": "Controle de Vendas", "icon": "ShoppingCart"},
                        {"value": "estoque", "label": "Gestão de Estoque", "icon": "Package"},
                        {"value": "clientes", "label": "Cadastro de Clientes", "icon": "Users"},
                        {"value": "agendamentos", "label": "Agendamentos", "icon": "Calendar"},
                        {"value": "financeiro", "label": "Controle Financeiro", "icon": "DollarSign"},
                        {"value": "relatorios", "label": "Relatórios", "icon": "BarChart"},
                        {"value": "usuarios", "label": "Multi-usuários", "icon": "UserPlus"},
                        {"value": "api", "label": "API de Integração", "icon": "Code"},
                    ]
                }
            ]
        },
        {
            "id": "branding",
            "title": "Personalização",
            "description": "Personalize a aparência do seu sistema",
            "fields": [
                {
                    "name": "primary_color",
                    "type": "color",
                    "label": "Cor Principal",
                    "required": False,
                    "default": "#2563eb"
                },
                {
                    "name": "logo",
                    "type": "image",
                    "label": "Logo da Empresa",
                    "required": False,
                },
            ]
        },
        {
            "id": "integrations",
            "title": "Integrações",
            "description": "Quais integrações você gostaria de configurar?",
            "fields": [
                {
                    "name": "integrations",
                    "type": "multiselect",
                    "required": False,
                    "options": [
                        {"value": "whatsapp", "label": "WhatsApp Business", "icon": "MessageCircle"},
                        {"value": "mercadopago", "label": "Mercado Pago", "icon": "CreditCard"},
                        {"value": "google_calendar", "label": "Google Calendar", "icon": "Calendar"},
                        {"value": "email", "label": "Email Marketing", "icon": "Mail"},
                    ]
                }
            ]
        },
    ]
    
    return {"steps": steps}


@router.post("/create", response_model=OnboardingResponse)
async def create_system(
    data: OnboardingAnswers,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Cria um novo sistema personalizado baseado nas respostas do onboarding
    """
    logger.info(
        "onboarding_create_system",
        user_id=current_user.id,
        business_type=data.business_info.business_type,
    )
    
    try:
        # 1. Criar tenant
        tenant = Tenant(
            name=data.business_info.name,
            slug=data.business_info.name.lower().replace(" ", "-"),
            business_type=data.business_info.business_type,
            business_size=data.business_info.business_size,
            document=data.business_info.document,
            phone=data.business_info.phone,
            email=data.business_info.email or current_user.email,
            plan=settings.DEFAULT_TENANT_PLAN,
            onboarding_data=data.dict(),
            primary_color=data.branding.get("primary_color", "#2563eb") if data.branding else "#2563eb",
        )
        
        db.add(tenant)
        db.commit()
        db.refresh(tenant)
        
        logger.info("tenant_created", tenant_id=tenant.id)
        
        # 2. Vincular usuário ao tenant como admin
        tenant_user = TenantUser(
            tenant_id=tenant.id,
            user_id=current_user.id,
            role="admin",
            permissions=["*"],
        )
        
        db.add(tenant_user)
        db.commit()
        
        # 3. Gerar sistema usando o motor auto-modelável
        onboarding_data = data.dict()
        system_config = await engine.generate_system(
            tenant_id=tenant.id,
            onboarding_data=onboarding_data
        )
        
        # 4. Salvar configuração do sistema
        tenant_config = TenantConfig(
            tenant_id=tenant.id,
            ui_config=system_config.get("ui_configuration"),
            database_schema=system_config.get("database_schema"),
            api_config=system_config.get("api_configuration"),
            integrations={"enabled": data.integrations or []},
        )
        
        db.add(tenant_config)
        
        # 5. Marcar onboarding como completo
        tenant.onboarding_completed = True
        db.commit()
        
        logger.info(
            "system_created_successfully",
            tenant_id=tenant.id,
            features_count=len(system_config.get("features_enabled", [])),
        )
        
        return OnboardingResponse(
            tenant_id=tenant.id,
            status="success",
            message="Sistema criado com sucesso!",
            system_config={
                "features_enabled": system_config.get("features_enabled"),
                "integrations_suggested": system_config.get("integrations_suggested"),
                "tenant": {
                    "id": tenant.id,
                    "name": tenant.name,
                    "slug": tenant.slug,
                }
            }
        )
        
    except Exception as e:
        logger.error(
            "onboarding_failed",
            user_id=current_user.id,
            error=str(e),
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar sistema: {str(e)}"
        )


@router.get("/templates")
async def get_templates():
    """Retorna templates disponíveis para cada tipo de negócio"""
    from app.core.template_library import TemplateLibrary
    
    library = TemplateLibrary()
    await library.load_templates()
    
    templates = library.get_all_templates()
    
    return {"templates": templates}


@router.get("/status/{tenant_id}")
async def get_onboarding_status(
    tenant_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Retorna o status do onboarding de um tenant"""
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant não encontrado"
        )
    
    # Verificar se usuário tem acesso
    membership = db.query(TenantUser).filter(
        TenantUser.tenant_id == tenant_id,
        TenantUser.user_id == current_user.id
    ).first()
    
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado"
        )
    
    return {
        "tenant_id": tenant.id,
        "onboarding_completed": tenant.onboarding_completed,
        "business_type": tenant.business_type,
        "features_enabled": tenant.features_enabled,
        "created_at": tenant.created_at,
    }
