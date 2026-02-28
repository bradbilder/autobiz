"""
Router de CRUD Dinâmico - Autobiz
Endpoints auto-gerados para manipulação de dados
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import text, and_, or_
from typing import Dict, List, Any, Optional
import structlog

from app.config import settings
from app.models.base import get_db
from app.models.tenant import Tenant, TenantUser
from app.routers.auth import get_current_active_user
from app.core.database_manager import DatabaseManager

logger = structlog.get_logger()
router = APIRouter()

db_manager = DatabaseManager()


def get_tenant_db(tenant_id: str) -> Session:
    """Obtém sessão de banco para um tenant específico"""
    return db_manager.get_tenant_session(tenant_id)


def check_tenant_access(user, tenant_id: str, db: Session) -> bool:
    """Verifica se usuário tem acesso ao tenant"""
    membership = db.query(TenantUser).filter(
        TenantUser.tenant_id == tenant_id,
        TenantUser.user_id == user.id,
        TenantUser.is_active == True
    ).first()
    
    return membership is not None


@router.get("/{tenant_id}/{entity}")
async def list_entities(
    tenant_id: str,
    entity: str,
    request: Request,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    sort_by: Optional[str] = Query(None),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Lista registros de uma entidade"""
    
    # Verificar acesso ao tenant
    if not check_tenant_access(current_user, tenant_id, db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado ao tenant"
        )
    
    # Obter sessão do tenant
    tenant_db = get_tenant_db(tenant_id)
    
    try:
        # Construir query
        schema_name = f"tenant_{tenant_id.replace('-', '_')}"
        table_name = entity
        
        # Query base
        query = f"SELECT * FROM {schema_name}.{table_name}"
        count_query = f"SELECT COUNT(*) FROM {schema_name}.{table_name}"
        
        # Filtros
        where_clauses = []
        params = {}
        
        if search:
            # Busca em campos de texto
            where_clauses.append("(nome ILIKE :search OR descricao ILIKE :search)")
            params["search"] = f"%{search}%"
        
        # Aplicar filtros da query string
        for key, value in request.query_params.items():
            if key not in ["page", "page_size", "search", "sort_by", "sort_order"]:
                where_clauses.append(f"{key} = :{key}")
                params[key] = value
        
        if where_clauses:
            where_sql = " WHERE " + " AND ".join(where_clauses)
            query += where_sql
            count_query += where_sql
        
        # Ordenação
        if sort_by:
            query += f" ORDER BY {sort_by} {sort_order.upper()}"
        else:
            query += " ORDER BY created_at DESC"
        
        # Paginação
        offset = (page - 1) * page_size
        query += f" LIMIT :limit OFFSET :offset"
        params["limit"] = page_size
        params["offset"] = offset
        
        # Executar queries
        result = tenant_db.execute(text(query), params)
        count_result = tenant_db.execute(text(count_query), {k: v for k, v in params.items() if k not in ["limit", "offset"]})
        
        total = count_result.scalar()
        
        # Converter para dict
        items = []
        for row in result:
            item = {}
            for key in row.keys():
                value = getattr(row, key)
                # Converter datetime para string
                if hasattr(value, 'isoformat'):
                    value = value.isoformat()
                item[key] = value
            items.append(item)
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
        }
        
    except Exception as e:
        logger.error(
            "error_listing_entities",
            tenant_id=tenant_id,
            entity=entity,
            error=str(e),
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar registros: {str(e)}"
        )
    finally:
        tenant_db.close()


@router.post("/{tenant_id}/{entity}")
async def create_entity(
    tenant_id: str,
    entity: str,
    data: Dict[str, Any],
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Cria um novo registro"""
    
    if not check_tenant_access(current_user, tenant_id, db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado ao tenant"
        )
    
    tenant_db = get_tenant_db(tenant_id)
    
    try:
        schema_name = f"tenant_{tenant_id.replace('-', '_')}"
        table_name = entity
        
        # Adicionar tenant_id e timestamps
        data["tenant_id"] = tenant_id
        
        # Construir INSERT
        columns = list(data.keys())
        values = [f":{col}" for col in columns]
        
        query = f"""
            INSERT INTO {schema_name}.{table_name} ({', '.join(columns)})
            VALUES ({', '.join(values)})
            RETURNING *
        """
        
        result = tenant_db.execute(text(query), data)
        tenant_db.commit()
        
        row = result.fetchone()
        
        # Converter para dict
        item = {}
        for key in row.keys():
            value = getattr(row, key)
            if hasattr(value, 'isoformat'):
                value = value.isoformat()
            item[key] = value
        
        logger.info(
            "entity_created",
            tenant_id=tenant_id,
            entity=entity,
            record_id=item.get("id"),
        )
        
        return item
        
    except Exception as e:
        tenant_db.rollback()
        logger.error(
            "error_creating_entity",
            tenant_id=tenant_id,
            entity=entity,
            error=str(e),
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar registro: {str(e)}"
        )
    finally:
        tenant_db.close()


@router.get("/{tenant_id}/{entity}/{record_id}")
async def get_entity(
    tenant_id: str,
    entity: str,
    record_id: str,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtém um registro específico"""
    
    if not check_tenant_access(current_user, tenant_id, db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado ao tenant"
        )
    
    tenant_db = get_tenant_db(tenant_id)
    
    try:
        schema_name = f"tenant_{tenant_id.replace('-', '_')}"
        table_name = entity
        
        query = f"""
            SELECT * FROM {schema_name}.{table_name}
            WHERE id = :id AND tenant_id = :tenant_id
        """
        
        result = tenant_db.execute(text(query), {
            "id": record_id,
            "tenant_id": tenant_id
        })
        
        row = result.fetchone()
        
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro não encontrado"
            )
        
        item = {}
        for key in row.keys():
            value = getattr(row, key)
            if hasattr(value, 'isoformat'):
                value = value.isoformat()
            item[key] = value
        
        return item
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "error_getting_entity",
            tenant_id=tenant_id,
            entity=entity,
            record_id=record_id,
            error=str(e),
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter registro: {str(e)}"
        )
    finally:
        tenant_db.close()


