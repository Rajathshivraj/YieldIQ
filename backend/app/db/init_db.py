"""
Database initialization: create tables and seed admin user.
"""
import logging
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.core.security import get_password_hash

logger = logging.getLogger(__name__)


def init_db() -> None:
    """Create all tables and seed initial admin user."""
    # Import all models so they register with Base metadata
    from app.models import investor, product, transaction, revenue, cohort, user  # noqa: F401

    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created.")

    db: Session = SessionLocal()
    try:
        _seed_admin_user(db)
    finally:
        db.close()


def _seed_admin_user(db: Session) -> None:
    from app.models.user import User

    existing = db.query(User).filter(User.email == "admin@yieldiq.com").first()
    if not existing:
        admin = User(
            email="admin@yieldiq.com",
            full_name="YieldIQ Admin",
            hashed_password=get_password_hash("Admin@123"),
            role="admin",
            is_active=True,
        )
        db.add(admin)

        analyst = User(
            email="analyst@yieldiq.com",
            full_name="YieldIQ Analyst",
            hashed_password=get_password_hash("Analyst@123"),
            role="analyst",
            is_active=True,
        )
        db.add(analyst)

        readonly = User(
            email="viewer@yieldiq.com",
            full_name="YieldIQ Viewer",
            hashed_password=get_password_hash("Viewer@123"),
            role="readonly",
            is_active=True,
        )
        db.add(readonly)

        db.commit()
        logger.info("Seeded default users: admin, analyst, viewer")
    else:
        logger.info("Admin user already exists, skipping seed.")
