"""
Cohort model — investor retention cohort analysis.
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Cohort(Base):
    __tablename__ = "cohorts"

    cohort_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cohort_month = Column(String(7), nullable=False)   # e.g. "2024-01"
    investor_id = Column(UUID(as_uuid=True), ForeignKey("investors.investor_id", ondelete="CASCADE"), nullable=False)
    retention_month = Column(Integer, nullable=False, default=0)
    is_retained = Column(String(5), nullable=False, default="Yes")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    investor = relationship("Investor", back_populates="cohorts")

    __table_args__ = (
        Index("idx_cohort_month", "cohort_month"),
        Index("idx_cohort_investor_id", "investor_id"),
        Index("idx_cohort_month_retention", "cohort_month", "retention_month"),
    )
