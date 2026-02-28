"""
Gerador de endpoints da API dinâmicos
"""
from typing import Dict, List, Any, Optional
import structlog

logger = structlog.get_logger()


class APIGenerator:
    """Gera endpoints da API dinamicamente baseado no schema"""
    
    # Operações CRUD padrão
    CRUD_OPERATIONS = ["create", "read", "update", "delete", "list"]
    
    # Endpoints adicionais por tipo de entidade
    EXTRA_ENDPOINTS = {
        "produtos": [
            {"name": "ajustar_estoque", "method": "POST", "path": "/{id}/ajustar-estoque"},
            {"name": "duplicar", "method": "POST", "path": "/{id}/duplicar"},
            {"name": "exportar", "method": "GET", "path": "/exportar"},
        ],
        "vendas": [
            {"name": "cancelar", "method": "POST", "path": "/{id}/cancelar"},
            {"name": "gerar_nota", "method": "POST", "path": "/{id}/gerar-nota"},
            {"name": "enviar_email", "method": "POST", "path": "/{id}/enviar-email"},
        ],
        "clientes": [
            {"name": "historico", "method": "GET", "path": "/{id}/historico"},
            {"name": "enviar_mensagem", "method": "POST", "path": "/{id}/enviar-mensagem"},
        ],
        "agendamentos": [
            {"name": "confirmar", "method": "POST", "path": "/{id}/confirmar"},
            {"name": "cancelar", "method": "POST", "path": "/{id}/cancelar"},
            {"name": "remarcar", "method": "POST", "path": "/{id}/remarcar"},
        ],
        "consultas": [
            {"name": "iniciar", "method": "POST", "path": "/{id}/iniciar"},
            {"name": "finalizar", "method": "POST", "path": "/{id}/finalizar"},
            {"name": "prontuario", "method": "GET", "path": "/{id}/prontuario"},
        ],
    }
    
    # Endpoints de relatórios
    REPORT_ENDPOINTS = {
        "vendas": [
            {"name": "por_periodo", "path": "/relatorios/vendas/por-periodo"},
            {"name": "por_produto", "path": "/relatorios/vendas/por-produto"},
            {"name": "por_cliente", "path": "/relatorios/vendas/por-cliente"},
            {"name": "por_vendedor", "path": "/relatorios/vendas/por-vendedor"},
        ],
        "financeiro": [
            {"name": "fluxo_caixa", "path": "/relatorios/financeiro/fluxo-caixa"},
            {"name": "contas_receber", "path": "/relatorios/financeiro/contas-receber"},
            {"name": "contas_pagar", "path": "/relatorios/financeiro/contas-pagar"},
        ],
        "estoque": [
            {"name": "posicao", "path": "/relatorios/estoque/posicao"},
            {"name": "movimentacao", "path": "/relatorios/estoque/movimentacao"},
            {"name": "curva_abc", "path": "/relatorios/estoque/curva-abc"},
        ],
    }
    
    def __init__(self):
        pass
    
    async def generate(
        self,
        business_profile: Dict[str, Any],
        db_schema: Dict[str, Any],
        template: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Gera configuração completa da API
        """
        business_type = business_profile.get("type", "generico")
        
        logger.info(
            "generating_api",
            business_type=business_type,
        )
        
        # Gerar endpoints para cada entidade
        entity_endpoints = {}
        for entity_name in db_schema.get("entities", {}).keys():
            endpoints = self._generate_entity_endpoints(entity_name)
            entity_endpoints[entity_name] = endpoints
        
        # Gerar endpoints de relatórios
        report_endpoints = self._generate_report_endpoints(business_type)
        
        # Gerar endpoints de dashboard
        dashboard_endpoints = self._generate_dashboard_endpoints()
        
        # Gerar endpoints de busca
        search_endpoints = self._generate_search_endpoints(db_schema)
        
        api_config = {
            "version": "v1",
            "base_path": "/api/v1",
            "entities": entity_endpoints,
            "reports": report_endpoints,
            "dashboard": dashboard_endpoints,
            "search": search_endpoints,
            "webhooks": self._generate_webhook_config(),
        }
        
        logger.info(
            "api_generated",
            entities_count=len(entity_endpoints),
            endpoints_count=sum(len(e) for e in entity_endpoints.values()),
        )
        
        return api_config
    
    def _generate_entity_endpoints(self, entity_name: str) -> List[Dict[str, Any]]:
        """Gera endpoints para uma entidade"""
        endpoints = []
        
        # Endpoints CRUD básicos
        base_path = f"/data/{entity_name}"
        
        # Listar
        endpoints.append({
            "name": f"listar_{entity_name}",
            "method": "GET",
            "path": base_path,
            "operation": "list",
            "auth_required": True,
            "permissions": [f"{entity_name}:read"],
            "parameters": [
                {"name": "page", "type": "integer", "default": 1},
                {"name": "page_size", "type": "integer", "default": 10},
                {"name": "search", "type": "string"},
                {"name": "sort_by", "type": "string"},
                {"name": "sort_order", "type": "string", "default": "desc"},
                {"name": "filters", "type": "object"},
            ],
        })
        
        # Criar
        endpoints.append({
            "name": f"criar_{entity_name}",
            "method": "POST",
            "path": base_path,
            "operation": "create",
            "auth_required": True,
            "permissions": [f"{entity_name}:write"],
        })
        
        # Obter
        endpoints.append({
            "name": f"obter_{entity_name}",
            "method": "GET",
            "path": f"{base_path}/{{id}}",
            "operation": "read",
            "auth_required": True,
            "permissions": [f"{entity_name}:read"],
        })
        
        # Atualizar
        endpoints.append({
            "name": f"atualizar_{entity_name}",
            "method": "PUT",
            "path": f"{base_path}/{{id}}",
            "operation": "update",
            "auth_required": True,
            "permissions": [f"{entity_name}:write"],
        })
        
        # Deletar
        endpoints.append({
            "name": f"deletar_{entity_name}",
            "method": "DELETE",
            "path": f"{base_path}/{{id}}",
            "operation": "delete",
            "auth_required": True,
            "permissions": [f"{entity_name}:delete"],
        })
        
        # Endpoints extras específicos
        extra = self.EXTRA_ENDPOINTS.get(entity_name, [])
        for ep in extra:
            endpoints.append({
                "name": ep["name"],
                "method": ep["method"],
                "path": f"{base_path}{ep['path']}",
                "auth_required": True,
                "permissions": [f"{entity_name}:write"],
            })
        
        return endpoints
    
    def _generate_report_endpoints(self, business_type: str) -> List[Dict[str, Any]]:
        """Gera endpoints de relatórios"""
        endpoints = []
        
        # Relatórios específicos do tipo de negócio
        reports = self.REPORT_ENDPOINTS.get(business_type, [])
        for report in reports:
            endpoints.append({
                "name": report["name"],
                "method": "GET",
                "path": report["path"],
                "auth_required": True,
                "permissions": ["relatorios:read"],
                "parameters": [
                    {"name": "data_inicio", "type": "date", "required": True},
                    {"name": "data_fim", "type": "date", "required": True},
                    {"name": "formato", "type": "string", "default": "json"},
                ],
            })
        
        return endpoints
    
    def _generate_dashboard_endpoints(self) -> List[Dict[str, Any]]:
        """Gera endpoints do dashboard"""
        return [
            {
                "name": "kpi_cards",
                "method": "GET",
                "path": "/dashboard/kpis",
                "auth_required": True,
            },
            {
                "name": "chart_data",
                "method": "GET",
                "path": "/dashboard/charts/{chart_id}",
                "auth_required": True,
            },
            {
                "name": "recent_activity",
                "method": "GET",
                "path": "/dashboard/activity",
                "auth_required": True,
            },
            {
                "name": "alerts",
                "method": "GET",
                "path": "/dashboard/alerts",
                "auth_required": True,
            },
        ]
    
    def _generate_search_endpoints(self, db_schema: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Gera endpoints de busca global"""
        return [
            {
                "name": "global_search",
                "method": "GET",
                "path": "/search",
                "auth_required": True,
                "parameters": [
                    {"name": "q", "type": "string", "required": True},
                    {"name": "entities", "type": "array"},
                    {"name": "limit", "type": "integer", "default": 10},
                ],
            },
            {
                "name": "autocomplete",
                "method": "GET",
                "path": "/search/autocomplete",
                "auth_required": True,
                "parameters": [
                    {"name": "q", "type": "string", "required": True},
                    {"name": "entity", "type": "string", "required": True},
                ],
            },
        ]
    
    def _generate_webhook_config(self) -> Dict[str, Any]:
        """Gera configuração de webhooks"""
        return {
            "enabled": True,
            "events": [
                "entity.created",
                "entity.updated",
                "entity.deleted",
                "venda.confirmada",
                "agendamento.confirmado",
                "estoque.baixo",
            ],
            "retry_policy": {
                "max_retries": 3,
                "retry_delay": 60,
            },
        }
