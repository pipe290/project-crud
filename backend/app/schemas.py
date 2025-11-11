"""
Pydantic schemas for request/response validation.
"""

from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    description: Optional[str] = None
    price: float = Field(..., ge=0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)

class ProductOut(ProductBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
