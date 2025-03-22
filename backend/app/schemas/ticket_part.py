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
    
    model_config = {
        "from_attributes": True
    }


class TicketPart(TicketPartInDBBase):
    part: Part
    total: float = 0
    profit: float = 0
    
    @classmethod
    def model_validate(cls, ticket_part, **kwargs):
        obj = TicketPart(**ticket_part.__dict__)
        obj.part = Part.model_validate(ticket_part.part)
        obj.total = ticket_part.calculate_total()
        obj.profit = ticket_part.calculate_profit()
        return obj
        
    # Keep backward compatibility
    @classmethod
    def from_orm(cls, obj):
        return cls.model_validate(obj)