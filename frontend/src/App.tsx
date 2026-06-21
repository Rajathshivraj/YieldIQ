import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { QueryClient, QueryClientProvider } from 'react-query';

import { AuthProvider, useAuth } from './store/AuthContext';
import Layout from './components/Layout';
import LoginPage from './pages/LoginPage';
import ExecutiveDashboardPage from './pages/ExecutiveDashboard';
import InvestorsPage from './pages/InvestorsPage';
import TransactionsPage from './pages/TransactionsPage';
import ProductsPage from './pages/ProductsPage';
import RevenueDashboard from './pages/RevenueDashboard';
import PortfolioDashboard from './pages/PortfolioDashboard';
import CohortDashboard from './pages/CohortDashboard';
import ProductAnalyticsDashboard from './pages/ProductAnalyticsDashboard';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#4361EE' },
    secondary: { main: '#7209B7' },
    background: { default: '#0A0E1A', paper: '#0D1117' },
    text: { primary: '#ffffff', secondary: 'rgba(255,255,255,0.7)' },
  },
  typography: { fontFamily: 'Inter, sans-serif' },
  shape: { borderRadius: 8 },
  components: {
    MuiButton: { styleOverrides: { root: { textTransform: 'none', fontWeight: 600 } } },
    MuiPaper: { styleOverrides: { root: { backgroundImage: 'none' } } },
  },
});

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { refetchOnWindowFocus: false, retry: 1 },
  },
});

const ProtectedRoute = ({ children }: { children: React.ReactElement }) => {
  const { isAuthenticated, loading } = useAuth();
  if (loading) return <div>Loading...</div>;
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return <Layout>{children}</Layout>;
};

function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/" element={<ProtectedRoute><ExecutiveDashboardPage /></ProtectedRoute>} />
      <Route path="/investors" element={<ProtectedRoute><InvestorsPage /></ProtectedRoute>} />
      <Route path="/transactions" element={<ProtectedRoute><TransactionsPage /></ProtectedRoute>} />
      <Route path="/products" element={<ProtectedRoute><ProductsPage /></ProtectedRoute>} />
      <Route path="/revenue" element={<ProtectedRoute><RevenueDashboard /></ProtectedRoute>} />
      <Route path="/portfolio" element={<ProtectedRoute><PortfolioDashboard /></ProtectedRoute>} />
      <Route path="/cohorts" element={<ProtectedRoute><CohortDashboard /></ProtectedRoute>} />
      <Route path="/product-analytics" element={<ProtectedRoute><ProductAnalyticsDashboard /></ProtectedRoute>} />
      
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <AuthProvider>
          <Router>
            <AppRoutes />
          </Router>
        </AuthProvider>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App;
