from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from app.models.ticket import TicketStatus


class TicketUpdateBase(BaseModel):
    ticket_id: int
    previous_status: Optional[TicketStatus] = None
    new_status: TicketStatus
    note: Optional[str] = None
    user_id: int


class TicketUpdateCreate(TicketUpdateBase):
    pass


class TicketUpdateInDBBase(TicketUpdateBase):
    id: int
    timestamp: datetime
    
    class Config:
        orm_mode = True


class TicketUpdate(TicketUpdateInDBBase):
    pass