import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_URL,
  timeout: 30000,
});

// Request interceptor — attach JWT
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('yieldiq_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor — handle 401
api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('yieldiq_token');
      localStorage.removeItem('yieldiq_user');
      window.location.href = '/login';
    }
    return Promise.reject(err);
  }
);

export default api;

// ── Auth ───────────────────────────────────────────────────────────────────────
export const authApi = {
  login: (email: string, password: string) =>
    api.post('/auth/login', { email, password }),
  me: () => api.get('/auth/me'),
};

// ── Investors ──────────────────────────────────────────────────────────────────
export const investorsApi = {
  list: (params?: any) => api.get('/investors', { params }),
  get: (id: string) => api.get(`/investors/${id}`),
  create: (data: any) => api.post('/investors', data),
  update: (id: string, data: any) => api.put(`/investors/${id}`, data),
  delete: (id: string) => api.delete(`/investors/${id}`),
  portfolio: (id: string) => api.get(`/investors/${id}/portfolio`),
};

// ── Products ───────────────────────────────────────────────────────────────────
export const productsApi = {
  list: (params?: any) => api.get('/products', { params }),
  get: (id: string) => api.get(`/products/${id}`),
  create: (data: any) => api.post('/products', data),
  update: (id: string, data: any) => api.put(`/products/${id}`, data),
  delete: (id: string) => api.delete(`/products/${id}`),
};

// ── Transactions ───────────────────────────────────────────────────────────────
export const transactionsApi = {
  list: (params?: any) => api.get('/transactions', { params }),
  get: (id: string) => api.get(`/transactions/${id}`),
  create: (data: any) => api.post('/transactions', data),
  update: (id: string, data: any) => api.put(`/transactions/${id}`, data),
};

// ── Analytics ──────────────────────────────────────────────────────────────────
export const analyticsApi = {
  executive: () => api.get('/analytics/dashboard/executive'),
  revenue: (months = 12) => api.get('/analytics/revenue', { params: { months } }),
  portfolio: () => api.get('/analytics/portfolio'),
  investors: () => api.get('/analytics/investors'),
  productPerformance: () => api.get('/analytics/products/performance'),
  cohorts: () => api.get('/analytics/cohorts'),
  retention: () => api.get('/analytics/retention'),
};

// ── Reports ────────────────────────────────────────────────────────────────────
export const reportsApi = {
  revenueCsv: () => `${API_URL}/reports/revenue/csv`,
  revenueExcel: () => `${API_URL}/reports/revenue/excel`,
  revenuePdf: () => `${API_URL}/reports/revenue/pdf`,
  investorsCsv: () => `${API_URL}/reports/investors/csv`,
  investorsExcel: () => `${API_URL}/reports/investors/excel`,
  transactionsCsv: () => `${API_URL}/reports/transactions/csv`,
  portfolioPdf: () => `${API_URL}/reports/portfolio/pdf`,
};
