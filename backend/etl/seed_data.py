"""
YieldIQ Seed Data Generator
Generates: 20,000 investors, 15 products, 100,000+ transactions, revenue records, cohorts.
Uses Faker for realistic Indian fintech data.
Run: python -m etl.seed_data
"""
import sys
import os
import random
import uuid
import logging
from datetime import date, timedelta
from decimal import Decimal

import numpy as np
import pandas as pd
from faker import Faker
from dateutil.relativedelta import relativedelta
from sqlalchemy import text

# Add backend root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.models.user import User
from app.models.investor import Investor
from app.models.product import Product
from app.models.transaction import Transaction
from app.models.revenue import Revenue
from app.models.cohort import Cohort
from app.core.security import get_password_hash

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

fake = Faker("en_IN")
Faker.seed(42)
np.random.seed(42)
random.seed(42)

# ── Config ─────────────────────────────────────────────────────────────────────
NUM_INVESTORS = 20_000
NUM_TRANSACTIONS = 100_000
BATCH_SIZE = 1_000
START_DATE = date(2021, 1, 1)
END_DATE = date(2025, 12, 31)

INDIAN_CITIES = [
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata",
    "Pune", "Ahmedabad", "Jaipur", "Surat", "Lucknow", "Kanpur",
    "Nagpur", "Indore", "Thane", "Bhopal", "Visakhapatnam", "Pimpri-Chinchwad",
    "Patna", "Vadodara", "Ghaziabad", "Ludhiana", "Agra", "Nashik",
    "Faridabad", "Meerut", "Rajkot", "Kalyan", "Vasai-Virar", "Varanasi",
]

PRODUCTS_DATA = [
    {"name": "Government Securities Bond 2027", "category": "Bond", "return": 7.25, "tenure": 36, "risk": "Low", "min_inv": 10000},
    {"name": "Corporate Bond Series A", "category": "Bond", "return": 9.50, "tenure": 24, "risk": "Medium", "min_inv": 50000},
    {"name": "SBI Fixed Deposit Premium", "category": "Fixed Deposit", "return": 7.10, "tenure": 12, "risk": "Low", "min_inv": 10000},
    {"name": "HDFC Bank FD Plus", "category": "Fixed Deposit", "return": 7.40, "tenure": 24, "risk": "Low", "min_inv": 25000},
    {"name": "Invoice Discounting - SME Fund", "category": "Invoice Discounting", "return": 12.50, "tenure": 3, "risk": "Medium", "min_inv": 100000},
    {"name": "Invoice Discounting - Enterprise", "category": "Invoice Discounting", "return": 14.00, "tenure": 6, "risk": "High", "min_inv": 200000},
    {"name": "Commercial Vehicle Leasing Fund", "category": "Asset Leasing", "return": 11.00, "tenure": 48, "risk": "Medium", "min_inv": 100000},
    {"name": "Medical Equipment Leasing", "category": "Asset Leasing", "return": 13.00, "tenure": 36, "risk": "Medium", "min_inv": 150000},
    {"name": "Digital Gold SIP", "category": "Digital Gold", "return": 8.50, "tenure": 12, "risk": "Medium", "min_inv": 5000},
    {"name": "Digital Gold Plus", "category": "Digital Gold", "return": 10.00, "tenure": 24, "risk": "Medium", "min_inv": 10000},
    {"name": "AIF Category II - Real Estate", "category": "Alternative Investment", "return": 15.00, "tenure": 60, "risk": "High", "min_inv": 1000000},
    {"name": "AIF Category III - Equity Hedge", "category": "Alternative Investment", "return": 18.00, "tenure": 36, "risk": "High", "min_inv": 1000000},
    {"name": "High Yield NCD 2026", "category": "Bond", "return": 11.50, "tenure": 18, "risk": "Medium", "min_inv": 10000},
    {"name": "Renewable Energy Asset Leasing", "category": "Asset Leasing", "return": 12.50, "tenure": 60, "risk": "Medium", "min_inv": 250000},
    {"name": "Working Capital Invoice Fund", "category": "Invoice Discounting", "return": 13.50, "tenure": 3, "risk": "High", "min_inv": 500000},
]

RISK_PROFILES = ["Conservative", "Moderate", "Aggressive"]
RISK_WEIGHTS = [0.30, 0.50, 0.20]

STATUSES = ["Active", "Inactive", "Churned"]
STATUS_WEIGHTS = [0.75, 0.15, 0.10]

TXN_STATUSES = ["Active", "Matured", "Cancelled", "Defaulted"]
TXN_STATUS_WEIGHTS = [0.55, 0.38, 0.05, 0.02]


def random_date(start: date, end: date) -> date:
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))


