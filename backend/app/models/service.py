from sqlalchemy import Column, Integer, String, Text, Float
from sqlalchemy.orm import relationship

from app.models.base import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    
    # Can be extended with additional fields like duration, labor hours, etc.