"""
Product Repository.
"""
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional, List, Tuple
from uuid import UUID

from app.models.product import Product


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict) -> Product:
        product = Product(**data)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def get_by_id(self, product_id: UUID) -> Optional[Product]:
        return self.db.query(Product).filter(Product.product_id == product_id).first()

    def update(self, product: Product, data: dict) -> Product:
        for key, value in data.items():
            if value is not None:
                setattr(product, key, value)
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product: Product) -> None:
        self.db.delete(product)
        self.db.commit()

    def list(
        self,
        category: Optional[str] = None,
        risk_level: Optional[str] = None,
        is_active: Optional[str] = "Yes",
    ) -> List[Product]:
        query = self.db.query(Product)
        if category:
            query = query.filter(Product.category == category)
        if risk_level:
            query = query.filter(Product.risk_level == risk_level)
        if is_active:
            query = query.filter(Product.is_active == is_active)
        return query.order_by(desc(Product.created_at)).all()
