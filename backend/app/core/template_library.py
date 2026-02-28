"""
Biblioteca de templates de negócio
"""
from typing import Dict, List, Any, Optional
import json
import structlog

logger = structlog.get_logger()


class TemplateLibrary:
    """
    Biblioteca de templates pré-configurados para diferentes tipos de negócio
    """
    
    # Templates predefinidos
    TEMPLATES = {
        "varejo": {
            "name": "Varejo",
            "description": "Loja física ou virtual de produtos",
            "icon": "ShoppingBag",
            "features": ["produtos", "estoque", "vendas", "clientes", "relatorios"],
            "entities": ["produtos", "categorias", "clientes", "vendas", "itens_venda"],
            "dashboard_widgets": ["vendas_hoje", "estoque_baixo", "produtos_mais_vendidos"],
            "suggested_integrations": ["mercadopago", "whatsapp"],
            "color_palette": "modern",
        },
        "ecommerce": {
            "name": "E-commerce",
            "description": "Loja virtual completa",
            "icon": "Globe",
            "features": ["produtos", "estoque", "pedidos", "clientes", "carrinho", "envios"],
            "entities": ["produtos", "categorias", "clientes", "pedidos", "itens_pedido", "carrinho"],
            "dashboard_widgets": ["pedidos_hoje", "vendas_mes", "carrinhos_abandonados"],
            "suggested_integrations": ["mercadopago", "whatsapp", "correios"],
            "color_palette": "modern",
        },
        "servicos": {
            "name": "Prestação de Serviços",
            "description": "Agendamento e gestão de serviços",
            "icon": "Briefcase",
            "features": ["servicos", "agendamentos", "clientes", "profissionais", "comissoes"],
            "entities": ["servicos", "clientes", "agendamentos", "profissionais"],
            "dashboard_widgets": ["agendamentos_hoje", "faturamento", "servicos_pendentes"],
            "suggested_integrations": ["whatsapp", "google_calendar"],
            "color_palette": "professional",
        },
        "consultoria": {
            "name": "Consultoria",
            "description": "Gestão de projetos e consultoria",
            "icon": "Users",
            "features": ["projetos", "clientes", "tarefas", "horas", "entregaveis"],
            "entities": ["projetos", "clientes", "tarefas", "consultores"],
            "dashboard_widgets": ["projetos_ativos", "horas_lancadas", "faturamento"],
            "suggested_integrations": ["whatsapp", "google_calendar"],
            "color_palette": "professional",
        },
        "restaurante": {
            "name": "Restaurante",
            "description": "Gestão de restaurante e delivery",
            "icon": "Utensils",
            "features": ["cardapio", "pedidos", "mesas", "delivery", "cozinha"],
            "entities": ["produtos", "categorias", "mesas", "pedidos", "comandas"],
            "dashboard_widgets": ["pedidos_hoje", "mesas_ocupadas", "ticket_medio"],
            "suggested_integrations": ["mercadopago", "whatsapp", "ifood"],
            "color_palette": "warm",
        },
        "clinica": {
            "name": "Clínica Médica",
            "description": "Gestão de clínica e prontuários",
            "icon": "Heart",
            "features": ["pacientes", "consultas", "agenda", "prontuarios", "exames"],
            "entities": ["pacientes", "medicos", "consultas", "procedimentos"],
            "dashboard_widgets": ["consultas_hoje", "pacientes_ativos", "faturamento"],
            "suggested_integrations": ["whatsapp", "google_calendar"],
            "color_palette": "health",
        },
        "imobiliaria": {
            "name": "Imobiliária",
            "description": "Gestão de imóveis e corretores",
            "icon": "Home",
            "features": ["imoveis", "proprietarios", "interessados", "visitas", "contratos"],
            "entities": ["imoveis", "proprietarios", "interessados", "visitas", "contratos"],
            "dashboard_widgets": ["imoveis_disponiveis", "visitas_mes", "vendas_fechadas"],
            "suggested_integrations": ["whatsapp"],
            "color_palette": "professional",
        },
        "construcao": {
            "name": "Construção Civil",
            "description": "Gestão de obras e fornecedores",
            "icon": "Building",
            "features": ["obras", "fornecedores", "materiais", "equipe", "cronograma"],
            "entities": ["obras", "fornecedores", "materiais", "equipe", "cronograma"],
            "dashboard_widgets": ["obras_ativas", "gastos_mes", "prazos"],
            "suggested_integrations": ["whatsapp"],
            "color_palette": "minimal",
        },
        "escola": {
            "name": "Escola/Instituição",
            "description": "Gestão escolar completa",
            "icon": "GraduationCap",
            "features": ["alunos", "professores", "turmas", "notas", "frequencia"],
            "entities": ["alunos", "professores", "turmas", "disciplinas", "notas"],
            "dashboard_widgets": ["alunos_ativos", "frequencia_media", "provas_pendentes"],
            "suggested_integrations": ["whatsapp"],
            "color_palette": "professional",
        },
        "academia": {
            "name": "Academia",
            "description": "Gestão de academia e alunos",
            "icon": "Dumbbell",
            "features": ["alunos", "planos", "aulas", "matriculas", "frequencia"],
            "entities": ["alunos", "planos", "aulas", "matriculas", "frequencia"],
            "dashboard_widgets": ["alunos_ativos", "frequencia_hoje", "matriculas_mes"],
            "suggested_integrations": ["whatsapp", "mercadopago"],
            "color_palette": "health",
        },
        "salao": {
            "name": "Salão de Beleza",
            "description": "Gestão de salão e agendamentos",
            "icon": "Scissors",
            "features": ["clientes", "servicos", "profissionais", "agendamentos", "comissoes"],
            "entities": ["clientes", "servicos", "profissionais", "agendamentos"],
            "dashboard_widgets": ["agendamentos_hoje", "faturamento", "comissoes"],
            "suggested_integrations": ["whatsapp"],
            "color_palette": "warm",
        },
        "oficina": {
            "name": "Oficina Mecânica",
            "description": "Gestão de oficina e ordens de serviço",
            "icon": "Wrench",
            "features": ["veiculos", "clientes", "servicos", "pecas", "ordens"],
            "entities": ["veiculos", "clientes", "servicos", "pecas", "ordens_servico"],
            "dashboard_widgets": ["ordens_hoje", "servicos_pendentes", "faturamento"],
            "suggested_integrations": ["whatsapp"],
            "color_palette": "minimal",
        },
    }
    
    def __init__(self):
        self.templates = {}
    
    async def load_templates(self):
        """Carrega templates da biblioteca"""
        logger.info("loading_templates")
        
        self.templates = self.TEMPLATES.copy()
        
        logger.info(
            "templates_loaded",
            count=len(self.templates),
        )
    
    def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """Retorna um template pelo ID"""
        return self.templates.get(template_id)
    
    def get_all_templates(self) -> List[Dict[str, Any]]:
        """Retorna todos os templates disponíveis"""
        return [
            {"id": k, **v}
            for k, v in self.templates.items()
        ]
    
    def get_template_for_profile(
        self,
        business_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Seleciona o melhor template para um perfil de negócio
        """
        business_type = business_profile.get("type", "varejo")
        
        # Tentar encontrar template exato
        if business_type in self.templates:
            return self.templates[business_type]
        
        # Fallback para varejo
        return self.templates.get("varejo")
    
    def customize_template(
        self,
        template_id: str,
        customizations: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Customiza um template com configurações específicas
        """
        template = self.get_template(template_id)
        if not template:
            raise ValueError(f"Template não encontrado: {template_id}")
        
        # Criar cópia customizada
        customized = template.copy()
        
        # Aplicar customizações
        if "features" in customizations:
            customized["features"] = customizations["features"]
        
        if "entities" in customizations:
            customized["entities"] = customizations["entities"]
        
        if "color_palette" in customizations:
            customized["color_palette"] = customizations["color_palette"]
        
        return customized
