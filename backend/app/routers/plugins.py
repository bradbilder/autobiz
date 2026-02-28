"""
Router de Plugins - Autobiz
Sistema de extensões e plugins
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import Dict, List, Any, Optional
import structlog

from app.models.base import get_db
from app.models.tenant import Tenant, TenantConfig, TenantUser
from app.routers.auth import get_current_active_user
from app.plugins.manager import PluginManager

logger = structlog.get_logger()
router = APIRouter()

plugin_manager = PluginManager()


@router.get("/available")
async def get_available_plugins(
    current_user = Depends(get_current_active_user)
):
    """Retorna plugins disponíveis na plataforma"""
    
    plugins = await plugin_manager.get_available_plugins()
    
    return {"plugins": plugins}


@router.get("/{tenant_id}/installed")
async def get_installed_plugins(
    tenant_id: str,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Retorna plugins instalados no tenant"""
    
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
    
    installed = config.integrations.get("plugins", []) if config else []
    
    return {"plugins": installed}


@router.post("/{tenant_id}/install")
async def install_plugin(
    tenant_id: str,
    data: Dict[str, Any],
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Instala um plugin no tenant"""
    
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
    
    plugin_id = data.get("plugin_id")
    
    result = await plugin_manager.install_plugin(
        tenant_id=tenant_id,
        plugin_id=plugin_id,
        config=data.get("config", {})
    )
    
    logger.info(
        "plugin_installed",
        tenant_id=tenant_id,
        plugin_id=plugin_id,
        user_id=current_user.id,
    )
    
    return result


@router.post("/{tenant_id}/uninstall")
async def uninstall_plugin(
    tenant_id: str,
    data: Dict[str, Any],
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Desinstala um plugin do tenant"""
    
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
    
    plugin_id = data.get("plugin_id")
    
    result = await plugin_manager.uninstall_plugin(
        tenant_id=tenant_id,
        plugin_id=plugin_id,
    )
    
    logger.info(
        "plugin_uninstalled",
        tenant_id=tenant_id,
        plugin_id=plugin_id,
        user_id=current_user.id,
    )
    
    return result


@router.put("/{tenant_id}/configure")
async def configure_plugin(
    tenant_id: str,
    data: Dict[str, Any],
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Configura um plugin instalado"""
    
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
    
    plugin_id = data.get("plugin_id")
    config = data.get("config", {})
    
    result = await plugin_manager.configure_plugin(
        tenant_id=tenant_id,
        plugin_id=plugin_id,
        config=config,
    )
    
    return result


@router.post("/{tenant_id}/execute")
async def execute_plugin_action(
    tenant_id: str,
    data: Dict[str, Any],
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Executa uma ação de plugin"""
    
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
    
    plugin_id = data.get("plugin_id")
    action = data.get("action")
    params = data.get("params", {})
    
    result = await plugin_manager.execute_action(
        tenant_id=tenant_id,
        plugin_id=plugin_id,
        action=action,
        params=params,
    )
    
    return result


# Admin endpoints
@router.post("/admin/upload")
async def upload_plugin(
    file: UploadFile = File(...),
    current_user = Depends(get_current_active_user)
):
    """Upload de novo plugin (admin apenas)"""
    
    if not current_user.is_master_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado"
        )
    
    result = await plugin_manager.upload_plugin(file)
    
    logger.info(
        "plugin_uploaded",
        filename=file.filename,
        user_id=current_user.id,
    )
    
    return result


@router.delete("/admin/{plugin_id}")
async def delete_plugin(
    plugin_id: str,
    current_user = Depends(get_current_active_user)
):
    """Remove um plugin da plataforma (admin apenas)"""
    
    if not current_user.is_master_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado"
        )
    
    result = await plugin_manager.delete_plugin(plugin_id)
    
    logger.info(
        "plugin_deleted",
        plugin_id=plugin_id,
        user_id=current_user.id,
    )
    
    return result
