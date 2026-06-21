"""
Investor Service — business logic layer.
"""
import math
from datetime import date
from typing import Optional, Tuple, List
from uuid import UUID

from fastapi import HTTPException, status

from app.repositories.investor_repo import InvestorRepository
from app.schemas.investor import InvestorCreate, InvestorUpdate, InvestorResponse, InvestorPortfolioSummary


def _compute_segment(total_invested: float) -> str:
    if total_invested >= 1_000_000:
        return "Platinum"
    elif total_invested >= 500_000:
        return "Gold"
    elif total_invested >= 100_000:
        return "Silver"
    return "New Investor"


class InvestorService:
    def __init__(self, repo: InvestorRepository):
        self.repo = repo

    def create_investor(self, payload: InvestorCreate) -> InvestorResponse:
        if self.repo.get_by_email(payload.email):
            raise HTTPException(status_code=409, detail="Email already registered")

        data = payload.model_dump()
        data["registration_date"] = data.get("registration_date") or date.today()
        data["investor_segment"] = "New Investor"
        data["status"] = "Active"

        investor = self.repo.create(data)
        return InvestorResponse.model_validate(investor)

    def get_investor(self, investor_id: UUID) -> InvestorResponse:
        investor = self.repo.get_by_id(investor_id)
        if not investor:
            raise HTTPException(status_code=404, detail="Investor not found")
        return InvestorResponse.model_validate(investor)

    def update_investor(self, investor_id: UUID, payload: InvestorUpdate) -> InvestorResponse:
        investor = self.repo.get_by_id(investor_id)
        if not investor:
            raise HTTPException(status_code=404, detail="Investor not found")
        updated = self.repo.update(investor, payload.model_dump(exclude_none=True))
        return InvestorResponse.model_validate(updated)

    def delete_investor(self, investor_id: UUID) -> dict:
        investor = self.repo.get_by_id(investor_id)
        if not investor:
            raise HTTPException(status_code=404, detail="Investor not found")
        self.repo.delete(investor)
        return {"message": "Investor deleted successfully"}

    def list_investors(
        self,
        page: int = 1,
        page_size: int = 50,
        search: Optional[str] = None,
        status: Optional[str] = None,
        segment: Optional[str] = None,
        risk_profile: Optional[str] = None,
        city: Optional[str] = None,
    ) -> dict:
        items, total = self.repo.list(
            page=page,
            page_size=page_size,
            search=search,
            status=status,
            segment=segment,
            risk_profile=risk_profile,
            city=city,
        )
        return {
            "items": [InvestorResponse.model_validate(i) for i in items],
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": math.ceil(total / page_size) if page_size else 1,
        }

    def get_portfolio_summary(self, investor_id: UUID) -> InvestorPortfolioSummary:
        investor = self.repo.get_by_id(investor_id)
        if not investor:
            raise HTTPException(status_code=404, detail="Investor not found")

        summary = self.repo.get_portfolio_summary(investor_id)
        segment = _compute_segment(summary["total_invested"])

        # Auto-update segment if changed
        if investor.investor_segment != segment:
            self.repo.update(investor, {"investor_segment": segment})

        return InvestorPortfolioSummary(
            investor_id=investor.investor_id,
            full_name=investor.full_name,
            investor_segment=segment,
            risk_profile=investor.risk_profile,
            **summary,
        )
