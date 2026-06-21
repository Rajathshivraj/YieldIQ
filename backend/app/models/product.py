"""
Product model — fixed income and alternative investment products.
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Numeric, Integer, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    product_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    expected_return = Column(Numeric(5, 2), nullable=False)
    tenure_months = Column(Integer, nullable=False)
    risk_level = Column(String(50), nullable=False, default="Medium")
    min_investment = Column(Numeric(15, 2), nullable=False, default=10000)
    max_investment = Column(Numeric(15, 2), nullable=True)
    is_active = Column(String(10), nullable=False, default="Yes")
    description = Column(String(1000), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    transactions = relationship("Transaction", back_populates="product", lazy="dynamic")

    __table_args__ = (
        Index("idx_product_category", "category"),
        Index("idx_product_risk_level", "risk_level"),
    )
