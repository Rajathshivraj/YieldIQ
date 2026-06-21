"""
Transaction routes.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from datetime import date

from app.db.session import get_db
from app.repositories.transaction_repo import TransactionRepository
from app.repositories.investor_repo import InvestorRepository
from app.repositories.product_repo import ProductRepository
from app.services.transaction_service import TransactionService
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponse, TransactionListResponse
from app.core.security import get_current_user, require_analyst

router = APIRouter(prefix="/transactions", tags=["Transactions"])


def get_service(db: Session = Depends(get_db)) -> TransactionService:
    return TransactionService(
        TransactionRepository(db),
        InvestorRepository(db),
        ProductRepository(db),
    )


@router.post("/", response_model=TransactionResponse, status_code=201)
def create_transaction(payload: TransactionCreate, service: TransactionService = Depends(get_service), _=Depends(require_analyst)):
    return service.create_transaction(payload)


@router.get("/", response_model=TransactionListResponse)
def list_transactions(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=500),
    investor_id: Optional[UUID] = None,
    product_id: Optional[UUID] = None,
    transaction_status: Optional[str] = None,
    category: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    search: Optional[str] = None,
    service: TransactionService = Depends(get_service),
    _=Depends(get_current_user),
):
    return service.list_transactions(
        page=page, page_size=page_size,
        investor_id=investor_id, product_id=product_id,
        transaction_status=transaction_status, category=category,
        date_from=date_from, date_to=date_to,
        min_amount=min_amount, max_amount=max_amount, search=search,
    )


@router.get("/{txn_id}", response_model=TransactionResponse)
def get_transaction(txn_id: UUID, service: TransactionService = Depends(get_service), _=Depends(get_current_user)):
    txn = service.repo.get_by_id(txn_id)
    if not txn:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Transaction not found")
    return service._to_response(txn)


@router.put("/{txn_id}", response_model=TransactionResponse)
def update_transaction(txn_id: UUID, payload: TransactionUpdate, service: TransactionService = Depends(get_service), _=Depends(require_analyst)):
    return service.update_transaction(txn_id, payload)
