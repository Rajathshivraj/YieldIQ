"""
Pydantic schemas for Product endpoints.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class ProductBase(BaseModel):
    product_name: str = Field(..., min_length=2, max_length=255)
    category: str = Field(..., pattern="^(Bond|Fixed Deposit|Invoice Discounting|Asset Leasing|Digital Gold|Alternative Investment)$")
    expected_return: float = Field(..., ge=0, le=100)
    tenure_months: int = Field(..., ge=1, le=360)
    risk_level: str = Field("Medium", pattern="^(Low|Medium|High)$")
    min_investment: float = Field(10000, ge=0)
    max_investment: Optional[float] = None
    description: Optional[str] = Field(None, max_length=1000)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    expected_return: Optional[float] = None
    tenure_months: Optional[int] = None
    risk_level: Optional[str] = None
    min_investment: Optional[float] = None
    max_investment: Optional[float] = None
    is_active: Optional[str] = None
    description: Optional[str] = None


class ProductResponse(ProductBase):
    product_id: UUID
    is_active: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    items: List[ProductResponse]
    total: int
