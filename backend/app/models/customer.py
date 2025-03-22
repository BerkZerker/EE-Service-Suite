from sqlalchemy import Column, String, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), index=True)
    phone = Column(String(20))
    notes = Column(Text, nullable=True)
    
    # Relationship to bikes
    bikes = relationship("Bike", back_populates="owner", cascade="all, delete-orphan")
