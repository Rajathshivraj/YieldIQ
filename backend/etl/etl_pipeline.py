"""
ETL Pipeline — automated KPI calculations, monthly aggregations, batch processing.
Run: python -m etl.etl_pipeline
"""
import sys
import os
import logging
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

import pandas as pd
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.models.investor import Investor
from app.models.transaction import Transaction
from app.models.revenue import Revenue
from app.models.product import Product

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


class ETLPipeline:
    """Pandas-based ETL pipeline for YieldIQ analytics."""

    def __init__(self):
        self.db = SessionLocal()

    def close(self):
        self.db.close()

    def load_transactions_df(self) -> pd.DataFrame:
        """Load all transactions into a DataFrame for analytics."""
        logger.info("Loading transactions into DataFrame...")
        query = (
            self.db.query(
                Transaction.transaction_id,
                Transaction.investor_id,
                Transaction.product_id,
                Transaction.investment_amount,
                Transaction.investment_date,
                Transaction.maturity_date,
                Transaction.expected_return,
                Transaction.actual_return,
                Transaction.transaction_status,
                Product.category,
                Product.product_name,
                Revenue.platform_fee,
                Revenue.brokerage_fee,
                Revenue.net_revenue,
            )
            .join(Product, Transaction.product_id == Product.product_id)
            .outerjoin(Revenue, Revenue.transaction_id == Transaction.transaction_id)
        )
        rows = query.all()
        df = pd.DataFrame(rows, columns=[
            "transaction_id", "investor_id", "product_id",
            "investment_amount", "investment_date", "maturity_date",
            "expected_return", "actual_return", "transaction_status",
            "category", "product_name",
            "platform_fee", "brokerage_fee", "net_revenue",
        ])
        df["investment_amount"] = pd.to_numeric(df["investment_amount"], errors="coerce")
        df["net_revenue"] = pd.to_numeric(df["net_revenue"], errors="coerce").fillna(0)
        df["investment_date"] = pd.to_datetime(df["investment_date"])
        df["year_month"] = df["investment_date"].dt.to_period("M").astype(str)
        logger.info(f"Loaded {len(df):,} transaction rows.")
        return df

    def compute_monthly_kpis(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aggregate KPIs by month."""
        logger.info("Computing monthly KPIs...")
        monthly = (
            df.groupby("year_month")
            .agg(
                transaction_count=("transaction_id", "count"),
                total_invested=("investment_amount", "sum"),
                total_revenue=("net_revenue", "sum"),
                unique_investors=("investor_id", "nunique"),
                avg_investment=("investment_amount", "mean"),
            )
            .reset_index()
            .sort_values("year_month")
        )
        monthly["revenue_growth_pct"] = monthly["total_revenue"].pct_change() * 100
        monthly["investment_growth_pct"] = monthly["total_invested"].pct_change() * 100
        logger.info(f"Computed monthly KPIs for {len(monthly)} months.")
        return monthly

    def compute_product_performance(self, df: pd.DataFrame) -> pd.DataFrame:
        """Product-level performance analytics."""
        logger.info("Computing product performance...")
        perf = (
            df.groupby(["category", "product_name"])
            .agg(
                transaction_count=("transaction_id", "count"),
                total_invested=("investment_amount", "sum"),
                total_revenue=("net_revenue", "sum"),
                unique_investors=("investor_id", "nunique"),
                avg_investment=("investment_amount", "mean"),
                avg_expected_return=("expected_return", "mean"),
            )
            .reset_index()
            .sort_values("total_invested", ascending=False)
        )
        perf["revenue_per_txn"] = perf["total_revenue"] / perf["transaction_count"]
        return perf

    def compute_investor_segments(self, df: pd.DataFrame) -> pd.DataFrame:
        """Investor segmentation analytics."""
        logger.info("Computing investor segments...")
        inv_totals = (
            df.groupby("investor_id")
            .agg(total_invested=("investment_amount", "sum"), txn_count=("transaction_id", "count"))
            .reset_index()
        )
        inv_totals["segment"] = pd.cut(
            inv_totals["total_invested"],
            bins=[0, 100_000, 500_000, 1_000_000, float("inf")],
            labels=["New Investor", "Silver", "Gold", "Platinum"],
        )
        segment_summary = (
            inv_totals.groupby("segment")
            .agg(investor_count=("investor_id", "count"), total_invested=("total_invested", "sum"))
            .reset_index()
        )
        return segment_summary

    def compute_retention_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        """Monthly investor retention analysis."""
        logger.info("Computing retention analysis...")
        monthly_inv = (
            df.groupby("year_month")["investor_id"]
            .apply(set)
            .reset_index()
            .rename(columns={"investor_id": "investors"})
            .sort_values("year_month")
        )
        monthly_inv["active_count"] = monthly_inv["investors"].apply(len)
        monthly_inv["retained_count"] = 0
        monthly_inv["retention_rate"] = 0.0

        for i in range(1, len(monthly_inv)):
            prev = monthly_inv.iloc[i - 1]["investors"]
            curr = monthly_inv.iloc[i]["investors"]
            retained = len(prev & curr)
            monthly_inv.at[monthly_inv.index[i], "retained_count"] = retained
            monthly_inv.at[monthly_inv.index[i], "retention_rate"] = (
                round(retained / len(prev) * 100, 2) if prev else 0.0
            )

        monthly_inv["churn_rate"] = 100 - monthly_inv["retention_rate"]
        monthly_inv.drop(columns=["investors"], inplace=True)
        return monthly_inv

    def export_to_csv(self, df: pd.DataFrame, filename: str):
        """Export DataFrame to CSV for Power BI compatibility."""
        path = os.path.join(os.path.dirname(__file__), "exports", filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        df.to_csv(path, index=False)
        logger.info(f"Exported {len(df):,} rows to {path}")

    def run(self):
        logger.info("=" * 60)
        logger.info("YieldIQ ETL Pipeline Starting...")
        logger.info("=" * 60)

        try:
            df = self.load_transactions_df()

            monthly_kpis = self.compute_monthly_kpis(df)
            self.export_to_csv(monthly_kpis, "monthly_kpis.csv")

            product_perf = self.compute_product_performance(df)
            self.export_to_csv(product_perf, "product_performance.csv")

            segments = self.compute_investor_segments(df)
            self.export_to_csv(segments, "investor_segments.csv")

            retention = self.compute_retention_analysis(df)
            self.export_to_csv(retention, "retention_analysis.csv")

            logger.info("=" * 60)
            logger.info("✅ ETL Pipeline complete. Exports saved to etl/exports/")
            logger.info("=" * 60)

        except Exception as e:
            logger.error(f"ETL failed: {e}")
            raise
        finally:
            self.close()


if __name__ == "__main__":
    pipeline = ETLPipeline()
    pipeline.run()
