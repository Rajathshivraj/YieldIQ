"""
API v1 router — aggregates all route modules.
"""
from fastapi import APIRouter

from app.api.v1.routes import auth, investors, products, transactions, analytics, reports

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(investors.router)
api_router.include_router(products.router)
api_router.include_router(transactions.router)
api_router.include_router(analytics.router)
api_router.include_router(reports.router)
