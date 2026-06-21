"""
YieldIQ FastAPI Application Entry Point.
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.db.init_db import init_db
from app.api.v1.router import api_router

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting YieldIQ backend...")
    init_db()
    logger.info("YieldIQ backend ready.")
    yield
    logger.info("Shutting down YieldIQ backend.")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.APP_VERSION,
    description="""
## YieldIQ — Fixed Income Analytics & Investor Intelligence Platform

Production-grade fintech analytics API supporting 100,000+ investment transactions.

### Features
- **Investor Management** — Full CRUD with portfolio analytics
- **Product Management** — Fixed income products (Bonds, FD, Invoice Discounting, etc.)
- **Transaction Processing** — 100k+ records with pagination & advanced filtering
- **Analytics Dashboards** — Revenue, Portfolio, Cohort, Retention analytics
- **Reports** — Downloadable CSV, Excel, PDF
- **JWT Authentication** — Role-based access control (Admin/Analyst/ReadOnly)
    """,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan,
)

# ── Middleware ─────────────────────────────────────────────────────────────────
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes ─────────────────────────────────────────────────────────────────────
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Health"])
def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "operational",
        "docs": f"{settings.API_V1_STR}/docs",
    }


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy", "environment": settings.ENVIRONMENT}
