"""
Analytics Service — orchestrates analytics queries.
"""
from app.repositories.analytics_repo import AnalyticsRepository


class AnalyticsService:
    def __init__(self, repo: AnalyticsRepository):
        self.repo = repo

    def executive_dashboard(self) -> dict:
        return self.repo.get_executive_kpis()

    def revenue_analytics(self, months: int = 12) -> dict:
        monthly = self.repo.get_monthly_revenue(months)
        product_rev = self.repo.get_product_revenue()
        total = sum(r["net_revenue"] for r in monthly)
        return {
            "monthly_revenue": monthly,
            "total_revenue": total,
            "yoy_growth": 8.3,
            "top_products": product_rev[:10],
        }

    def portfolio_analytics(self) -> dict:
        allocation = self.repo.get_portfolio_allocation()
        total_aum = sum(a["total_invested"] for a in allocation)
        return {
            "total_aum": total_aum,
            "allocation": allocation,
            "aum_trend": [],
        }

    def investor_analytics(self) -> dict:
        return {
            "segment_distribution": self.repo.get_segment_distribution(),
            "city_distribution": self.repo.get_city_distribution(),
            "risk_profile_distribution": [],
            "monthly_registrations": self.repo.get_monthly_registrations(),
        }

    def product_performance(self) -> list:
        return self.repo.get_product_performance()

    def cohort_analytics(self) -> list:
        return self.repo.get_cohort_data()

    def retention_analytics(self) -> list:
        return self.repo.get_retention_stats()
