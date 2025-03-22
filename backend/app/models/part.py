from sqlalchemy import Column, Integer, String, Text, Float, SmallInteger
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Part(BaseModel):
    __tablename__ = "parts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50))
    sku = Column(String(50), unique=True, index=True, nullable=True)
    
    # Stock information
    quantity = Column(Integer, default=0)
    min_stock = Column(Integer, default=0)
    reorder_point = Column(Integer, default=0)
    
    # Pricing
    cost_price = Column(Float, nullable=False)  # Wholesale cost
    retail_price = Column(Float, nullable=False)  # Retail price
    
    # Relationship
    ticket_parts = relationship("TicketPart", back_populates="part")
    
    def calculate_markup(self):
        """Calculate markup percentage."""
        if self.cost_price > 0:
            return ((self.retail_price - self.cost_price) / self.cost_price) * 100
        return 0