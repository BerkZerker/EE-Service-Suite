from sqlalchemy import Column, String, Boolean, Enum
import enum
from app.models.base import BaseModel


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    TECHNICIAN = "technician"


class User(BaseModel):
    """User model for staff accounts"""
    
    __tablename__ = "users"
    
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(Enum(UserRole), default=UserRole.TECHNICIAN, nullable=False)
    is_active = Column(Boolean, default=True)