@router.put("/{tenant_id}/{entity}/{record_id}")
async def update_entity(
    tenant_id: str,
    entity: str,
    record_id: str,
    data: Dict[str, Any],
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Atualiza um registro"""
    
    if not check_tenant_access(current_user, tenant_id, db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado ao tenant"
        )
    
    tenant_db = get_tenant_db(tenant_id)
    
    try:
        schema_name = f"tenant_{tenant_id.replace('-', '_')}"
        table_name = entity
        
        # Remover campos protegidos
        data.pop("id", None)
        data.pop("tenant_id", None)
        data.pop("created_at", None)
        
        # Construir UPDATE
        set_clauses = [f"{key} = :{key}" for key in data.keys()]
        
        query = f"""
            UPDATE {schema_name}.{table_name}
            SET {', '.join(set_clauses)}, updated_at = NOW()
            WHERE id = :id AND tenant_id = :tenant_id
            RETURNING *
        """
        
        data["id"] = record_id
        data["tenant_id"] = tenant_id
        
        result = tenant_db.execute(text(query), data)
        tenant_db.commit()
        
        row = result.fetchone()
        
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro não encontrado"
            )
        
        item = {}
        for key in row.keys():
            value = getattr(row, key)
            if hasattr(value, 'isoformat'):
                value = value.isoformat()
            item[key] = value
        
        logger.info(
            "entity_updated",
            tenant_id=tenant_id,
            entity=entity,
            record_id=record_id,
        )
        
        return item
        
    except HTTPException:
        raise
    except Exception as e:
        tenant_db.rollback()
        logger.error(
            "error_updating_entity",
            tenant_id=tenant_id,
            entity=entity,
            record_id=record_id,
            error=str(e),
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar registro: {str(e)}"
        )
    finally:
        tenant_db.close()


@router.delete("/{tenant_id}/{entity}/{record_id}")
async def delete_entity(
    tenant_id: str,
    entity: str,
    record_id: str,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Remove um registro"""
    
    if not check_tenant_access(current_user, tenant_id, db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado ao tenant"
        )
    
    tenant_db = get_tenant_db(tenant_id)
    
    try:
        schema_name = f"tenant_{tenant_id.replace('-', '_')}"
        table_name = entity
        
        query = f"""
            DELETE FROM {schema_name}.{table_name}
            WHERE id = :id AND tenant_id = :tenant_id
            RETURNING id
        """
        
        result = tenant_db.execute(text(query), {
            "id": record_id,
            "tenant_id": tenant_id
        })
        tenant_db.commit()
        
        row = result.fetchone()
        
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro não encontrado"
            )
        
        logger.info(
            "entity_deleted",
            tenant_id=tenant_id,
            entity=entity,
            record_id=record_id,
        )
        
        return {"message": "Registro removido com sucesso"}
        
    except HTTPException:
        raise
    except Exception as e:
        tenant_db.rollback()
        logger.error(
            "error_deleting_entity",
            tenant_id=tenant_id,
            entity=entity,
            record_id=record_id,
            error=str(e),
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao remover registro: {str(e)}"
        )
    finally:
        tenant_db.close()


@router.post("/{tenant_id}/{entity}/{record_id}/{action}")
async def execute_entity_action(
    tenant_id: str,
    entity: str,
    record_id: str,
    action: str,
    data: Optional[Dict[str, Any]] = None,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Executa uma ação customizada em um registro"""
    
    if not check_tenant_access(current_user, tenant_id, db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado ao tenant"
        )
    
    # Mapear ações conhecidas
    actions_map = {
        "cancelar": "cancel",
        "confirmar": "confirm",
        "duplicar": "duplicate",
        "ajustar-estoque": "adjust_stock",
    }
    
    action_name = actions_map.get(action, action)
    
    logger.info(
        "entity_action_executed",
        tenant_id=tenant_id,
        entity=entity,
        record_id=record_id,
        action=action_name,
    )
    
    # TODO: Implementar lógica de ações
    
    return {
        "message": f"Ação '{action}' executada com sucesso",
        "action": action_name,
    }
