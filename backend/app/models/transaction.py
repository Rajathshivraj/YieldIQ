"""
Transaction model — core investment transaction records.
"""
import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Numeric, Date, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    investor_id = Column(UUID(as_uuid=True), ForeignKey("investors.investor_id", ondelete="CASCADE"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.product_id", ondelete="RESTRICT"), nullable=False)
    investment_amount = Column(Numeric(15, 2), nullable=False)
    investment_date = Column(Date, nullable=False, default=date.today)
    maturity_date = Column(Date, nullable=False)
    expected_return = Column(Numeric(5, 2), nullable=False)
    actual_return = Column(Numeric(5, 2), nullable=True)
    transaction_status = Column(String(50), nullable=False, default="Active")
    notes = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    investor = relationship("Investor", back_populates="transactions")
    product = relationship("Product", back_populates="transactions")
    revenue = relationship("Revenue", back_populates="transaction", uselist=False)

    __table_args__ = (
        Index("idx_txn_investor_id", "investor_id"),
        Index("idx_txn_product_id", "product_id"),
        Index("idx_txn_investment_date", "investment_date"),
        Index("idx_txn_status", "transaction_status"),
        Index("idx_txn_investor_date", "investor_id", "investment_date"),
    )
