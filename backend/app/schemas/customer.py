from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field

from app.schemas.bike import Bike


class CustomerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    notes: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)


class CustomerInDBBase(CustomerBase):
    id: int
    
    model_config = {
        "from_attributes": True
    }


class Customer(CustomerInDBBase):
    pass


class CustomerWithBikes(CustomerInDBBase):
    bikes: List[Bike] = []