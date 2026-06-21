"""
Transaction Service — business logic layer.
"""
import math
from datetime import date
from typing import Optional
from uuid import UUID

from dateutil.relativedelta import relativedelta
from fastapi import HTTPException

from app.repositories.transaction_repo import TransactionRepository
from app.repositories.investor_repo import InvestorRepository
from app.repositories.product_repo import ProductRepository
from app.models.revenue import Revenue
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponse
from app.db.session import SessionLocal


class TransactionService:
    def __init__(
        self,
        repo: TransactionRepository,
        investor_repo: InvestorRepository,
        product_repo: ProductRepository,
    ):
        self.repo = repo
        self.investor_repo = investor_repo
        self.product_repo = product_repo

    def create_transaction(self, payload: TransactionCreate) -> TransactionResponse:
        investor = self.investor_repo.get_by_id(payload.investor_id)
        if not investor:
            raise HTTPException(status_code=404, detail="Investor not found")

        product = self.product_repo.get_by_id(payload.product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        if product.is_active != "Yes":
            raise HTTPException(status_code=400, detail="Product is not active")

        data = payload.model_dump()
        if not data.get("maturity_date"):
            data["maturity_date"] = payload.investment_date + relativedelta(months=int(product.tenure_months))
        data["expected_return"] = float(product.expected_return)
        data["transaction_status"] = "Active"

        txn = self.repo.create(data)

        # Auto-create revenue record
        platform_fee = float(payload.investment_amount) * 0.005   # 0.5%
        brokerage_fee = float(payload.investment_amount) * 0.003  # 0.3%
        rev = Revenue(
            transaction_id=txn.transaction_id,
            platform_fee=round(platform_fee, 2),
            brokerage_fee=round(brokerage_fee, 2),
            net_revenue=round(platform_fee + brokerage_fee, 2),
        )
        self.repo.db.add(rev)
        self.repo.db.commit()

        return self._to_response(txn)

    def update_transaction(self, txn_id: UUID, payload: TransactionUpdate) -> TransactionResponse:
        txn = self.repo.get_by_id(txn_id)
        if not txn:
            raise HTTPException(status_code=404, detail="Transaction not found")
        updated = self.repo.update(txn, payload.model_dump(exclude_none=True))
        return self._to_response(updated)

    def list_transactions(self, page: int = 1, page_size: int = 50, **filters) -> dict:
        items, total = self.repo.list(page=page, page_size=page_size, **filters)
        return {
            "items": [self._to_response(t) for t in items],
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": math.ceil(total / page_size) if page_size else 1,
        }

    def _to_response(self, txn) -> TransactionResponse:
        return TransactionResponse(
            transaction_id=txn.transaction_id,
            investor_id=txn.investor_id,
            product_id=txn.product_id,
            investment_amount=float(txn.investment_amount),
            investment_date=txn.investment_date,
            maturity_date=txn.maturity_date,
            expected_return=float(txn.expected_return),
            actual_return=float(txn.actual_return) if txn.actual_return else None,
            transaction_status=txn.transaction_status,
            notes=txn.notes,
            created_at=txn.created_at,
            updated_at=txn.updated_at,
            investor_name=txn.investor.full_name if txn.investor else None,
            product_name=txn.product.product_name if txn.product else None,
            product_category=txn.product.category if txn.product else None,
        )
