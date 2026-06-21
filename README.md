# YieldIQ

**YieldIQ** is a production-grade full-stack fintech analytics platform designed to process and analyze large-scale investment transactions (100,000+) across multiple fixed-income and alternative investment products.

## Technology Stack

- **Backend:** Python, FastAPI, SQLAlchemy, PostgreSQL
- **Frontend:** React, TypeScript, Material UI, Recharts, React Query
- **Data Processing:** Pandas, NumPy (ETL jobs)
- **Deployment:** Docker, Docker Compose

## Features

- **Executive Dashboard:** Real-time KPI metrics, AUM growth, and monthly revenue trends.
- **Investor Management:** Full CRUD operations, segmentation (Platinum, Gold, Silver), and portfolio views.
- **Transaction Engine:** Handling 100k+ records with server-side pagination, sorting, and filtering.
- **Product Management:** Manage various asset classes (Bonds, FDs, Digital Gold, Invoice Discounting).
- **Analytics Dashboards:** Portfolio Allocation, Revenue Analytics, Cohort Retention, and Product Performance.
- **Reports Generation:** Downloadable CSV, Excel, and PDF reports.
- **Role-Based Access Control:** Secure JWT authentication (Admin, Analyst, Viewer roles).

## Folder Structure

```
YieldIQ/
├── backend/
│   ├── app/                 # FastAPI Application
│   │   ├── api/v1/routes/   # REST API Endpoints
│   │   ├── core/            # Config, Security, Logging
│   │   ├── db/              # DB Session & Init
│   │   ├── models/          # SQLAlchemy ORM Models
│   │   ├── repositories/    # Data Access Layer
│   │   ├── schemas/         # Pydantic Validation Models
│   │   └── services/        # Business Logic Layer
│   ├── etl/                 # Seed Data & Data Processing Scripts
│   ├── sql/                 # Database initialization scripts
│   ├── Dockerfile           # Backend Docker configuration
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/                 # React Application
│   │   ├── api/             # Axios API Client
│   │   ├── components/      # Reusable UI Components
│   │   ├── pages/           # Dashboard Pages
│   │   ├── store/           # Global State (AuthContext)
│   │   ├── types/           # TypeScript Interfaces
│   │   └── utils/           # Helper Functions
│   ├── Dockerfile           # Frontend Docker configuration
│   └── package.json         # Node dependencies
├── docker-compose.yml       # Production/Local Orchestration
└── .env.example             # Environment template
```

## Setup & Running Locally

### Prerequisites
- Docker and Docker Compose installed.
- (Optional) Python 3.11+ and Node.js v18+ for local development without Docker.

### Running with Docker Compose (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd YieldIQ
   ```

2. **Start the services:**
   This will spin up PostgreSQL, the FastAPI Backend, and the React Frontend.
   ```bash
   docker-compose up -d
   ```

3. **Generate Seed Data (Run once):**
   This script creates 20k investors, 15 products, and 100k+ transactions.
   ```bash
   docker-compose run --rm seed
   ```

4. **Access the application:**
   - **Frontend UI:** [http://localhost:3000](http://localhost:3000)
   - **Backend API Docs:** [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)

### Default Test Accounts

| Role | Email | Password |
|---|---|---|
| Admin | `admin@yieldiq.com` | `Admin@123` |
| Analyst | `analyst@yieldiq.com` | `Analyst@123` |
| Viewer | `viewer@yieldiq.com` | `Viewer@123` |

## Advanced: ETL Pipeline

The platform includes a Pandas-based ETL pipeline for generating static offline KPI reports suitable for tools like Power BI.
To run the ETL pipeline locally (assuming backend env is set up):

```bash
cd backend
python -m etl.etl_pipeline
```
This generates CSV files in `backend/etl/exports/`.

---
*Designed & Built for SDE-1 Fintech Requirements.*
