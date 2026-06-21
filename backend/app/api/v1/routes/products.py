"""
Product routes.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from app.db.session import get_db
from app.repositories.product_repo import ProductRepository
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse, ProductListResponse
from app.core.security import get_current_user, require_analyst, require_admin

router = APIRouter(prefix="/products", tags=["Products"])


def get_repo(db: Session = Depends(get_db)) -> ProductRepository:
    return ProductRepository(db)


@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(payload: ProductCreate, repo: ProductRepository = Depends(get_repo), _=Depends(require_admin)):
    return repo.create(payload.model_dump())


@router.get("/", response_model=ProductListResponse)
def list_products(
    category: Optional[str] = None,
    risk_level: Optional[str] = None,
    is_active: Optional[str] = "Yes",
    repo: ProductRepository = Depends(get_repo),
    _=Depends(get_current_user),
):
    items = repo.list(category=category, risk_level=risk_level, is_active=is_active)
    return {"items": items, "total": len(items)}


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: UUID, repo: ProductRepository = Depends(get_repo), _=Depends(get_current_user)):
    product = repo.get_by_id(product_id)
    if not product:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: UUID, payload: ProductUpdate, repo: ProductRepository = Depends(get_repo), _=Depends(require_analyst)):
    product = repo.get_by_id(product_id)
    if not product:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Product not found")
    return repo.update(product, payload.model_dump(exclude_none=True))


@router.delete("/{product_id}")
def delete_product(product_id: UUID, repo: ProductRepository = Depends(get_repo), _=Depends(require_admin)):
    product = repo.get_by_id(product_id)
    if not product:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Product not found")
    repo.delete(product)
    return {"message": "Product deleted successfully"}
