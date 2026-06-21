"""
Reports routes — downloadable CSV, Excel, PDF.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.session import get_db
from app.repositories.analytics_repo import AnalyticsRepository
from app.repositories.investor_repo import InvestorRepository
from app.repositories.transaction_repo import TransactionRepository
from app.services.report_service import ReportService
from app.core.security import get_current_user

router = APIRouter(prefix="/reports", tags=["Reports"])


def get_report_service() -> ReportService:
    return ReportService()


@router.get("/revenue/csv")
def revenue_csv(db: Session = Depends(get_db), _=Depends(get_current_user), svc: ReportService = Depends(get_report_service)):
    data = AnalyticsRepository(db).get_monthly_revenue(60)
    return svc.generate_csv(data, f"revenue_report_{datetime.now().strftime('%Y%m%d')}.csv")


@router.get("/revenue/excel")
def revenue_excel(db: Session = Depends(get_db), _=Depends(get_current_user), svc: ReportService = Depends(get_report_service)):
    data = AnalyticsRepository(db).get_monthly_revenue(60)
    return svc.generate_excel(data, "Revenue", f"revenue_report_{datetime.now().strftime('%Y%m%d')}.xlsx")


@router.get("/revenue/pdf")
def revenue_pdf(db: Session = Depends(get_db), _=Depends(get_current_user), svc: ReportService = Depends(get_report_service)):
    data = AnalyticsRepository(db).get_monthly_revenue(60)
    return svc.generate_pdf("YieldIQ Revenue Report", data, f"revenue_report_{datetime.now().strftime('%Y%m%d')}.pdf")


@router.get("/investors/csv")
def investors_csv(db: Session = Depends(get_db), _=Depends(get_current_user), svc: ReportService = Depends(get_report_service)):
    items, _ = InvestorRepository(db).list(page=1, page_size=50000)
    data = [
        {
            "investor_id": str(i.investor_id), "full_name": i.full_name, "email": i.email,
            "city": i.city, "segment": i.investor_segment, "status": i.status,
            "risk_profile": i.risk_profile, "registration_date": str(i.registration_date),
        }
        for i in items
    ]
    return svc.generate_csv(data, f"investors_{datetime.now().strftime('%Y%m%d')}.csv")


@router.get("/investors/excel")
def investors_excel(db: Session = Depends(get_db), _=Depends(get_current_user), svc: ReportService = Depends(get_report_service)):
    items, _ = InvestorRepository(db).list(page=1, page_size=50000)
    data = [
        {
            "investor_id": str(i.investor_id), "full_name": i.full_name, "email": i.email,
            "city": i.city, "segment": i.investor_segment, "status": i.status,
            "risk_profile": i.risk_profile, "registration_date": str(i.registration_date),
        }
        for i in items
    ]
    return svc.generate_excel(data, "Investors", f"investors_{datetime.now().strftime('%Y%m%d')}.xlsx")


@router.get("/transactions/csv")
def transactions_csv(db: Session = Depends(get_db), _=Depends(get_current_user), svc: ReportService = Depends(get_report_service)):
    items, _ = TransactionRepository(db).list(page=1, page_size=100000)
    data = [
        {
            "transaction_id": str(t.transaction_id),
            "investor_name": t.investor.full_name if t.investor else "",
            "product_name": t.product.product_name if t.product else "",
            "category": t.product.category if t.product else "",
            "amount": float(t.investment_amount),
            "investment_date": str(t.investment_date),
            "maturity_date": str(t.maturity_date),
            "status": t.transaction_status,
            "expected_return": float(t.expected_return),
        }
        for t in items
    ]
    return svc.generate_csv(data, f"transactions_{datetime.now().strftime('%Y%m%d')}.csv")


@router.get("/portfolio/pdf")
def portfolio_pdf(db: Session = Depends(get_db), _=Depends(get_current_user), svc: ReportService = Depends(get_report_service)):
    data = AnalyticsRepository(db).get_portfolio_allocation()
    return svc.generate_pdf("YieldIQ Portfolio Report", data, f"portfolio_{datetime.now().strftime('%Y%m%d')}.pdf")
