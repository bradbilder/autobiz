"""
Base e utilitários dos modelos SQLAlchemy
"""
from sqlalchemy import create_engine, Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
import uuid

from app.config import settings

# Criar engine principal
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa
Base = declarative_base()


class BaseModel(Base):
    """Modelo base com campos comuns"""
    __abstract__ = True
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


def get_db():
    """Gerenciador de contexto para sessões de banco"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
