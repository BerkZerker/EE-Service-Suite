from typing import Optional, List
from pydantic import BaseModel, Field


class BikeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    specs: Optional[str] = None
    owner_id: Optional[int] = None


class BikeCreate(BikeBase):
    owner_id: int


class BikeUpdate(BikeBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    owner_id: Optional[int] = None


class BikeInDBBase(BikeBase):
    id: int
    
    model_config = {
        "from_attributes": True
    }


class Bike(BikeInDBBase):
    pass


# Avoiding circular imports
from app.schemas.ticket import Ticket


class BikeWithTickets(BikeInDBBase):
    tickets: List[Ticket] = []