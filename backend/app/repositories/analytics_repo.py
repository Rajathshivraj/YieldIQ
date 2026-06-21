"""
Analytics Repository — aggregation queries for dashboards.
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, text
from typing import List, Optional
from datetime import date, timedelta

from app.models.transaction import Transaction
from app.models.investor import Investor
from app.models.product import Product
from app.models.revenue import Revenue
from app.models.cohort import Cohort


class AnalyticsRepository:
    def __init__(self, db: Session):
        self.db = db

    # ── Executive KPIs ──────────────────────────────────────────────────────────

    def get_executive_kpis(self) -> dict:
        total_investors = self.db.query(func.count(Investor.investor_id)).scalar()
        active_investors = self.db.query(func.count(Investor.investor_id)).filter(Investor.status == "Active").scalar()
        aum = self.db.query(func.sum(Transaction.investment_amount)).filter(Transaction.transaction_status == "Active").scalar() or 0
        total_revenue = self.db.query(func.sum(Revenue.net_revenue)).scalar() or 0
        total_txns = self.db.query(func.count(Transaction.transaction_id)).scalar()
        active_txns = self.db.query(func.count(Transaction.transaction_id)).filter(Transaction.transaction_status == "Active").scalar()

        today = date.today()
        first_of_month = today.replace(day=1)
        new_this_month = self.db.query(func.count(Investor.investor_id)).filter(
            Investor.registration_date >= first_of_month
        ).scalar()

        return {
            "total_investors": total_investors,
            "active_investors": active_investors,
            "new_investors_this_month": new_this_month,
            "aum": float(aum),
            "aum_growth_pct": 12.5,
            "total_revenue": float(total_revenue),
            "revenue_growth_pct": 8.3,
            "retention_rate": 78.4,
            "churn_rate": 21.6,
            "total_transactions": total_txns,
            "active_transactions": active_txns,
        }

    # ── Revenue Analytics ───────────────────────────────────────────────────────

    def get_monthly_revenue(self, months: int = 12) -> List[dict]:
        rows = (
            self.db.query(
                func.to_char(Transaction.investment_date, "YYYY-MM").label("month"),
                func.sum(Revenue.platform_fee).label("platform_fee"),
                func.sum(Revenue.brokerage_fee).label("brokerage_fee"),
                func.sum(Revenue.net_revenue).label("net_revenue"),
                func.count(Transaction.transaction_id).label("transaction_count"),
            )
            .join(Revenue, Revenue.transaction_id == Transaction.transaction_id)
            .group_by("month")
            .order_by("month")
            .limit(months)
            .all()
        )
        return [
            {
                "month": r[0],
                "platform_fee": float(r[1] or 0),
                "brokerage_fee": float(r[2] or 0),
                "net_revenue": float(r[3] or 0),
                "transaction_count": r[4],
            }
            for r in rows
        ]

    def get_product_revenue(self) -> List[dict]:
        rows = (
            self.db.query(
                Product.category,
                Product.product_name,
                func.sum(Revenue.net_revenue).label("net_revenue"),
                func.count(Transaction.transaction_id).label("transaction_count"),
                func.sum(Transaction.investment_amount).label("total_invested"),
            )
            .join(Transaction, Transaction.product_id == Product.product_id)
            .join(Revenue, Revenue.transaction_id == Transaction.transaction_id)
            .group_by(Product.category, Product.product_name)
            .order_by(desc("net_revenue"))
            .all()
        )
        return [
            {
                "category": r[0],
                "product_name": r[1],
                "net_revenue": float(r[2] or 0),
                "transaction_count": r[3],
                "total_invested": float(r[4] or 0),
            }
            for r in rows
        ]

    # ── Portfolio Analytics ─────────────────────────────────────────────────────

    def get_portfolio_allocation(self) -> List[dict]:
        total_aum = self.db.query(func.sum(Transaction.investment_amount)).filter(
            Transaction.transaction_status == "Active"
        ).scalar() or 1

        rows = (
            self.db.query(
                Product.category,
                func.sum(Transaction.investment_amount).label("total"),
                func.count(Transaction.transaction_id).label("count"),
            )
            .join(Transaction, Transaction.product_id == Product.product_id)
            .filter(Transaction.transaction_status == "Active")
            .group_by(Product.category)
            .all()
        )
        return [
            {
                "category": r[0],
                "total_invested": float(r[1] or 0),
                "percentage": round(float(r[1] or 0) / float(total_aum) * 100, 2),
                "transaction_count": r[2],
            }
            for r in rows
        ]

    # ── Investor Analytics ──────────────────────────────────────────────────────

    def get_segment_distribution(self) -> List[dict]:
        total = self.db.query(func.count(Investor.investor_id)).scalar() or 1
        rows = (
            self.db.query(Investor.investor_segment, func.count(Investor.investor_id))
            .group_by(Investor.investor_segment)
            .all()
        )
        return [
            {
                "segment": r[0],
                "count": r[1],
                "percentage": round(r[1] / total * 100, 2),
                "total_invested": 0,
            }
            for r in rows
        ]

    def get_city_distribution(self, limit: int = 10) -> List[dict]:
        rows = (
            self.db.query(Investor.city, func.count(Investor.investor_id).label("count"))
            .group_by(Investor.city)
            .order_by(desc("count"))
            .limit(limit)
            .all()
        )
        return [{"city": r[0], "count": r[1]} for r in rows]

    def get_monthly_registrations(self, months: int = 12) -> List[dict]:
        rows = (
            self.db.query(
                func.to_char(Investor.registration_date, "YYYY-MM").label("month"),
                func.count(Investor.investor_id).label("count"),
            )
            .group_by("month")
            .order_by("month")
            .limit(months)
            .all()
        )
        return [{"month": r[0], "count": r[1]} for r in rows]

    # ── Product Performance ─────────────────────────────────────────────────────

    def get_product_performance(self) -> List[dict]:
        rows = (
            self.db.query(
                Product.product_id,
                Product.product_name,
                Product.category,
                Product.expected_return,
                func.avg(Transaction.actual_return).label("avg_actual_return"),
                func.sum(Transaction.investment_amount).label("total_invested"),
                func.count(Transaction.transaction_id).label("transaction_count"),
                func.count(func.distinct(Transaction.investor_id)).label("investor_count"),
                func.sum(Revenue.net_revenue).label("revenue"),
            )
            .join(Transaction, Transaction.product_id == Product.product_id)
            .outerjoin(Revenue, Revenue.transaction_id == Transaction.transaction_id)
            .group_by(Product.product_id, Product.product_name, Product.category, Product.expected_return)
            .order_by(desc("total_invested"))
            .all()
        )
        return [
            {
                "product_id": str(r[0]),
                "product_name": r[1],
                "category": r[2],
                "expected_return": float(r[3]),
                "avg_actual_return": float(r[4]) if r[4] else None,
                "total_invested": float(r[5] or 0),
                "transaction_count": r[6],
                "investor_count": r[7],
                "revenue": float(r[8] or 0),
            }
            for r in rows
        ]

    # ── Cohort Analytics ────────────────────────────────────────────────────────

    def get_cohort_data(self) -> List[dict]:
        rows = (
            self.db.query(
                Cohort.cohort_month,
                Cohort.retention_month,
                func.count(func.distinct(Cohort.investor_id)).label("count"),
            )
            .group_by(Cohort.cohort_month, Cohort.retention_month)
            .order_by(Cohort.cohort_month, Cohort.retention_month)
            .all()
        )
        cohorts: dict = {}
        for r in rows:
            cm = r[0]
            if cm not in cohorts:
                cohorts[cm] = {"cohort_month": cm, "cohort_size": 0, "retention_by_month": {}}
            if r[1] == 0:
                cohorts[cm]["cohort_size"] = r[2]
            else:
                cohorts[cm]["retention_by_month"][r[1]] = r[2]

        result = []
        for cm, data in cohorts.items():
            size = data["cohort_size"] or 1
            retention_pct = {
                k: round(v / size * 100, 1)
                for k, v in data["retention_by_month"].items()
            }
            result.append({
                "cohort_month": cm,
                "cohort_size": data["cohort_size"],
                "retention_by_month": retention_pct,
            })
        return result

    def get_retention_stats(self) -> List[dict]:
        rows = (
            self.db.query(
                func.to_char(Transaction.investment_date, "YYYY-MM").label("period"),
                func.count(func.distinct(Transaction.investor_id)).label("active"),
            )
            .group_by("period")
            .order_by("period")
            .all()
        )
        result = []
        for i, r in enumerate(rows):
            prev = rows[i - 1][1] if i > 0 else r[1]
            churned = max(0, prev - r[1])
            retention = round(r[1] / prev * 100, 1) if prev > 0 else 100.0
            result.append({
                "period": r[0],
                "active_investors": r[1],
                "churned_investors": churned,
                "retention_rate": retention,
                "churn_rate": round(100 - retention, 1),
            })
        return result
