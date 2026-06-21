"""
Investor routes.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from app.db.session import get_db
from app.repositories.investor_repo import InvestorRepository
from app.services.investor_service import InvestorService
from app.schemas.investor import InvestorCreate, InvestorUpdate, InvestorResponse, InvestorListResponse, InvestorPortfolioSummary
from app.core.security import get_current_user, require_analyst, require_admin

router = APIRouter(prefix="/investors", tags=["Investors"])


def get_service(db: Session = Depends(get_db)) -> InvestorService:
    return InvestorService(InvestorRepository(db))


@router.post("/", response_model=InvestorResponse, status_code=201)
def create_investor(payload: InvestorCreate, service: InvestorService = Depends(get_service), _=Depends(require_analyst)):
    return service.create_investor(payload)


@router.get("/", response_model=InvestorListResponse)
def list_investors(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=500),
    search: Optional[str] = None,
    status: Optional[str] = None,
    segment: Optional[str] = None,
    risk_profile: Optional[str] = None,
    city: Optional[str] = None,
    service: InvestorService = Depends(get_service),
    _=Depends(get_current_user),
):
    return service.list_investors(
        page=page, page_size=page_size, search=search,
        status=status, segment=segment, risk_profile=risk_profile, city=city,
    )


@router.get("/{investor_id}", response_model=InvestorResponse)
def get_investor(investor_id: UUID, service: InvestorService = Depends(get_service), _=Depends(get_current_user)):
    return service.get_investor(investor_id)


@router.put("/{investor_id}", response_model=InvestorResponse)
def update_investor(investor_id: UUID, payload: InvestorUpdate, service: InvestorService = Depends(get_service), _=Depends(require_analyst)):
    return service.update_investor(investor_id, payload)


@router.delete("/{investor_id}")
def delete_investor(investor_id: UUID, service: InvestorService = Depends(get_service), _=Depends(require_admin)):
    return service.delete_investor(investor_id)


@router.get("/{investor_id}/portfolio", response_model=InvestorPortfolioSummary)
def get_portfolio(investor_id: UUID, service: InvestorService = Depends(get_service), _=Depends(get_current_user)):
    return service.get_portfolio_summary(investor_id)
