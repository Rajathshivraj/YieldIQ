"""
Revenue model — platform fee and brokerage per transaction.
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, Numeric, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Revenue(Base):
    __tablename__ = "revenue"

    revenue_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transaction_id = Column(UUID(as_uuid=True), ForeignKey("transactions.transaction_id", ondelete="CASCADE"), nullable=False, unique=True)
    platform_fee = Column(Numeric(15, 2), nullable=False, default=0)
    brokerage_fee = Column(Numeric(15, 2), nullable=False, default=0)
    net_revenue = Column(Numeric(15, 2), nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    transaction = relationship("Transaction", back_populates="revenue")

    __table_args__ = (
        Index("idx_revenue_transaction_id", "transaction_id"),
    )
