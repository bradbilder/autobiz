"""
Classe base para plugins
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional


class PluginBase(ABC):
    """Classe base que todos os plugins devem estender"""
    
    # Metadados do plugin
    name: str = ""
    version: str = "1.0.0"
    description: str = ""
    author: str = ""
    
    # Configurações
    config_schema: Dict[str, Any] = {}
    default_config: Dict[str, Any] = {}
    
    def __init__(self, tenant_id: str, config: Dict[str, Any] = None):
        self.tenant_id = tenant_id
        self.config = {**self.default_config, **(config or {})}
        self.enabled = True
    
    @abstractmethod
    async def initialize(self):
        """Inicializa o plugin"""
        pass
    
    @abstractmethod
    async def shutdown(self):
        """Desliga o plugin"""
        pass
    
    def get_config(self) -> Dict[str, Any]:
        """Retorna configuração atual"""
        return self.config
    
    def update_config(self, config: Dict[str, Any]):
        """Atualiza configuração"""
        self.config.update(config)
    
    async def execute(self, action: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Executa uma ação do plugin"""
        method = getattr(self, f"action_{action}", None)
        
        if method and callable(method):
            return await method(params or {})
        
        return {"success": False, "error": f"Ação '{action}' não encontrada"}
    
    def get_hooks(self) -> List[str]:
        """Retorna hooks que este plugin registra"""
        return []
    
    async def on_hook(self, hook_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Chamado quando um hook é disparado"""
        handler = getattr(self, f"hook_{hook_name}", None)
        
        if handler and callable(handler):
            return await handler(data)
        
        return {"success": True}
