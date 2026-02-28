"""
Gerador de temas e componentes de UI dinâmicos
"""
from typing import Dict, List, Any, Optional
import structlog

logger = structlog.get_logger()


class UIGenerator:
    """Gera configurações de UI personalizadas baseado no perfil do negócio"""
    
    # Paletas de cores predefinidas
    COLOR_PALETTES = {
        "professional": {
            "primary": "#2563eb",
            "secondary": "#64748b",
            "accent": "#0ea5e9",
            "success": "#10b981",
            "warning": "#f59e0b",
            "error": "#ef4444",
            "background": "#f8fafc",
            "surface": "#ffffff",
            "text": "#1e293b",
            "textSecondary": "#64748b",
        },
        "modern": {
            "primary": "#7c3aed",
            "secondary": "#8b5cf6",
            "accent": "#ec4899",
            "success": "#22c55e",
            "warning": "#f97316",
            "error": "#dc2626",
            "background": "#faf5ff",
            "surface": "#ffffff",
            "text": "#2e1065",
            "textSecondary": "#6b7280",
        },
        "minimal": {
            "primary": "#18181b",
            "secondary": "#71717a",
            "accent": "#3f3f46",
            "success": "#16a34a",
            "warning": "#ca8a04",
            "error": "#dc2626",
            "background": "#fafafa",
            "surface": "#ffffff",
            "text": "#09090b",
            "textSecondary": "#52525b",
        },
        "warm": {
            "primary": "#ea580c",
            "secondary": "#c2410c",
            "accent": "#f59e0b",
            "success": "#65a30d",
            "warning": "#d97706",
            "error": "#dc2626",
            "background": "#fff7ed",
            "surface": "#ffffff",
            "text": "#431407",
            "textSecondary": "#78716c",
        },
        "health": {
            "primary": "#059669",
            "secondary": "#10b981",
            "accent": "#14b8a6",
            "success": "#22c55e",
            "warning": "#eab308",
            "error": "#ef4444",
            "background": "#f0fdf4",
            "surface": "#ffffff",
            "text": "#064e3b",
            "textSecondary": "#6b7280",
        },
    }
    
    # Layouts por tipo de negócio
    LAYOUTS = {
        "varejo": {
            "sidebar": True,
            "sidebar_collapsed": False,
            "topbar": True,
            "sidebar_items": [
                {"icon": "LayoutDashboard", "label": "Dashboard", "path": "/"},
                {"icon": "ShoppingCart", "label": "Vendas", "path": "/vendas"},
                {"icon": "Package", "label": "Produtos", "path": "/produtos"},
                {"icon": "Users", "label": "Clientes", "path": "/clientes"},
                {"icon": "BarChart3", "label": "Relatórios", "path": "/relatorios"},
                {"icon": "Settings", "label": "Configurações", "path": "/configuracoes"},
            ],
        },
        "servicos": {
            "sidebar": True,
            "sidebar_collapsed": False,
            "topbar": True,
            "sidebar_items": [
                {"icon": "LayoutDashboard", "label": "Dashboard", "path": "/"},
                {"icon": "Calendar", "label": "Agenda", "path": "/agenda"},
                {"icon": "Briefcase", "label": "Serviços", "path": "/servicos"},
                {"icon": "Users", "label": "Clientes", "path": "/clientes"},
                {"icon": "CheckSquare", "label": "Tarefas", "path": "/tarefas"},
                {"icon": "BarChart3", "label": "Relatórios", "path": "/relatorios"},
                {"icon": "Settings", "label": "Configurações", "path": "/configuracoes"},
            ],
        },
        "clinica": {
            "sidebar": True,
            "sidebar_collapsed": False,
            "topbar": True,
            "sidebar_items": [
                {"icon": "LayoutDashboard", "label": "Dashboard", "path": "/"},
                {"icon": "Calendar", "label": "Agenda", "path": "/agenda"},
                {"icon": "Users", "label": "Pacientes", "path": "/pacientes"},
                {"icon": "Stethoscope", "label": "Consultas", "path": "/consultas"},
                {"icon": "FileText", "label": "Prontuários", "path": "/prontuarios"},
                {"icon": "BarChart3", "label": "Relatórios", "path": "/relatorios"},
                {"icon": "Settings", "label": "Configurações", "path": "/configuracoes"},
            ],
        },
    }
    
    # Widgets de dashboard por tipo
    DASHBOARD_WIDGETS = {
        "varejo": [
            {"type": "kpi", "title": "Vendas Hoje", "icon": "DollarSign", "color": "primary"},
            {"type": "kpi", "title": "Ticket Médio", "icon": "Receipt", "color": "secondary"},
            {"type": "kpi", "title": "Produtos em Falta", "icon": "AlertTriangle", "color": "warning"},
            {"type": "kpi", "title": "Clientes Novos", "icon": "UserPlus", "color": "success"},
            {"type": "chart", "title": "Vendas por Período", "chart_type": "line"},
            {"type": "chart", "title": "Produtos Mais Vendidos", "chart_type": "bar"},
            {"type": "list", "title": "Últimas Vendas", "entity": "vendas"},
            {"type": "list", "title": "Alertas de Estoque", "entity": "produtos"},
        ],
        "servicos": [
            {"type": "kpi", "title": "Agendamentos Hoje", "icon": "Calendar", "color": "primary"},
            {"type": "kpi", "title": "Serviços Pendentes", "icon": "Clock", "color": "warning"},
            {"type": "kpi", "title": "Faturamento", "icon": "DollarSign", "color": "success"},
            {"type": "kpi", "title": "Clientes Ativos", "icon": "Users", "color": "secondary"},
            {"type": "chart", "title": "Agendamentos por Mês", "chart_type": "line"},
            {"type": "chart", "title": "Serviços por Categoria", "chart_type": "pie"},
            {"type": "list", "title": "Próximos Agendamentos", "entity": "agendamentos"},
            {"type": "list", "title": "Tarefas Pendentes", "entity": "tarefas"},
        ],
        "clinica": [
            {"type": "kpi", "title": "Consultas Hoje", "icon": "Stethoscope", "color": "primary"},
            {"type": "kpi", "title": "Pacientes Aguardando", "icon": "UserClock", "color": "warning"},
            {"type": "kpi", "title": "Atendimentos Mês", "icon": "Activity", "color": "success"},
            {"type": "kpi", "title": "Taxa de Comparecimento", "icon": "Percent", "color": "accent"},
            {"type": "chart", "title": "Consultas por Especialidade", "chart_type": "pie"},
            {"type": "chart", "title": "Evolução de Atendimentos", "chart_type": "line"},
            {"type": "list", "title": "Próximas Consultas", "entity": "consultas"},
            {"type": "list", "title": "Aniversariantes", "entity": "pacientes"},
        ],
    }
    
    def __init__(self):
        pass
    
    async def generate(
        self,
        business_profile: Dict[str, Any],
        template: Optional[Dict[str, Any]] = None,
        branding: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Gera configuração completa de UI
        """
        business_type = business_profile.get("type", "generico")
        size = business_profile.get("size", "small")
        
        logger.info(
            "generating_ui",
            business_type=business_type,
        )
        
        # Selecionar paleta de cores
        palette = self._select_palette(business_profile, branding)
        
        # Gerar layout
        layout = self._generate_layout(business_type)
        
        # Gerar dashboard
        dashboard = self._generate_dashboard(business_type)
        
        # Gerar tema
        theme = self._generate_theme(palette, branding)
        
        # Gerar configuração de formulários
        forms = self._generate_forms(business_type)
        
        ui_config = {
            "theme": theme,
            "layout": layout,
            "dashboard": dashboard,
            "forms": forms,
            "components": self._get_component_config(),
        }
        
        logger.info("ui_generated")
        
        return ui_config
    
    def _select_palette(
        self,
        business_profile: Dict[str, Any],
        branding: Optional[Dict[str, Any]]
    ) -> Dict[str, str]:
        """Seleciona paleta de cores"""
        # Usar cor da marca se fornecida
        if branding and branding.get("primary_color"):
            palette = self.COLOR_PALETTES["professional"].copy()
            palette["primary"] = branding["primary_color"]
            return palette
        
        # Selecionar por tipo de negócio
        business_type = business_profile.get("type", "")
        
        if business_type in ["clinica", "saude", "academia"]:
            return self.COLOR_PALETTES["health"]
        elif business_type in ["restaurante", "food"]:
            return self.COLOR_PALETTES["warm"]
        elif business_type in ["varejo", "ecommerce"]:
            return self.COLOR_PALETTES["modern"]
        elif business_type in ["consultoria", "servicos"]:
            return self.COLOR_PALETTES["professional"]
        else:
            return self.COLOR_PALETTES["minimal"]
    
    def _generate_layout(self, business_type: str) -> Dict[str, Any]:
        """Gera configuração de layout"""
        layout = self.LAYOUTS.get(business_type, self.LAYOUTS["varejo"])
        return layout
    
    def _generate_dashboard(self, business_type: str) -> Dict[str, Any]:
        """Gera configuração do dashboard"""
        widgets = self.DASHBOARD_WIDGETS.get(
            business_type,
            self.DASHBOARD_WIDGETS["varejo"]
        )
        
        return {
            "layout": "grid",
            "columns": 4,
            "widgets": widgets,
            "refresh_interval": 300,  # segundos
        }
    
    def _generate_theme(
        self,
        palette: Dict[str, str],
        branding: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Gera configuração de tema"""
        return {
            "colors": palette,
            "typography": {
                "font_family": branding.get("font_family", "Inter") if branding else "Inter",
                "heading_sizes": {
                    "h1": "2rem",
                    "h2": "1.5rem",
                    "h3": "1.25rem",
                    "h4": "1rem",
                },
            },
            "spacing": {
                "xs": "0.25rem",
                "sm": "0.5rem",
                "md": "1rem",
                "lg": "1.5rem",
                "xl": "2rem",
            },
            "border_radius": {
                "sm": "0.25rem",
                "md": "0.5rem",
                "lg": "0.75rem",
                "xl": "1rem",
            },
            "shadows": {
                "sm": "0 1px 2px rgba(0,0,0,0.05)",
                "md": "0 4px 6px rgba(0,0,0,0.1)",
                "lg": "0 10px 15px rgba(0,0,0,0.1)",
            },
            "logo": branding.get("logo_url") if branding else None,
            "favicon": branding.get("favicon_url") if branding else None,
        }
    
    def _generate_forms(self, business_type: str) -> Dict[str, Any]:
        """Gera configuração de formulários"""
        return {
            "default_layout": "vertical",
            "label_position": "top",
            "submit_button_position": "bottom",
            "show_required_indicator": True,
            "validation_mode": "on_blur",
        }
    
    def _get_component_config(self) -> Dict[str, Any]:
        """Retorna configuração de componentes"""
        return {
            "table": {
                "pagination": True,
                "page_size": 10,
                "searchable": True,
                "sortable": True,
                "filterable": True,
                "exportable": True,
            },
            "form": {
                "autosave": False,
                "confirm_on_leave": True,
            },
            "modal": {
                "close_on_overlay_click": True,
                "show_close_button": True,
            },
        }
