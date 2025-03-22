from typing import Optional
from pydantic import BaseModel

from app.schemas.part import Part


class TicketPartBase(BaseModel):
    ticket_id: int
    part_id: int
    quantity: int = 1
    price_charged: float


class TicketPartCreate(TicketPartBase):
    pass


class TicketPartUpdate(BaseModel):
    quantity: Optional[int] = None
    price_charged: Optional[float] = None


class TicketPartInDBBase(TicketPartBase):
    id: int
    
    class Config:
        orm_mode = True


class TicketPart(TicketPartInDBBase):
    part: Part
    total: float = 0
    profit: float = 0
    
    @staticmethod
    def from_orm(ticket_part):
        obj = TicketPart(**ticket_part.__dict__)
        obj.part = Part.from_orm(ticket_part.part)
        obj.total = ticket_part.calculate_total()
        obj.profit = ticket_part.calculate_profit()
        return obj