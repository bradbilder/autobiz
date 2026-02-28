"""
Modelos dinâmicos gerados em runtime
"""
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from typing import Dict, Any, Type

DynamicBase = declarative_base()


class DynamicModel:
    """
    Factory para criar modelos dinâmicos baseado no schema
    """
    
    # Mapeamento de tipos
    TYPE_MAPPING = {
        "string": String,
        "text": Text,
        "integer": Integer,
        "decimal": Float,
        "boolean": Boolean,
        "datetime": DateTime,
        "date": DateTime,
        "json": JSON,
        "uuid": String(36),
        "reference": String(36),
        "file": String(500),
        "image": String(500),
        "email": String(255),
        "phone": String(50),
        "cpf": String(14),
        "cnpj": String(18),
        "cep": String(9),
        "money": Float,
        "percentage": Float,
        "enum": String(100),
    }
    
    @classmethod
    def create_model(
        cls,
        name: str,
        schema: Dict[str, Any],
        base=DynamicBase
    ) -> Type:
        """
        Cria uma classe de modelo dinâmica
        
        Args:
            name: Nome da entidade
            schema: Schema da entidade
            base: Base declarativa
            
        Returns:
            Classe do modelo
        """
        attrs = {
            "__tablename__": schema.get("table_name", name),
            "__table_args__": {"extend_existing": True},
        }
        
        # Adicionar colunas
        for field in schema.get("fields", []):
            column = cls._create_column(field)
            if column:
                attrs[field["name"]] = column
        
        # Criar classe
        model_class = type(name.capitalize(), (base,), attrs)
        
        return model_class
    
    @classmethod
    def _create_column(cls, field: Dict[str, Any]):
        """Cria uma coluna SQLAlchemy a partir da definição de campo"""
        field_type = field.get("type", "string")
        
        # Obter tipo SQLAlchemy
        sa_type = cls.TYPE_MAPPING.get(field_type, String(255))
        
        # Argumentos da coluna
        kwargs = {}
        
        # Primary key
        if field.get("primary_key"):
            kwargs["primary_key"] = True
        
        # Nullable
        if not field.get("required") and not field.get("primary_key"):
            kwargs["nullable"] = True
        else:
            kwargs["nullable"] = False
        
        # Unique
        if field.get("unique"):
            kwargs["unique"] = True
        
        # Default
        if "default" in field:
            kwargs["default"] = field["default"]
        
        # Index
        if field.get("index"):
            kwargs["index"] = True
        
        return Column(sa_type, **kwargs)
    
    @classmethod
    def create_all_models(
        cls,
        schema: Dict[str, Any],
        base=DynamicBase
    ) -> Dict[str, Type]:
        """
        Cria todos os modelos a partir de um schema completo
        
        Args:
            schema: Schema completo com todas as entidades
            base: Base declarativa
            
        Returns:
            Dicionário de modelos
        """
        models = {}
        
        for entity_name, entity_schema in schema.get("entities", {}).items():
            model = cls.create_model(entity_name, entity_schema, base)
            models[entity_name] = model
        
        return models
