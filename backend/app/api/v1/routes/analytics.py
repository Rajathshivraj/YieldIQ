"""
Analytics routes — revenue, portfolio, investor, cohort, retention, product performance.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.analytics_repo import AnalyticsRepository
from app.services.analytics_service import AnalyticsService
from app.core.security import get_current_user

router = APIRouter(prefix="/analytics", tags=["Analytics"])


def get_service(db: Session = Depends(get_db)) -> AnalyticsService:
    return AnalyticsService(AnalyticsRepository(db))


@router.get("/dashboard/executive")
def executive_dashboard(service: AnalyticsService = Depends(get_service), _=Depends(get_current_user)):
    return service.executive_dashboard()


@router.get("/revenue")
def revenue_analytics(
    months: int = Query(12, ge=1, le=60),
    service: AnalyticsService = Depends(get_service),
    _=Depends(get_current_user),
):
    return service.revenue_analytics(months)


@router.get("/portfolio")
def portfolio_analytics(service: AnalyticsService = Depends(get_service), _=Depends(get_current_user)):
    return service.portfolio_analytics()


@router.get("/investors")
def investor_analytics(service: AnalyticsService = Depends(get_service), _=Depends(get_current_user)):
    return service.investor_analytics()


@router.get("/products/performance")
def product_performance(service: AnalyticsService = Depends(get_service), _=Depends(get_current_user)):
    return service.product_performance()


@router.get("/cohorts")
def cohort_analytics(service: AnalyticsService = Depends(get_service), _=Depends(get_current_user)):
    return service.cohort_analytics()


@router.get("/retention")
def retention_analytics(service: AnalyticsService = Depends(get_service), _=Depends(get_current_user)):
    return service.retention_analytics()
