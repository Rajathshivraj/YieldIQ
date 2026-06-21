"""
Pydantic schemas for Analytics and Dashboard endpoints.
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import date


class KPICard(BaseModel):
    label: str
    value: Any
    change_pct: Optional[float] = None
    trend: Optional[str] = None  # "up" | "down" | "flat"


class ExecutiveDashboard(BaseModel):
    total_investors: int
    active_investors: int
    new_investors_this_month: int
    aum: float
    aum_growth_pct: float
    total_revenue: float
    revenue_growth_pct: float
    retention_rate: float
    churn_rate: float
    total_transactions: int
    active_transactions: int


class MonthlyRevenue(BaseModel):
    month: str
    platform_fee: float
    brokerage_fee: float
    net_revenue: float
    transaction_count: int


class ProductRevenue(BaseModel):
    category: str
    product_name: str
    net_revenue: float
    transaction_count: int
    total_invested: float


class InvestorSegmentStats(BaseModel):
    segment: str
    count: int
    total_invested: float
    percentage: float


class ProductPerformance(BaseModel):
    product_id: str
    product_name: str
    category: str
    expected_return: float
    avg_actual_return: Optional[float]
    total_invested: float
    transaction_count: int
    investor_count: int
    revenue: float


class CohortRow(BaseModel):
    cohort_month: str
    cohort_size: int
    retention_by_month: Dict[int, float]  # {1: 85.2, 2: 72.1, ...}


class RetentionStats(BaseModel):
    period: str
    active_investors: int
    churned_investors: int
    retention_rate: float
    churn_rate: float


class PortfolioAllocation(BaseModel):
    category: str
    total_invested: float
    percentage: float
    transaction_count: int


class RevenueAnalytics(BaseModel):
    monthly_revenue: List[MonthlyRevenue]
    total_revenue: float
    yoy_growth: float
    top_products: List[ProductRevenue]


class PortfolioAnalytics(BaseModel):
    total_aum: float
    allocation: List[PortfolioAllocation]
    aum_trend: List[Dict[str, Any]]


class InvestorAnalytics(BaseModel):
    segment_distribution: List[InvestorSegmentStats]
    city_distribution: List[Dict[str, Any]]
    risk_profile_distribution: List[Dict[str, Any]]
    monthly_registrations: List[Dict[str, Any]]
