from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.models.base import Base
from app.models.ticket import TicketStatus


class TicketUpdate(Base):
    __tablename__ = "ticket_updates"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"))
    ticket = relationship("Ticket", back_populates="updates")
    
    previous_status = Column(Enum(TicketStatus), nullable=True)
    new_status = Column(Enum(TicketStatus), nullable=False)
    note = Column(Text, nullable=True)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")
    
    timestamp = Column(DateTime, default=datetime.utcnow)