def compute_segment(total_invested: float) -> str:
    if total_invested >= 1_000_000:
        return "Platinum"
    elif total_invested >= 500_000:
        return "Gold"
    elif total_invested >= 100_000:
        return "Silver"
    return "New Investor"


def generate_investors() -> list:
    logger.info(f"Generating {NUM_INVESTORS:,} investors...")
    investors = []
    for i in range(NUM_INVESTORS):
        reg_date = random_date(START_DATE, END_DATE)
        risk = random.choices(RISK_PROFILES, RISK_WEIGHTS)[0]
        status = random.choices(STATUSES, STATUS_WEIGHTS)[0]
        investors.append({
            "investor_id": uuid.uuid4(),
            "full_name": fake.name(),
            "email": f"investor{i+1}_{fake.unique.user_name()}@{fake.domain_name()}",
            "phone": fake.phone_number()[:20],
            "city": random.choice(INDIAN_CITIES),
            "registration_date": reg_date,
            "risk_profile": risk,
            "investor_segment": "New Investor",  # updated after transactions
            "status": status,
            "kyc_verified": random.choices(["Yes", "No"], [0.92, 0.08])[0],
            "pan_number": f"{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=5))}{random.randint(1000, 9999)}{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=1))}",
        })
        if (i + 1) % 5000 == 0:
            logger.info(f"  {i+1:,} investors generated...")
    return investors


def generate_products() -> list:
    logger.info("Generating products...")
    products = []
    for p in PRODUCTS_DATA:
        products.append({
            "product_id": uuid.uuid4(),
            "product_name": p["name"],
            "category": p["category"],
            "expected_return": p["return"],
            "tenure_months": p["tenure"],
            "risk_level": p["risk"],
            "min_investment": p["min_inv"],
            "max_investment": p["min_inv"] * 100,
            "is_active": "Yes",
            "description": f"A premium {p['category']} product offering {p['return']}% expected annual returns with {p['tenure']} months tenure.",
        })
    return products


def generate_transactions(investor_ids: list, products: list) -> tuple:
    logger.info(f"Generating {NUM_TRANSACTIONS:,} transactions...")
    transactions = []
    revenues = []

    # Weight investors for investment (some invest more than others — power law)
    weights = np.random.power(0.5, NUM_INVESTORS)
    weights = weights / weights.sum()

    txn_count = 0
    batch_investors = np.random.choice(
        range(NUM_INVESTORS), size=NUM_TRANSACTIONS, p=weights
    )

    for idx in batch_investors:
        investor_id = investor_ids[idx]
        product = random.choice(products)

        min_inv = float(product["min_investment"])
        # Investment amounts follow log-normal distribution
        amount = min(
            max(
                np.random.lognormal(mean=np.log(min_inv * 2), sigma=1.2),
                min_inv
            ),
            float(product["max_investment"])
        )
        amount = round(amount / 1000) * 1000  # round to nearest 1000

        inv_date = random_date(START_DATE, END_DATE)
        maturity_date = inv_date + relativedelta(months=int(product["tenure_months"]))

        status = random.choices(TXN_STATUSES, TXN_STATUS_WEIGHTS)[0]

        # Actual return: near expected, with noise
        expected_ret = float(product["expected_return"])
        if status == "Matured":
            actual_ret = round(expected_ret + np.random.normal(0, 0.5), 2)
        elif status == "Defaulted":
            actual_ret = round(expected_ret * random.uniform(-0.5, 0.3), 2)
        else:
            actual_ret = None

        txn_id = uuid.uuid4()
        transactions.append({
            "transaction_id": txn_id,
            "investor_id": investor_id,
            "product_id": product["product_id"],
            "investment_amount": round(amount, 2),
            "investment_date": inv_date,
            "maturity_date": maturity_date,
            "expected_return": expected_ret,
            "actual_return": actual_ret,
            "transaction_status": status,
            "notes": None,
        })

        # Revenue
        platform_fee = round(amount * 0.005, 2)
        brokerage_fee = round(amount * 0.003, 2)
        revenues.append({
            "revenue_id": uuid.uuid4(),
            "transaction_id": txn_id,
            "platform_fee": platform_fee,
            "brokerage_fee": brokerage_fee,
            "net_revenue": round(platform_fee + brokerage_fee, 2),
        })

        txn_count += 1
        if txn_count % 10000 == 0:
            logger.info(f"  {txn_count:,} transactions generated...")

    return transactions, revenues


