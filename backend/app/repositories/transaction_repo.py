"""
Transaction Repository — optimized for large-scale data.
"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, func, desc, and_
from typing import Optional, List, Tuple
from uuid import UUID
from datetime import date

from app.models.transaction import Transaction
from app.models.investor import Investor
from app.models.product import Product
from app.models.revenue import Revenue


class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict) -> Transaction:
        txn = Transaction(**data)
        self.db.add(txn)
        self.db.commit()
        self.db.refresh(txn)
        return txn

    def get_by_id(self, txn_id: UUID) -> Optional[Transaction]:
        return (
            self.db.query(Transaction)
            .options(joinedload(Transaction.investor), joinedload(Transaction.product))
            .filter(Transaction.transaction_id == txn_id)
            .first()
        )

    def update(self, txn: Transaction, data: dict) -> Transaction:
        for key, value in data.items():
            if value is not None:
                setattr(txn, key, value)
        self.db.commit()
        self.db.refresh(txn)
        return txn

    def list(
        self,
        page: int = 1,
        page_size: int = 50,
        investor_id: Optional[UUID] = None,
        product_id: Optional[UUID] = None,
        transaction_status: Optional[str] = None,
        category: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        min_amount: Optional[float] = None,
        max_amount: Optional[float] = None,
        search: Optional[str] = None,
    ) -> Tuple[List[Transaction], int]:
        query = (
            self.db.query(Transaction)
            .options(joinedload(Transaction.investor), joinedload(Transaction.product))
        )

        if investor_id:
            query = query.filter(Transaction.investor_id == investor_id)
        if product_id:
            query = query.filter(Transaction.product_id == product_id)
        if transaction_status:
            query = query.filter(Transaction.transaction_status == transaction_status)
        if date_from:
            query = query.filter(Transaction.investment_date >= date_from)
        if date_to:
            query = query.filter(Transaction.investment_date <= date_to)
        if min_amount:
            query = query.filter(Transaction.investment_amount >= min_amount)
        if max_amount:
            query = query.filter(Transaction.investment_amount <= max_amount)
        if category:
            query = query.join(Product).filter(Product.category == category)
        if search:
            query = query.join(Investor).filter(
                or_(
                    Investor.full_name.ilike(f"%{search}%"),
                    Investor.email.ilike(f"%{search}%"),
                )
            )

        total = query.count()
        items = (
            query.order_by(desc(Transaction.investment_date))
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        return items, total

    def get_monthly_volume(self) -> List[dict]:
        rows = (
            self.db.query(
                func.to_char(Transaction.investment_date, "YYYY-MM").label("month"),
                func.count(Transaction.transaction_id).label("count"),
                func.sum(Transaction.investment_amount).label("total"),
            )
            .group_by("month")
            .order_by("month")
            .all()
        )
        return [{"month": r[0], "count": r[1], "total": float(r[2] or 0)} for r in rows]
