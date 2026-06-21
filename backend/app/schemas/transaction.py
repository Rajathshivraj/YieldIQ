"""
Pydantic schemas for Transaction endpoints.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from uuid import UUID


class TransactionBase(BaseModel):
    investor_id: UUID
    product_id: UUID
    investment_amount: float = Field(..., ge=1000)
    investment_date: date
    maturity_date: date
    expected_return: float = Field(..., ge=0, le=100)


class TransactionCreate(TransactionBase):
    notes: Optional[str] = None


class TransactionUpdate(BaseModel):
    transaction_status: Optional[str] = None
    actual_return: Optional[float] = None
    notes: Optional[str] = None


class TransactionResponse(TransactionBase):
    transaction_id: UUID
    actual_return: Optional[float] = None
    transaction_status: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    # Joined fields
    investor_name: Optional[str] = None
    product_name: Optional[str] = None
    product_category: Optional[str] = None

    class Config:
        from_attributes = True


class TransactionListResponse(BaseModel):
    items: List[TransactionResponse]
    total: int
    page: int
    page_size: int
    pages: int


class TransactionFilters(BaseModel):
    investor_id: Optional[UUID] = None
    product_id: Optional[UUID] = None
    transaction_status: Optional[str] = None
    category: Optional[str] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    search: Optional[str] = None
