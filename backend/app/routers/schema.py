"""
Router de Schema Dinâmico - Autobiz
Gerenciamento de schemas de banco de dados
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, List, Any, Optional
import structlog

from app.models.base import get_db
from app.models.tenant import Tenant, TenantConfig, TenantUser
from app.routers.auth import get_current_active_user
from app.core.schema_generator import SchemaGenerator

logger = structlog.get_logger()
router = APIRouter()


@router.get("/{tenant_id}")
async def get_schema(
    tenant_id: str,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Retorna o schema de banco de dados do tenant"""
    
    # Verificar acesso
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
    
    if not config or not config.database_schema:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schema não encontrado"
        )
    
    return {
        "tenant_id": tenant_id,
        "schema": config.database_schema,
    }


@router.post("/{tenant_id}/validate")
async def validate_schema(
    tenant_id: str,
    schema: Dict[str, Any],
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Valida um schema proposto"""
    
    # Verificar acesso admin
    membership = db.query(TenantUser).filter(
        TenantUser.tenant_id == tenant_id,
        TenantUser.user_id == current_user.id,
        TenantUser.role.in_(["admin", "manager"]),
        TenantUser.is_active == True
    ).first()
    
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado"
        )
    
    generator = SchemaGenerator()
    
    # Validar schema
    errors = []
    warnings = []
    
    # Verificar entidades
    if "entities" not in schema:
        errors.append("Schema deve conter 'entities'")
    else:
        for entity_name, entity in schema["entities"].items():
            if "fields" not in entity:
                errors.append(f"Entidade '{entity_name}' deve ter 'fields'")
            else:
                for field in entity["fields"]:
                    if "name" not in field:
                        errors.append(f"Campo em '{entity_name}' deve ter 'name'")
                    if "type" not in field:
                        errors.append(f"Campo '{field.get('name', '?')}' em '{entity_name}' deve ter 'type'")
                    elif field["type"] not in generator.FIELD_TYPES:
                        errors.append(f"Tipo '{field['type']}' não é suportado")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }


@router.post("/{tenant_id}/generate-sql")
async def generate_sql(
    tenant_id: str,
    schema: Dict[str, Any],
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Gera SQL DDL a partir de um schema"""
    
    membership = db.query(TenantUser).filter(
        TenantUser.tenant_id == tenant_id,
        TenantUser.user_id == current_user.id,
        TenantUser.role.in_(["admin", "manager"]),
        TenantUser.is_active == True
    ).first()
    
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado"
        )
    
    generator = SchemaGenerator()
    sql = generator.generate_sql(schema)
    
    return {
        "sql": sql,
    }


@router.get("/{tenant_id}/entities/{entity_name}")
async def get_entity_schema(
    tenant_id: str,
    entity_name: str,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Retorna schema de uma entidade específica"""
    
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
    
    if not config or not config.database_schema:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schema não encontrado"
        )
    
    entities = config.database_schema.get("entities", {})
    
    if entity_name not in entities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entidade não encontrada"
        )
    
    return {
        "entity": entity_name,
        "schema": entities[entity_name],
    }


@router.post("/{tenant_id}/entities/{entity_name}/fields")
async def add_field(
    tenant_id: str,
    entity_name: str,
    field: Dict[str, Any],
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Adiciona um campo a uma entidade existente"""
    
    membership = db.query(TenantUser).filter(
        TenantUser.tenant_id == tenant_id,
        TenantUser.user_id == current_user.id,
        TenantUser.role == "admin",
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
    
    if not config or not config.database_schema:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schema não encontrado"
        )
    
    entities = config.database_schema.get("entities", {})
    
    if entity_name not in entities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entidade não encontrada"
        )
    
    # Adicionar campo
    entities[entity_name]["fields"].append(field)
    
    # Salvar
    config.database_schema["entities"] = entities
    db.commit()
    
    logger.info(
        "field_added",
        tenant_id=tenant_id,
        entity=entity_name,
        field=field.get("name"),
    )
    
    return {
        "message": "Campo adicionado com sucesso",
        "entity": entity_name,
        "field": field,
    }


@router.get("/field-types")
async def get_field_types():
    """Retorna tipos de campos suportados"""
    
    generator = SchemaGenerator()
    
    types = []
    for type_name, type_info in generator.FIELD_TYPES.items():
        types.append({
            "name": type_name,
            "sql_type": type_info["sql"],
            "python_type": type_info["python"],
        })
    
    return {"types": types}
