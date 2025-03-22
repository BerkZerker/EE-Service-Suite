from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Bike(BaseModel):
    __tablename__ = "bikes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    specs = Column(Text, nullable=True)
    
    # Owner relationship
    owner_id = Column(Integer, ForeignKey("customers.id"))
    owner = relationship("Customer", back_populates="bikes")
    
    # Relationship to tickets
    tickets = relationship("Ticket", back_populates="bike", cascade="all, delete-orphan")
