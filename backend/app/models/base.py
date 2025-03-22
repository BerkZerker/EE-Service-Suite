from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from app.db.database import Base as SQLAlchemyBase


class TimestampMixin:
    """Mixin that adds created_at and updated_at columns to models"""
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now(), 
        nullable=False
    )


class BaseModel(SQLAlchemyBase):
    """Base model with id and timestamp columns"""
    
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now(), 
        nullable=False
    )