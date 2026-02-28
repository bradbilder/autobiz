"""
Classificador de negócios usando IA
"""
from typing import Dict, Any, List
import structlog

from app.config import settings

logger = structlog.get_logger()


class BusinessClassifier:
    """Classifica o tipo de negócio baseado nas respostas do onboarding"""
    
    # Mapeamento de palavras-chave para tipos de negócio
    KEYWORDS = {
        "varejo": ["loja", "varejo", "produtos", "loja física", "comércio"],
        "ecommerce": ["e-commerce", "ecommerce", "loja virtual", "online", "internet", "site"],
        "servicos": ["serviços", "prestação", "consultoria", "serviço"],
        "consultoria": ["consultoria", "consultor", "assessoria", "consultoría"],
        "restaurante": ["restaurante", "comida", "alimentação", "lanchonete", "bar", "delivery"],
        "clinica": ["clínica", "médico", "saúde", "consultório", "dentista", "fisioterapia"],
        "imobiliaria": ["imobiliária", "imóveis", "corretor", "imóvel", "casa", "apartamento"],
        "construcao": ["construção", "obra", "construtora", "engenharia", "pedreiro"],
        "escola": ["escola", "educação", "curso", "aula", "professor", "treinamento"],
        "academia": ["academia", "fitness", "ginásio", "musculação", "crossfit"],
        "salao": ["salão", "beleza", "cabeleireiro", "estética", "manicure", "barbearia"],
        "oficina": ["oficina", "mecânica", "carro", "veículo", "auto", "mecânico"],
    }
    
    def __init__(self):
        self.openai_available = bool(settings.OPENAI_API_KEY)
    
    async def classify(self, onboarding_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classifica o negócio baseado nos dados do onboarding
        
        Returns:
            Dict com tipo, tamanho, features sugeridas, etc.
        """
        business_info = onboarding_data.get("business_info", {})
        
        # Extrair informações
        business_type = business_info.get("business_type", "")
        business_size = business_info.get("business_size", "small")
        description = business_info.get("description", "")
        name = business_info.get("name", "")
        
        # Se já tem tipo definido, usar
        if business_type:
            detected_type = business_type
        else:
            # Detectar por palavras-chave
            detected_type = self._detect_by_keywords(name + " " + description)
        
        # Sugerir features baseado no tipo
        suggested_features = self._suggest_features(detected_type, business_size)
        
        # Sugerir integrações
        suggested_integrations = self._suggest_integrations(detected_type)
        
        profile = {
            "type": detected_type,
            "size": business_size,
            "name": name,
            "description": description,
            "features": suggested_features,
            "integrations": suggested_integrations,
            "complexity": self._calculate_complexity(business_size, suggested_features),
        }
        
        logger.info(
            "business_classified",
            type=detected_type,
            size=business_size,
            features_count=len(suggested_features),
        )
        
        return profile
    
    def _detect_by_keywords(self, text: str) -> str:
        """Detecta tipo de negócio por palavras-chave"""
        text_lower = text.lower()
        
        scores = {}
        for business_type, keywords in self.KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                scores[business_type] = score
        
        if scores:
            return max(scores, key=scores.get)
        
        return "varejo"  # Default
    
    def _suggest_features(self, business_type: str, size: str) -> List[str]:
        """Sugere features baseado no tipo de negócio"""
        features = ["dashboard", "relatorios"]
        
        # Features por tipo
        type_features = {
            "varejo": ["produtos", "estoque", "vendas", "clientes", "pdv"],
            "ecommerce": ["produtos", "estoque", "pedidos", "clientes", "carrinho", "envios"],
            "servicos": ["servicos", "agendamentos", "clientes", "profissionais"],
            "consultoria": ["projetos", "clientes", "tarefas", "horas", "entregaveis"],
            "restaurante": ["cardapio", "pedidos", "mesas", "comandas", "delivery"],
            "clinica": ["pacientes", "consultas", "agenda", "prontuarios", "exames"],
            "imobiliaria": ["imoveis", "proprietarios", "interessados", "visitas", "contratos"],
            "construcao": ["obras", "fornecedores", "materiais", "equipe", "cronograma"],
            "escola": ["alunos", "professores", "turmas", "notas", "frequencia"],
            "academia": ["alunos", "planos", "aulas", "matriculas", "frequencia"],
            "salao": ["clientes", "servicos", "profissionais", "agendamentos", "comissoes"],
            "oficina": ["veiculos", "clientes", "servicos", "pecas", "ordens"],
        }
        
        features.extend(type_features.get(business_type, []))
        
        # Features por tamanho
        if size in ["medium", "large"]:
            features.extend(["multi_usuario", "permissoes", "workflows"])
        
        if size == "large":
            features.extend(["multi_filial", "api", "webhooks", "automacao"])
        
        return list(set(features))
    
    def _suggest_integrations(self, business_type: str) -> List[str]:
        """Sugere integrações baseado no tipo"""
        integrations = ["whatsapp"]
        
        if business_type in ["varejo", "ecommerce", "restaurante", "academia"]:
            integrations.append("mercadopago")
        
        if business_type in ["servicos", "consultoria", "clinica", "salao"]:
            integrations.append("google_calendar")
        
        if business_type == "ecommerce":
            integrations.extend(["email_marketing", "correios"])
        
        return integrations
    
    def _calculate_complexity(self, size: str, features: List[str]) -> str:
        """Calcula nível de complexidade do sistema"""
        feature_count = len(features)
        
        if size == "small" and feature_count <= 5:
            return "simple"
        elif size == "large" or feature_count > 15:
            return "complex"
        else:
            return "medium"
