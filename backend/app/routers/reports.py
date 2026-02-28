"""
Router de Relatórios - Autobiz
Geração de relatórios e dashboards
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Dict, List, Any, Optional
from datetime import datetime, date
import structlog

from app.models.base import get_db
from app.models.tenant import Tenant, TenantConfig, TenantUser
from app.routers.auth import get_current_active_user
from app.services.report_generator import ReportGenerator

logger = structlog.get_logger()
router = APIRouter()


@router.get("/{tenant_id}/dashboard")
async def get_dashboard_data(
    tenant_id: str,
    period: str = Query("month", description="Período: day, week, month, year"),
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Retorna dados para o dashboard"""
    
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
    
    generator = ReportGenerator(tenant_id)
    
    # KPIs
    kpis = await generator.get_kpis(period)
    
    # Gráficos
    charts = await generator.get_charts(period)
    
    # Atividades recentes
    activities = await generator.get_recent_activities()
    
    # Alertas
    alerts = await generator.get_alerts()
    
    return {
        "period": period,
        "kpis": kpis,
        "charts": charts,
        "activities": activities,
        "alerts": alerts,
    }


@router.get("/{tenant_id}/vendas/por-periodo")
async def report_vendas_por_periodo(
    tenant_id: str,
    data_inicio: date = Query(...),
    data_fim: date = Query(...),
    formato: str = Query("json", regex="^(json|csv|pdf|xlsx)$"),
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Relatório de vendas por período"""
    
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
    
    generator = ReportGenerator(tenant_id)
    report = await generator.vendas_por_periodo(data_inicio, data_fim)
    
    if formato == "json":
        return report
    
    # TODO: Implementar exportação para outros formatos
    
    return report


@router.get("/{tenant_id}/vendas/por-produto")
async def report_vendas_por_produto(
    tenant_id: str,
    data_inicio: date = Query(...),
    data_fim: date = Query(...),
    limit: int = Query(20, ge=1, le=100),
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Relatório de vendas por produto"""
    
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
    
    generator = ReportGenerator(tenant_id)
    report = await generator.vendas_por_produto(data_inicio, data_fim, limit)
    
    return report


@router.get("/{tenant_id}/financeiro/fluxo-caixa")
async def report_fluxo_caixa(
    tenant_id: str,
    data_inicio: date = Query(...),
    data_fim: date = Query(...),
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Relatório de fluxo de caixa"""
    
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
    
    generator = ReportGenerator(tenant_id)
    report = await generator.fluxo_caixa(data_inicio, data_fim)
    
    return report


@router.get("/{tenant_id}/estoque/posicao")
async def report_estoque(
    tenant_id: str,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Relatório de posição de estoque"""
    
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
    
    generator = ReportGenerator(tenant_id)
    report = await generator.posicao_estoque()
    
    return report


@router.get("/{tenant_id}/clientes/analise")
async def report_analise_clientes(
    tenant_id: str,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Análise de clientes"""
    
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
    
    generator = ReportGenerator(tenant_id)
    report = await generator.analise_clientes()
    
    return report


@router.post("/{tenant_id}/custom")
async def create_custom_report(
    tenant_id: str,
    config: Dict[str, Any],
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Cria um relatório customizado"""
    
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
    
    generator = ReportGenerator(tenant_id)
    report = await generator.custom_report(config)
    
    return report


@router.get("/{tenant_id}/available")
async def get_available_reports(
    tenant_id: str,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Retorna relatórios disponíveis para o tenant"""
    
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
    
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    
    # Relatórios baseados no tipo de negócio
    reports = [
        {
            "id": "dashboard",
            "name": "Dashboard",
            "description": "Visão geral do negócio",
            "icon": "LayoutDashboard",
        },
        {
            "id": "vendas-por-periodo",
            "name": "Vendas por Período",
            "description": "Análise de vendas ao longo do tempo",
            "icon": "TrendingUp",
        },
        {
            "id": "vendas-por-produto",
            "name": "Vendas por Produto",
            "description": "Produtos mais vendidos",
            "icon": "Package",
        },
    ]
    
    if tenant.business_type in ["varejo", "ecommerce"]:
        reports.extend([
            {
                "id": "estoque",
                "name": "Posição de Estoque",
                "description": "Situação atual do estoque",
                "icon": "Warehouse",
            },
            {
                "id": "curva-abc",
                "name": "Curva ABC",
                "description": "Classificação de produtos",
                "icon": "PieChart",
            },
        ])
    
    if tenant.business_type in ["servicos", "consultoria"]:
        reports.extend([
            {
                "id": "agendamentos",
                "name": "Agendamentos",
                "description": "Análise de agendamentos",
                "icon": "Calendar",
            },
        ])
    
    reports.extend([
        {
            "id": "clientes",
            "name": "Análise de Clientes",
            "description": "Comportamento e segmentação",
            "icon": "Users",
        },
        {
            "id": "financeiro",
            "name": "Fluxo de Caixa",
            "description": "Movimentação financeira",
            "icon": "DollarSign",
        },
    ])
    
    return {"reports": reports}
