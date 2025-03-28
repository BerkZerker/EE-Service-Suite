from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, Float, DateTime, Boolean
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

from app.models.base import BaseModel


class TicketStatus(str, enum.Enum):
    INTAKE = "intake"
    DIAGNOSIS = "diagnosis"
    AWAITING_PARTS = "awaiting_parts"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    DELIVERED = "delivered"


class TicketPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Ticket(BaseModel):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(String(20), unique=True, index=True)
    problem_description = Column(Text, nullable=False)
    diagnosis = Column(Text, nullable=True)
    status = Column(Enum(TicketStatus), default=TicketStatus.INTAKE)
    priority = Column(Enum(TicketPriority), default=TicketPriority.MEDIUM)
    estimated_completion = Column(DateTime, nullable=True)
    is_archived = Column(Boolean, default=False, index=True)
    
    # Relationships
    bike_id = Column(Integer, ForeignKey("bikes.id"))
    bike = relationship("Bike", back_populates="tickets")
    
    technician_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    technician = relationship("User")
    
    # Related items
    updates = relationship("TicketUpdate", back_populates="ticket", cascade="all, delete-orphan")
    parts = relationship("TicketPart", back_populates="ticket", cascade="all, delete-orphan")
    
    # Financial tracking
    labor_cost = Column(Float, default=0.0)
    total_parts_cost = Column(Float, default=0.0)
    
    def calculate_total(self):
        """Calculate the total cost of the ticket including parts and labor."""
        return self.labor_cost + self.total_parts_cost