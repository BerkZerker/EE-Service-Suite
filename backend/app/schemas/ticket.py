from typing import Optional, List, Any
from datetime import datetime
from pydantic import BaseModel, Field

from app.models.ticket import TicketStatus, TicketPriority


class TicketBase(BaseModel):
    ticket_number: str = Field(..., min_length=3, max_length=20)
    problem_description: str
    diagnosis: Optional[str] = None
    status: TicketStatus = TicketStatus.INTAKE
    priority: TicketPriority = TicketPriority.MEDIUM
    estimated_completion: Optional[datetime] = None
    bike_id: int
    technician_id: Optional[int] = None
    labor_cost: float = 0.0
    is_archived: bool = False


class TicketCreate(TicketBase):
    pass


class TicketUpdate(BaseModel):
    problem_description: Optional[str] = None
    diagnosis: Optional[str] = None
    status: Optional[TicketStatus] = None
    priority: Optional[TicketPriority] = None
    estimated_completion: Optional[datetime] = None
    technician_id: Optional[int] = None
    labor_cost: Optional[float] = None
    note: Optional[str] = None
    is_archived: Optional[bool] = None


class TicketArchiveRequest(BaseModel):
    """Schema for archive/unarchive requests"""
    note: Optional[str] = None


class TicketInDBBase(TicketBase):
    id: int
    created_at: datetime
    updated_at: datetime
    total_parts_cost: float
    
    model_config = {
        "from_attributes": True
    }


class Ticket(TicketInDBBase):
    pass


from app.schemas.ticket_update import TicketUpdate as TicketUpdateSchema
from app.schemas.ticket_part import TicketPart


class TicketWithDetails(TicketInDBBase):
    updates: List[TicketUpdateSchema] = []
    parts: List[TicketPart] = []
    
    total: float = 0
    
    @classmethod
    def model_validate(cls, ticket: Any, **kwargs) -> 'TicketWithDetails':
        obj = TicketWithDetails(**ticket.__dict__)
        obj.total = ticket.calculate_total()
        return obj
        
    # Keep backward compatibility
    @classmethod
    def from_orm(cls, obj):
        return cls.model_validate(obj)