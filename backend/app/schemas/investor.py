"""
Pydantic schemas for Investor endpoints.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date, datetime
from uuid import UUID


class InvestorBase(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    city: Optional[str] = Field(None, max_length=100)
    risk_profile: str = Field("Moderate", pattern="^(Conservative|Moderate|Aggressive)$")
    kyc_verified: str = Field("Yes")
    pan_number: Optional[str] = None


class InvestorCreate(InvestorBase):
    registration_date: Optional[date] = None


class InvestorUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    risk_profile: Optional[str] = None
    status: Optional[str] = None
    investor_segment: Optional[str] = None


class InvestorResponse(InvestorBase):
    investor_id: UUID
    registration_date: date
    investor_segment: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class InvestorPortfolioSummary(BaseModel):
    investor_id: UUID
    full_name: str
    total_invested: float
    active_investments: int
    matured_investments: int
    total_transactions: int
    portfolio_value: float
    avg_return: float
    investor_segment: str
    risk_profile: str
    top_product_category: Optional[str] = None


class InvestorListResponse(BaseModel):
    items: List[InvestorResponse]
    total: int
    page: int
    page_size: int
    pages: int
