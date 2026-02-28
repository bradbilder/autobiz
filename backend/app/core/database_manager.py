"""
Gerenciador de bancos multi-tenant
"""
from typing import Dict, List, Any, Optional
from sqlalchemy import create_engine, text, MetaData
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
import structlog

from app.config import settings

logger = structlog.get_logger()


class DatabaseManager:
    """
    Gerencia bancos de dados multi-tenant
    Cria e gerencia schemas isolados para cada tenant
    """
    
    def __init__(self):
        self.engines: Dict[str, Any] = {}
        self.main_engine = None
        self.SessionLocal = None
    
    async def initialize(self):
        """Inicializa o gerenciador de banco de dados"""
        logger.info("initializing_database_manager")
        
        # Engine principal (banco de metadados)
        self.main_engine = create_engine(
            settings.DATABASE_URL,
            poolclass=QueuePool,
            pool_size=settings.DATABASE_POOL_SIZE,
            max_overflow=settings.DATABASE_MAX_OVERFLOW,
            pool_pre_ping=True,
        )
        
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.main_engine
        )
        
        logger.info("database_manager_initialized")
    
    async def shutdown(self):
        """Desliga o gerenciador"""
        logger.info("shutting_down_database_manager")
        
        # Fechar todos os engines de tenant
        for tenant_id, engine in self.engines.items():
            engine.dispose()
        
        # Fechar engine principal
        if self.main_engine:
            self.main_engine.dispose()
    
    async def create_tenant_database(
        self,
        tenant_id: str,
        schema: Dict[str, Any]
    ):
        """
        Cria banco de dados/schema para um novo tenant
        """
        logger.info(
            "creating_tenant_database",
            tenant_id=tenant_id,
        )
        
        # Criar schema isolado para o tenant
        schema_name = f"tenant_{tenant_id.replace('-', '_')}"
        
        with self.main_engine.connect() as conn:
            # Criar schema
            conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name}"))
            conn.commit()
            
            logger.info(
                "tenant_schema_created",
                tenant_id=tenant_id,
                schema_name=schema_name,
            )
            
            # Criar tabelas
            await self._create_tables(conn, schema_name, schema)
            
            # Criar índices
            await self._create_indexes(conn, schema_name, schema)
            
            conn.commit()
        
        logger.info(
            "tenant_database_created",
            tenant_id=tenant_id,
        )
    
    async def _create_tables(
        self,
        conn,
        schema_name: str,
        schema: Dict[str, Any]
    ):
        """Cria tabelas no schema do tenant"""
        from app.core.schema_generator import SchemaGenerator
        
        generator = SchemaGenerator()
        sql = generator.generate_sql(schema)
        
        # Executar SQL de criação de tabelas
        for statement in sql.split(";"):
            statement = statement.strip()
            if statement:
                # Adicionar schema name às tabelas
                statement = statement.replace(
                    "CREATE TABLE ",
                    f"CREATE TABLE {schema_name}."
                )
                statement = statement.replace(
                    "CREATE INDEX ",
                    f"CREATE INDEX {schema_name}."
                )
                statement = statement.replace(
                    "CREATE UNIQUE INDEX ",
                    f"CREATE UNIQUE INDEX {schema_name}."
                )
                
                try:
                    conn.execute(text(statement))
                except Exception as e:
                    logger.error(
                        "error_creating_table",
                        error=str(e),
                        statement=statement[:100],
                    )
    
    async def _create_indexes(
        self,
        conn,
        schema_name: str,
        schema: Dict[str, Any]
    ):
        """Cria índices no schema do tenant"""
        # Índices já são criados junto com as tabelas
        pass
    
    def get_tenant_session(self, tenant_id: str) -> Session:
        """Retorna uma sessão de banco para um tenant específico"""
        schema_name = f"tenant_{tenant_id.replace('-', '_')}"
        
        # Criar engine específico se não existir
        if tenant_id not in self.engines:
            # Modificar URL para usar schema específico
            db_url = settings.DATABASE_URL
            
            engine = create_engine(
                db_url,
                connect_args={
                    "options": f"-c search_path={schema_name},public"
                },
                poolclass=QueuePool,
                pool_size=5,
                max_overflow=10,
                pool_pre_ping=True,
            )
            
            self.engines[tenant_id] = engine
        
        # Criar sessão
        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engines[tenant_id]
        )
        
        return SessionLocal()
    
    def get_main_session(self) -> Session:
        """Retorna uma sessão para o banco principal"""
        return self.SessionLocal()
    
    async def migrate_tenant(
        self,
        tenant_id: str,
        migrations: List[Dict[str, Any]]
    ):
        """Executa migrações em um tenant específico"""
        logger.info(
            "migrating_tenant",
            tenant_id=tenant_id,
            migrations_count=len(migrations),
        )
        
        schema_name = f"tenant_{tenant_id.replace('-', '_')}"
        
        with self.main_engine.connect() as conn:
            for migration in migrations:
                try:
                    # Adicionar schema name
                    sql = migration["sql"].replace(
                        "{schema}",
                        schema_name
                    )
                    conn.execute(text(sql))
                    
                    # Registrar migração
                    conn.execute(
                        text(f"""
                            INSERT INTO {schema_name}.migrations 
                            (version, applied_at) 
                            VALUES (:version, NOW())
                        """),
                        {"version": migration["version"]}
                    )
                    
                    conn.commit()
                    
                except Exception as e:
                    logger.error(
                        "migration_failed",
                        tenant_id=tenant_id,
                        version=migration.get("version"),
                        error=str(e),
                    )
                    raise
        
        logger.info(
            "tenant_migrated",
            tenant_id=tenant_id,
        )
    
    async def backup_tenant(self, tenant_id: str) -> str:
        """Cria backup do banco de um tenant"""
        logger.info(
            "backing_up_tenant",
            tenant_id=tenant_id,
        )
        
        # Implementar backup usando pg_dump
        import subprocess
        from datetime import datetime
        
        backup_file = f"/backups/tenant_{tenant_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
        
        # TODO: Implementar backup real
        
        return backup_file
    
    async def restore_tenant(self, tenant_id: str, backup_file: str):
        """Restaura backup do banco de um tenant"""
        logger.info(
            "restoring_tenant",
            tenant_id=tenant_id,
            backup_file=backup_file,
        )
        
        # TODO: Implementar restore real
        pass
    
    async def delete_tenant_database(self, tenant_id: str):
        """Remove banco de dados de um tenant"""
        logger.info(
            "deleting_tenant_database",
            tenant_id=tenant_id,
        )
        
        schema_name = f"tenant_{tenant_id.replace('-', '_')}"
        
        with self.main_engine.connect() as conn:
            conn.execute(text(f"DROP SCHEMA IF EXISTS {schema_name} CASCADE"))
            conn.commit()
        
        # Remover engine
        if tenant_id in self.engines:
            self.engines[tenant_id].dispose()
            del self.engines[tenant_id]
        
        logger.info(
            "tenant_database_deleted",
            tenant_id=tenant_id,
        )
