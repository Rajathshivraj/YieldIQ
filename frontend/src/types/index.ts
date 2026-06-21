// TypeScript types for YieldIQ

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: 'admin' | 'analyst' | 'readonly';
  is_active: boolean;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
}

export interface Investor {
  investor_id: string;
  full_name: string;
  email: string;
  phone?: string;
  city?: string;
  registration_date: string;
  risk_profile: string;
  investor_segment: string;
  status: string;
  kyc_verified: string;
  pan_number?: string;
  created_at: string;
  updated_at: string;
}

export interface InvestorPortfolio {
  investor_id: string;
  full_name: string;
  total_invested: number;
  active_investments: number;
  matured_investments: number;
  total_transactions: number;
  portfolio_value: number;
  avg_return: number;
  investor_segment: string;
  risk_profile: string;
  top_product_category?: string;
}

export interface Product {
  product_id: string;
  product_name: string;
  category: string;
  expected_return: number;
  tenure_months: number;
  risk_level: string;
  min_investment: number;
  max_investment?: number;
  is_active: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface Transaction {
  transaction_id: string;
  investor_id: string;
  product_id: string;
  investment_amount: number;
  investment_date: string;
  maturity_date: string;
  expected_return: number;
  actual_return?: number;
  transaction_status: string;
  notes?: string;
  investor_name?: string;
  product_name?: string;
  product_category?: string;
  created_at: string;
  updated_at: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}

export interface ExecutiveDashboard {
  total_investors: number;
  active_investors: number;
  new_investors_this_month: number;
  aum: number;
  aum_growth_pct: number;
  total_revenue: number;
  revenue_growth_pct: number;
  retention_rate: number;
  churn_rate: number;
  total_transactions: number;
  active_transactions: number;
}

export interface MonthlyRevenue {
  month: string;
  platform_fee: number;
  brokerage_fee: number;
  net_revenue: number;
  transaction_count: number;
}

export interface ProductPerformance {
  product_id: string;
  product_name: string;
  category: string;
  expected_return: number;
  avg_actual_return?: number;
  total_invested: number;
  transaction_count: number;
  investor_count: number;
  revenue: number;
}

export interface PortfolioAllocation {
  category: string;
  total_invested: number;
  percentage: number;
  transaction_count: number;
}

export interface CohortRow {
  cohort_month: string;
  cohort_size: number;
  retention_by_month: Record<number, number>;
}

export interface RetentionStats {
  period: string;
  active_investors: number;
  churned_investors: number;
  retention_rate: number;
  churn_rate: number;
}
