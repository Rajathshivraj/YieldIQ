"""
Investor model — core entity of the platform.
"""
import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Date, DateTime, Enum, Index, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class RiskProfile(str, enum.Enum):
    conservative = "Conservative"
    moderate = "Moderate"
    aggressive = "Aggressive"


class InvestorSegment(str, enum.Enum):
    platinum = "Platinum"
    gold = "Gold"
    silver = "Silver"
    new_investor = "New Investor"


class InvestorStatus(str, enum.Enum):
    active = "Active"
    inactive = "Inactive"
    churned = "Churned"


class Investor(Base):
    __tablename__ = "investors"

    investor_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    city = Column(String(100), nullable=True)
    registration_date = Column(Date, nullable=False, default=date.today)
    risk_profile = Column(String(50), nullable=False, default="Moderate")
    investor_segment = Column(String(50), nullable=False, default="New Investor")
    status = Column(String(50), nullable=False, default="Active")
    kyc_verified = Column(String(10), nullable=False, default="Yes")
    pan_number = Column(String(15), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    transactions = relationship("Transaction", back_populates="investor", lazy="dynamic")
    cohorts = relationship("Cohort", back_populates="investor", lazy="dynamic")

    __table_args__ = (
        Index("idx_investor_status", "status"),
        Index("idx_investor_segment", "investor_segment"),
        Index("idx_investor_registration_date", "registration_date"),
    )
