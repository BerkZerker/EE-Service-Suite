from typing import Optional, List
from pydantic import BaseModel, Field, computed_field


class PartBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=50)
    sku: Optional[str] = Field(None, max_length=50)
    
    quantity: int = 0
    min_stock: int = 0
    reorder_point: int = 0
    
    cost_price: float
    retail_price: float


class PartCreate(PartBase):
    pass


class PartUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    category: Optional[str] = None
    sku: Optional[str] = None
    
    quantity: Optional[int] = None
    min_stock: Optional[int] = None
    reorder_point: Optional[int] = None
    
    cost_price: Optional[float] = None
    retail_price: Optional[float] = None


class PartInDBBase(PartBase):
    id: int
    
    model_config = {
        "from_attributes": True
    }


class Part(PartInDBBase):
    @computed_field
    def markup(self) -> float:
        if self.cost_price and self.cost_price > 0:
            return ((self.retail_price - self.cost_price) / self.cost_price) * 100
        return 0