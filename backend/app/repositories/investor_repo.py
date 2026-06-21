"""
Investor Repository — database access layer.
"""
from sqlalchemy.orm import Session
from sqlalchemy import or_, func, desc
from typing import Optional, List, Tuple
from uuid import UUID

from app.models.investor import Investor
from app.models.transaction import Transaction


class InvestorRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict) -> Investor:
        investor = Investor(**data)
        self.db.add(investor)
        self.db.commit()
        self.db.refresh(investor)
        return investor

    def get_by_id(self, investor_id: UUID) -> Optional[Investor]:
        return self.db.query(Investor).filter(Investor.investor_id == investor_id).first()

    def get_by_email(self, email: str) -> Optional[Investor]:
        return self.db.query(Investor).filter(Investor.email == email).first()

    def update(self, investor: Investor, data: dict) -> Investor:
        for key, value in data.items():
            if value is not None:
                setattr(investor, key, value)
        self.db.commit()
        self.db.refresh(investor)
        return investor

    def delete(self, investor: Investor) -> None:
        self.db.delete(investor)
        self.db.commit()

    def list(
        self,
        page: int = 1,
        page_size: int = 50,
        search: Optional[str] = None,
        status: Optional[str] = None,
        segment: Optional[str] = None,
        risk_profile: Optional[str] = None,
        city: Optional[str] = None,
    ) -> Tuple[List[Investor], int]:
        query = self.db.query(Investor)

        if search:
            query = query.filter(
                or_(
                    Investor.full_name.ilike(f"%{search}%"),
                    Investor.email.ilike(f"%{search}%"),
                    Investor.city.ilike(f"%{search}%"),
                )
            )
        if status:
            query = query.filter(Investor.status == status)
        if segment:
            query = query.filter(Investor.investor_segment == segment)
        if risk_profile:
            query = query.filter(Investor.risk_profile == risk_profile)
        if city:
            query = query.filter(Investor.city == city)

        total = query.count()
        items = (
            query.order_by(desc(Investor.created_at))
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        return items, total

    def get_portfolio_summary(self, investor_id: UUID) -> dict:
        from sqlalchemy import case
        txns = self.db.query(Transaction).filter(Transaction.investor_id == investor_id).all()
        total_invested = sum(float(t.investment_amount) for t in txns)
        active = sum(1 for t in txns if t.transaction_status == "Active")
        matured = sum(1 for t in txns if t.transaction_status == "Matured")
        returns = [float(t.actual_return or t.expected_return) for t in txns]
        avg_return = sum(returns) / len(returns) if returns else 0.0
        categories = [t.product.category for t in txns if t.product]
        top_category = max(set(categories), key=categories.count) if categories else None
        return {
            "total_invested": total_invested,
            "active_investments": active,
            "matured_investments": matured,
            "total_transactions": len(txns),
            "portfolio_value": total_invested * (1 + avg_return / 100),
            "avg_return": avg_return,
            "top_product_category": top_category,
        }

    def count_by_segment(self) -> List[dict]:
        rows = (
            self.db.query(Investor.investor_segment, func.count(Investor.investor_id))
            .group_by(Investor.investor_segment)
            .all()
        )
        return [{"segment": r[0], "count": r[1]} for r in rows]
