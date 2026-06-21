-- YieldIQ PostgreSQL initialization
-- Performance indexes are created by SQLAlchemy, but we set DB-level settings here

-- Enable pg_stat_statements for query monitoring
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Set work_mem for better sort/aggregate performance
ALTER DATABASE yieldiq SET work_mem = '64MB';
ALTER DATABASE yieldiq SET random_page_cost = 1.1;