def generate_cohorts(investor_ids: list, transactions: list) -> list:
    logger.info("Generating cohort data...")
    # Build investor registration month map
    cohorts = []

    # Group transactions by investor
    inv_txn_months: dict = {}
    for t in transactions:
        inv_id = str(t["investor_id"])
        month = t["investment_date"].strftime("%Y-%m")
        if inv_id not in inv_txn_months:
            inv_txn_months[inv_id] = set()
        inv_txn_months[inv_id].add(month)

    # Create cohort records (sample 5000 investors for performance)
    sample_ids = random.sample(investor_ids, min(5000, len(investor_ids)))
    for inv_id in sample_ids:
        months = sorted(inv_txn_months.get(str(inv_id), []))
        if not months:
            continue
        cohort_month = months[0]
        cohorts.append({
            "cohort_id": uuid.uuid4(),
            "cohort_month": cohort_month,
            "investor_id": inv_id,
            "retention_month": 0,
            "is_retained": "Yes",
        })
        for i, m in enumerate(months[1:], 1):
            cohorts.append({
                "cohort_id": uuid.uuid4(),
                "cohort_month": cohort_month,
                "investor_id": inv_id,
                "retention_month": i,
                "is_retained": "Yes",
            })

    return cohorts


def bulk_insert(db, model, records: list, label: str):
    logger.info(f"Inserting {len(records):,} {label}...")
    for i in range(0, len(records), BATCH_SIZE):
        batch = records[i:i + BATCH_SIZE]
        db.bulk_insert_mappings(model, batch)
        db.commit()
        if (i + BATCH_SIZE) % 10000 == 0 or i + BATCH_SIZE >= len(records):
            logger.info(f"  {min(i + BATCH_SIZE, len(records)):,}/{len(records):,} {label} inserted.")


def update_investor_segments(db, transactions: list):
    logger.info("Updating investor segments based on total investment...")
    inv_totals: dict = {}
    for t in transactions:
        inv_id = str(t["investor_id"])
        inv_totals[inv_id] = inv_totals.get(inv_id, 0) + float(t["investment_amount"])

    updated = 0
    for inv_id, total in inv_totals.items():
        segment = compute_segment(total)
        db.query(Investor).filter(Investor.investor_id == inv_id).update(
            {"investor_segment": segment}, synchronize_session=False
        )
        updated += 1
        if updated % 5000 == 0:
            db.commit()
            logger.info(f"  {updated:,} segments updated...")
    db.commit()
    logger.info(f"  {updated:,} investor segments updated.")


def seed_admin_users(db):
    logger.info("Seeding admin users...")
    users = [
        User(email="admin@yieldiq.com", full_name="YieldIQ Admin",
             hashed_password=get_password_hash("Admin@123"), role="admin", is_active=True),
        User(email="analyst@yieldiq.com", full_name="YieldIQ Analyst",
             hashed_password=get_password_hash("Analyst@123"), role="analyst", is_active=True),
        User(email="viewer@yieldiq.com", full_name="YieldIQ Viewer",
             hashed_password=get_password_hash("Viewer@123"), role="readonly", is_active=True),
    ]
    for u in users:
        existing = db.query(User).filter(User.email == u.email).first()
        if not existing:
            db.add(u)
    db.commit()
    logger.info("Admin users seeded.")


def main():
    logger.info("=" * 60)
    logger.info("YieldIQ Seed Data Generator")
    logger.info("=" * 60)

    # Create all tables
    logger.info("Creating database schema...")
    Base.metadata.create_all(bind=engine)
    logger.info("Schema created.")

    db = SessionLocal()
    try:
        # Check if already seeded
        existing = db.query(Investor).count()
        if existing > 1000:
            logger.warning(f"Database already has {existing:,} investors. Skipping seed.")
            logger.warning("To re-seed, truncate the tables first.")
            return

        seed_admin_users(db)

        # Generate data
        investors = generate_investors()
        products = generate_products()
        investor_ids = [i["investor_id"] for i in investors]
        transactions, revenues = generate_transactions(investor_ids, products)
        cohorts = generate_cohorts(investor_ids, transactions)

        # Insert in order (FK constraints)
        bulk_insert(db, Investor, investors, "investors")
        bulk_insert(db, Product, products, "products")
        bulk_insert(db, Transaction, transactions, "transactions")
        bulk_insert(db, Revenue, revenues, "revenue records")
        bulk_insert(db, Cohort, cohorts, "cohort records")

        # Update segments
        update_investor_segments(db, transactions)

        logger.info("=" * 60)
        logger.info("✅ Seed data generation complete!")
        logger.info(f"   Investors:    {len(investors):>10,}")
        logger.info(f"   Products:     {len(products):>10,}")
        logger.info(f"   Transactions: {len(transactions):>10,}")
        logger.info(f"   Revenue rows: {len(revenues):>10,}")
        logger.info(f"   Cohort rows:  {len(cohorts):>10,}")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"Seed failed: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
