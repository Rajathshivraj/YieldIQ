# YieldIQ – Fixed Income Analytics & Investor Intelligence Platform

![YieldIQ Banner](https://img.shields.io/badge/FinTech-Analytics-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![React](https://img.shields.io/badge/React-Frontend-61DAFB)
![Python](https://img.shields.io/badge/Python-Data%20Processing-yellow)

## Overview

YieldIQ is a full-stack fintech analytics and investor intelligence platform designed to help investment firms monitor investor behavior, portfolio performance, revenue growth, product performance, and retention trends.

The platform processes and analyzes over **100,000+ investment transactions** across multiple fixed-income and alternative investment products, enabling data-driven business decisions through real-time dashboards and advanced analytics.

---

## Key Features

### Investor Intelligence

* Investor onboarding and management
* Investor segmentation (Platinum, Gold, Silver, New Investors)
* Investor growth tracking
* Retention and churn analysis
* Investor portfolio summaries

### Portfolio Analytics

* Portfolio performance monitoring
* Asset allocation analysis
* Product distribution tracking
* ROI and investment trend analysis
* Assets Under Management (AUM) insights

### Revenue Analytics

* Monthly and quarterly revenue tracking
* Product-wise revenue analysis
* Growth trend monitoring
* Business KPI reporting

### Product Intelligence

* Product performance evaluation
* Most popular investment products
* Revenue contribution analysis
* Investment distribution analysis

### Cohort & Retention Analytics

* Cohort analysis by signup month
* Retention tracking
* Investor lifecycle monitoring
* Churn prediction support

### Reporting & Automation

* Automated analytics pipelines
* Scheduled KPI generation
* Downloadable reports (CSV, Excel, PDF)
* Executive business reporting

---

## Supported Investment Products

* Bonds
* Fixed Deposits (FDs)
* Invoice Discounting
* Asset Leasing
* Digital Gold
* Alternative Investment Products

---

## System Architecture

```text
                    ┌─────────────────────┐
                    │      Frontend       │
                    │   React Dashboard   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      FastAPI        │
                    │    REST APIs        │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
      Analytics Engine    Business Logic    Auth Layer
              │                │                │
              └────────────────┼────────────────┘
                               ▼
                    ┌─────────────────────┐
                    │    PostgreSQL DB    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Pandas + NumPy ETL  │
                    └─────────────────────┘
```

---

## Tech Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* JWT Authentication

### Frontend

* React
* TypeScript
* Material UI
* Axios

### Analytics

* Pandas
* NumPy
* Power BI Integration

### DevOps

* Docker
* Docker Compose
* GitHub Actions (Optional)

---

## Database Design

### Core Entities

#### Investors

```sql
investors
---------
investor_id
full_name
email
phone
risk_profile
registration_date
```

#### Products

```sql
products
--------
product_id
product_name
category
risk_level
expected_return
```

#### Transactions

```sql
transactions
------------
transaction_id
investor_id
product_id
investment_amount
investment_date
maturity_date
actual_return
```

#### Revenue

```sql
revenue
-------
revenue_id
transaction_id
platform_fee
brokerage_fee
net_revenue
```

---

## Scalability Considerations

The platform is designed to efficiently handle:

* 100,000+ investment transactions
* Large investor datasets
* High-volume analytical queries
* Aggregation-heavy reporting workloads

Implemented optimizations include:

* Database indexing
* Query optimization
* Pagination
* Server-side filtering
* Optimized joins
* Batch analytics processing

---

## API Modules

### Investor APIs

```http
GET    /api/investors
POST   /api/investors
PUT    /api/investors/{id}
DELETE /api/investors/{id}
```

### Product APIs

```http
GET    /api/products
POST   /api/products
```

### Transaction APIs

```http
GET    /api/transactions
POST   /api/transactions
```

### Analytics APIs

```http
GET /api/analytics/revenue
GET /api/analytics/portfolio
GET /api/analytics/retention
GET /api/analytics/cohorts
```

---

## Sample Analytics

### Investor Segmentation

| Segment      | Criteria    |
| ------------ | ----------- |
| Platinum     | > ₹10 Lakhs |
| Gold         | ₹5–10 Lakhs |
| Silver       | ₹1–5 Lakhs  |
| New Investor | < ₹1 Lakh   |

---

### Business KPIs

* Total Investors
* Active Investors
* Monthly Revenue
* AUM
* Retention Rate
* Churn Rate
* Portfolio Growth
* Product Performance

---

## Security Features

* JWT Authentication
* Password Hashing
* Role-Based Access Control (RBAC)
* Admin Access
* Analyst Access
* Read-Only Access
* Input Validation
* Secure API Endpoints

---

## Performance Metrics

* Processes 100,000+ investment transactions
* Optimized PostgreSQL indexing strategy
* FastAPI asynchronous endpoints
* Automated reporting pipelines
* Real-time dashboard support

---

## Future Enhancements

* Redis Caching
* Background Job Processing (Celery)
* Investor Risk Prediction
* AI-Based Portfolio Recommendations
* Fraud Detection Engine
* Real-Time Streaming Analytics
* Multi-Tenant Architecture
* Kubernetes Deployment

---

## Project Highlights

* Built a full-stack fintech analytics platform
* Processed and analyzed 100,000+ investment transactions
* Developed scalable REST APIs using FastAPI
* Designed normalized PostgreSQL database schemas
* Implemented investor segmentation and retention analytics
* Built executive dashboards for business intelligence
* Automated reporting workflows using Python and Pandas
* Delivered scalable analytics architecture suitable for enterprise fintech environments

---

## Author

**Rajath U**

B.Tech Computer Science (AI & ML)
Dayananda Sagar University

GitHub: https://github.com/Rajathshivraj

LinkedIn: Add your LinkedIn profile URL

Portfolio: Add your portfolio URL

---

⭐ If you found this project useful, consider starring the repository.
