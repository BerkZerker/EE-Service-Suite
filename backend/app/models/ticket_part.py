from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class TicketPart(Base):
    __tablename__ = "ticket_parts"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"))
    part_id = Column(Integer, ForeignKey("parts.id"))
    
    quantity = Column(Integer, default=1)
    price_charged = Column(Float)  # Price charged to customer (may differ from retail)
    
    # Relationships
    ticket = relationship("Ticket", back_populates="parts")
    part = relationship("Part", back_populates="ticket_parts")
    
    def calculate_total(self):
        """Calculate total cost for this line item."""
        return self.quantity * self.price_charged
    
    def calculate_profit(self):
        """Calculate profit for this line item."""
        cost = self.quantity * self.part.cost_price
        return self.calculate_total() - cost