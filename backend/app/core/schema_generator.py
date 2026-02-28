"""
Gerador de schemas de banco de dados dinâmicos
"""
from typing import Dict, List, Any, Optional
import structlog

logger = structlog.get_logger()


class SchemaGenerator:
    """Gera schemas de banco de dados baseado no perfil do negócio"""
    
    # Tipos de campos suportados
    FIELD_TYPES = {
        "string": {"sql": "VARCHAR(255)", "python": "str"},
        "text": {"sql": "TEXT", "python": "str"},
        "integer": {"sql": "INTEGER", "python": "int"},
        "decimal": {"sql": "DECIMAL(10,2)", "python": "float"},
        "boolean": {"sql": "BOOLEAN", "python": "bool"},
        "datetime": {"sql": "TIMESTAMP", "python": "datetime"},
        "date": {"sql": "DATE", "python": "date"},
        "json": {"sql": "JSONB", "python": "dict"},
        "uuid": {"sql": "UUID", "python": "uuid"},
        "reference": {"sql": "UUID", "python": "uuid"},
        "file": {"sql": "VARCHAR(500)", "python": "str"},
        "image": {"sql": "VARCHAR(500)", "python": "str"},
        "email": {"sql": "VARCHAR(255)", "python": "str"},
        "phone": {"sql": "VARCHAR(50)", "python": "str"},
        "cpf": {"sql": "VARCHAR(14)", "python": "str"},
        "cnpj": {"sql": "VARCHAR(18)", "python": "str"},
        "cep": {"sql": "VARCHAR(9)", "python": "str"},
        "money": {"sql": "DECIMAL(15,2)", "python": "float"},
        "percentage": {"sql": "DECIMAL(5,2)", "python": "float"},
        "enum": {"sql": "VARCHAR(100)", "python": "str"},
    }
    
    # Entidades base por tipo de negócio
    BASE_ENTITIES = {
        "varejo": ["produtos", "categorias", "clientes", "vendas", "itens_venda"],
        "ecommerce": ["produtos", "categorias", "clientes", "pedidos", "itens_pedido", "carrinho"],
        "servicos": ["servicos", "clientes", "contratos", "atendimentos", "tarefas"],
        "consultoria": ["projetos", "clientes", "consultores", "horas", "entregaveis"],
        "restaurante": ["produtos", "categorias", "mesas", "pedidos", "comandas", "garcons"],
        "clinica": ["pacientes", "medicos", "consultas", "procedimentos", "prontuarios"],
        "imobiliaria": ["imoveis", "proprietarios", "interessados", "visitas", "contratos"],
        "construcao": ["obras", "fornecedores", "materiais", "equipe", "cronograma"],
        "escola": ["alunos", "professores", "turmas", "disciplinas", "notas", "frequencia"],
        "academia": ["alunos", "planos", "aulas", "matriculas", "frequencia"],
        "salao": ["clientes", "servicos", "profissionais", "agendamentos", "comissoes"],
        "oficina": ["veiculos", "clientes", "servicos", "pecas", "ordens_servico"],
    }
    
    # Campos padrão por entidade
    ENTITY_FIELDS = {
        "produtos": [
            {"name": "nome", "type": "string", "required": True},
            {"name": "descricao", "type": "text", "required": False},
            {"name": "codigo", "type": "string", "required": True, "unique": True},
            {"name": "preco_custo", "type": "money", "required": True},
            {"name": "preco_venda", "type": "money", "required": True},
            {"name": "estoque_atual", "type": "integer", "required": True, "default": 0},
            {"name": "estoque_minimo", "type": "integer", "required": True, "default": 5},
            {"name": "unidade", "type": "enum", "required": True, "options": ["un", "kg", "lt", "mt", "cx"]},
            {"name": "ativo", "type": "boolean", "required": True, "default": True},
            {"name": "imagem", "type": "image", "required": False},
            {"name": "categoria_id", "type": "reference", "ref": "categorias", "required": False},
        ],
        "categorias": [
            {"name": "nome", "type": "string", "required": True},
            {"name": "descricao", "type": "text", "required": False},
            {"name": "cor", "type": "string", "required": False},
            {"name": "ordem", "type": "integer", "required": False, "default": 0},
        ],
        "clientes": [
            {"name": "nome", "type": "string", "required": True},
            {"name": "email", "type": "email", "required": False},
            {"name": "telefone", "type": "phone", "required": False},
            {"name": "cpf_cnpj", "type": "string", "required": False},
            {"name": "data_nascimento", "type": "date", "required": False},
            {"name": "endereco", "type": "json", "required": False},
            {"name": "observacoes", "type": "text", "required": False},
            {"name": "tags", "type": "json", "required": False},
        ],
        "vendas": [
            {"name": "cliente_id", "type": "reference", "ref": "clientes", "required": False},
            {"name": "data_venda", "type": "datetime", "required": True},
            {"name": "valor_total", "type": "money", "required": True},
            {"name": "desconto", "type": "money", "required": False, "default": 0},
            {"name": "forma_pagamento", "type": "enum", "required": True, "options": ["dinheiro", "cartao_credito", "cartao_debito", "pix", "boleto"]},
            {"name": "status", "type": "enum", "required": True, "options": ["pendente", "pago", "cancelado"], "default": "pendente"},
            {"name": "observacoes", "type": "text", "required": False},
        ],
        "itens_venda": [
            {"name": "venda_id", "type": "reference", "ref": "vendas", "required": True},
            {"name": "produto_id", "type": "reference", "ref": "produtos", "required": True},
            {"name": "quantidade", "type": "decimal", "required": True},
            {"name": "valor_unitario", "type": "money", "required": True},
            {"name": "valor_total", "type": "money", "required": True},
        ],
        "pedidos": [
            {"name": "cliente_id", "type": "reference", "ref": "clientes", "required": True},
            {"name": "data_pedido", "type": "datetime", "required": True},
            {"name": "status", "type": "enum", "required": True, "options": ["novo", "confirmado", "em_preparacao", "enviado", "entregue", "cancelado"]},
            {"name": "valor_produtos", "type": "money", "required": True},
            {"name": "valor_frete", "type": "money", "required": False, "default": 0},
            {"name": "valor_total", "type": "money", "required": True},
            {"name": "endereco_entrega", "type": "json", "required": True},
            {"name": "rastreamento", "type": "string", "required": False},
        ],
        "servicos": [
            {"name": "nome", "type": "string", "required": True},
            {"name": "descricao", "type": "text", "required": False},
            {"name": "preco", "type": "money", "required": True},
            {"name": "duracao_minutos", "type": "integer", "required": False},
            {"name": "ativo", "type": "boolean", "required": True, "default": True},
        ],
        "agendamentos": [
            {"name": "cliente_id", "type": "reference", "ref": "clientes", "required": True},
            {"name": "servico_id", "type": "reference", "ref": "servicos", "required": True},
            {"name": "profissional_id", "type": "reference", "ref": "profissionais", "required": False},
            {"name": "data_hora", "type": "datetime", "required": True},
            {"name": "status", "type": "enum", "required": True, "options": ["agendado", "confirmado", "em_andamento", "concluido", "cancelado"]},
            {"name": "observacoes", "type": "text", "required": False},
        ],
        "projetos": [
            {"name": "nome", "type": "string", "required": True},
            {"name": "descricao", "type": "text", "required": False},
            {"name": "cliente_id", "type": "reference", "ref": "clientes", "required": True},
            {"name": "responsavel_id", "type": "reference", "ref": "usuarios", "required": True},
            {"name": "data_inicio", "type": "date", "required": True},
            {"name": "data_fim_prevista", "type": "date", "required": False},
            {"name": "status", "type": "enum", "required": True, "options": ["planejamento", "em_andamento", "pausado", "concluido", "cancelado"]},
            {"name": "valor", "type": "money", "required": False},
        ],
        "tarefas": [
            {"name": "titulo", "type": "string", "required": True},
            {"name": "descricao", "type": "text", "required": False},
            {"name": "projeto_id", "type": "reference", "ref": "projetos", "required": False},
            {"name": "responsavel_id", "type": "reference", "ref": "usuarios", "required": True},
            {"name": "data_inicio", "type": "date", "required": True},
            {"name": "data_fim", "type": "date", "required": False},
            {"name": "status", "type": "enum", "required": True, "options": ["pendente", "em_andamento", "concluida", "cancelada"]},
            {"name": "prioridade", "type": "enum", "required": True, "options": ["baixa", "media", "alta", "urgente"]},
        ],
        "pacientes": [
            {"name": "nome", "type": "string", "required": True},
            {"name": "data_nascimento", "type": "date", "required": True},
            {"name": "sexo", "type": "enum", "required": True, "options": ["M", "F", "O"]},
            {"name": "cpf", "type": "cpf", "required": True},
            {"name": "telefone", "type": "phone", "required": True},
            {"name": "email", "type": "email", "required": False},
            {"name": "endereco", "type": "json", "required": False},
            {"name": "alergias", "type": "text", "required": False},
            {"name": "observacoes", "type": "text", "required": False},
        ],
        "consultas": [
            {"name": "paciente_id", "type": "reference", "ref": "pacientes", "required": True},
            {"name": "medico_id", "type": "reference", "ref": "medicos", "required": True},
            {"name": "data_hora", "type": "datetime", "required": True},
            {"name": "tipo", "type": "enum", "required": True, "options": ["primeira_vez", "retorno", "emergencia"]},
            {"name": "status", "type": "enum", "required": True, "options": ["agendada", "confirmada", "em_andamento", "concluida", "cancelada"]},
            {"name": "queixa_principal", "type": "text", "required": False},
            {"name": "diagnostico", "type": "text", "required": False},
            {"name": "prescricao", "type": "text", "required": False},
        ],
        "imoveis": [
            {"name": "titulo", "type": "string", "required": True},
            {"name": "descricao", "type": "text", "required": False},
            {"name": "tipo", "type": "enum", "required": True, "options": ["casa", "apartamento", "comercial", "terreno", "rural"]},
            {"name": "finalidade", "type": "enum", "required": True, "options": ["venda", "aluguel"]},
            {"name": "valor", "type": "money", "required": True},
            {"name": "endereco", "type": "json", "required": True},
            {"name": "area_total", "type": "decimal", "required": False},
            {"name": "area_construida", "type": "decimal", "required": False},
            {"name": "quartos", "type": "integer", "required": False},
            {"name": "banheiros", "type": "integer", "required": False},
            {"name": "vagas_garagem", "type": "integer", "required": False},
            {"name": "fotos", "type": "json", "required": False},
            {"name": "status", "type": "enum", "required": True, "options": ["disponivel", "reservado", "vendido", "alugado"]},
        ],
        "usuarios": [
            {"name": "nome", "type": "string", "required": True},
            {"name": "email", "type": "email", "required": True, "unique": True},
            {"name": "senha_hash", "type": "string", "required": True},
            {"name": "telefone", "type": "phone", "required": False},
            {"name": "cargo", "type": "enum", "required": True, "options": ["admin", "gerente", "operador", "visualizador"]},
            {"name": "ativo", "type": "boolean", "required": True, "default": True},
            {"name": "ultimo_acesso", "type": "datetime", "required": False},
            {"name": "avatar", "type": "image", "required": False},
        ],
    }
    
    def __init__(self):
        pass
    
    async def generate(
        self,
        business_profile: Dict[str, Any],
        template: Optional[Dict[str, Any]] = None,
        custom_fields: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Gera um schema de banco de dados completo
        """
        business_type = business_profile.get("type", "generico")
        size = business_profile.get("size", "small")
        
        logger.info(
            "generating_schema",
            business_type=business_type,
            size=size,
        )
        
        # Determinar entidades base
        entities = self._get_entities_for_business(business_type)
        
        # Adicionar entidades comuns a todos
        entities.extend(["usuarios", "configuracoes", "logs"])
        
        # Gerar schema para cada entidade
        schema = {
            "entities": {},
            "relationships": [],
            "indexes": [],
        }
        
        for entity_name in entities:
            entity_schema = self._generate_entity_schema(entity_name)
            schema["entities"][entity_name] = entity_schema
        
        # Adicionar campos customizados
        if custom_fields:
            for field in custom_fields:
                entity = field.get("entity")
                if entity and entity in schema["entities"]:
                    schema["entities"][entity]["fields"].append(field)
        
        # Gerar relacionamentos
        schema["relationships"] = self._generate_relationships(schema["entities"])
        
        # Gerar índices
        schema["indexes"] = self._generate_indexes(schema["entities"])
        
        logger.info(
            "schema_generated",
            entities_count=len(entities),
            relationships_count=len(schema["relationships"]),
        )
        
        return schema
    
    def _get_entities_for_business(self, business_type: str) -> List[str]:
        """Retorna entidades para um tipo de negócio"""
        return self.BASE_ENTITIES.get(business_type, ["clientes", "vendas", "produtos"])
    
    def _generate_entity_schema(self, entity_name: str) -> Dict[str, Any]:
        """Gera schema para uma entidade específica"""
        fields = self.ENTITY_FIELDS.get(entity_name, [])
        
        # Adicionar campos padrão de auditoria
        audit_fields = [
            {"name": "id", "type": "uuid", "required": True, "primary_key": True},
            {"name": "created_at", "type": "datetime", "required": True},
            {"name": "updated_at", "type": "datetime", "required": True},
            {"name": "tenant_id", "type": "uuid", "required": True, "index": True},
        ]
        
        all_fields = audit_fields + fields
        
        return {
            "name": entity_name,
            "fields": all_fields,
            "table_name": f"{entity_name}",
        }
    
    def _generate_relationships(
        self,
        entities: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Gera relacionamentos entre entidades"""
        relationships = []
        
        for entity_name, entity in entities.items():
            for field in entity.get("fields", []):
                if field.get("type") == "reference":
                    ref_entity = field.get("ref")
                    if ref_entity and ref_entity in entities:
                        relationships.append({
                            "from": entity_name,
                            "to": ref_entity,
                            "field": field["name"],
                            "type": "many_to_one",
                        })
        
        return relationships
    
    def _generate_indexes(
        self,
        entities: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Gera índices para otimização"""
        indexes = []
        
        for entity_name, entity in entities.items():
            for field in entity.get("fields", []):
                # Índice para campos de busca frequentes
                if field.get("index") or field.get("unique"):
                    indexes.append({
                        "table": entity_name,
                        "fields": [field["name"]],
                        "unique": field.get("unique", False),
                    })
                
                # Índice para campos de data
                if field["type"] in ["datetime", "date"]:
                    indexes.append({
                        "table": entity_name,
                        "fields": [field["name"]],
                        "unique": False,
                    })
        
        return indexes
    
    def generate_sql(self, schema: Dict[str, Any]) -> str:
        """Gera SQL DDL a partir do schema"""
        sql_statements = []
        
        for entity_name, entity in schema["entities"].items():
            fields_sql = []
            
            for field in entity["fields"]:
                field_type = self.FIELD_TYPES.get(field["type"], self.FIELD_TYPES["string"])
                sql_type = field_type["sql"]
                
                constraints = []
                if field.get("required") and not field.get("primary_key"):
                    constraints.append("NOT NULL")
                if field.get("unique"):
                    constraints.append("UNIQUE")
                if field.get("default") is not None:
                    constraints.append(f"DEFAULT {field['default']}")
                
                field_sql = f"    {field['name']} {sql_type} {' '.join(constraints)}"
                fields_sql.append(field_sql)
            
            # Primary key
            pk_field = next((f for f in entity["fields"] if f.get("primary_key")), None)
            if pk_field:
                fields_sql.append(f"    PRIMARY KEY ({pk_field['name']})")
            
            create_table = f"CREATE TABLE {entity_name} (\n" + ",\n".join(fields_sql) + "\n);"
            sql_statements.append(create_table)
        
        # Índices
        for idx in schema.get("indexes", []):
            idx_name = f"idx_{idx['table']}_{'_'.join(idx['fields'])}"
            unique = "UNIQUE " if idx.get("unique") else ""
            fields = ", ".join(idx["fields"])
            sql = f"CREATE {unique}INDEX {idx_name} ON {idx['table']} ({fields});"
            sql_statements.append(sql)
        
        return "\n\n".join(sql_statements)
