import React, { useEffect, useState } from 'react';
import {
  Box, Grid, Typography, Skeleton,
} from '@mui/material';
import PeopleIcon from '@mui/icons-material/People';
import AccountBalanceWalletIcon from '@mui/icons-material/AccountBalanceWallet';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import RepeatIcon from '@mui/icons-material/Repeat';
import PersonOffIcon from '@mui/icons-material/PersonOff';
import ReceiptIcon from '@mui/icons-material/Receipt';
import PersonAddIcon from '@mui/icons-material/PersonAdd';
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, PieChart, Pie, Cell,
} from 'recharts';
import KPICard from '../components/KPICard';
import { analyticsApi } from '../api';
import { ExecutiveDashboard, MonthlyRevenue } from '../types';
import { formatCurrency, formatNumber } from '../utils/formatters';

const COLORS = ['#4361EE', '#7209B7', '#F72585', '#3A0CA3', '#FFB703', '#06A77D'];

const ExecutiveDashboardPage: React.FC = () => {
  const [kpis, setKpis] = useState<ExecutiveDashboard | null>(null);
  const [revenue, setRevenue] = useState<MonthlyRevenue[]>([]);
  const [allocation, setAllocation] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const [kpiRes, revRes, portRes] = await Promise.all([
          analyticsApi.executive(),
          analyticsApi.revenue(12),
          analyticsApi.portfolio(),
        ]);
        setKpis(kpiRes.data);
        setRevenue(revRes.data.monthly_revenue || []);
        setAllocation(portRes.data.allocation || []);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const kpiCards = kpis ? [
    { title: 'Total Investors', value: formatNumber(kpis.total_investors), change: 5.2, subtitle: 'all-time', icon: <PeopleIcon fontSize="small" />, color: '#4361EE' },
    { title: 'Active Investors', value: formatNumber(kpis.active_investors), change: 3.1, subtitle: 'currently active', icon: <PeopleIcon fontSize="small" />, color: '#06A77D' },
    { title: 'Assets Under Mgmt', value: formatCurrency(kpis.aum, true), change: kpis.aum_growth_pct, subtitle: 'total AUM', icon: <AccountBalanceWalletIcon fontSize="small" />, color: '#7209B7' },
    { title: 'Total Revenue', value: formatCurrency(kpis.total_revenue, true), change: kpis.revenue_growth_pct, subtitle: 'net revenue', icon: <TrendingUpIcon fontSize="small" />, color: '#FFB703' },
    { title: 'Retention Rate', value: `${kpis.retention_rate.toFixed(1)}%`, change: 2.3, subtitle: 'monthly', icon: <RepeatIcon fontSize="small" />, color: '#06A77D' },
    { title: 'Churn Rate', value: `${kpis.churn_rate.toFixed(1)}%`, change: -2.3, subtitle: 'monthly', icon: <PersonOffIcon fontSize="small" />, color: '#F72585' },
    { title: 'Total Transactions', value: formatNumber(kpis.total_transactions), change: 7.8, subtitle: 'all-time', icon: <ReceiptIcon fontSize="small" />, color: '#3A0CA3' },
    { title: 'New This Month', value: formatNumber(kpis.new_investors_this_month), change: 12.1, subtitle: 'new investors', icon: <PersonAddIcon fontSize="small" />, color: '#4361EE' },
  ] : [];

  return (
    <Box sx={{ p: { xs: 2, md: 4 }, color: '#fff' }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" sx={{ fontWeight: 800, mb: 0.5 }}>Executive Dashboard</Typography>
        <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.4)' }}>Real-time platform overview</Typography>
      </Box>

      <Grid container spacing={2.5} sx={{ mb: 4 }}>
        {loading
          ? Array.from({ length: 8 }).map((_, i) => (
              <Grid size={{ xs: 12, sm: 6, md: 3 }} key={i}><KPICard title="" value="" icon={<></>} loading /></Grid>
            ))
          : kpiCards.map((card) => (
              <Grid size={{ xs: 12, sm: 6, md: 3 }} key={card.title}><KPICard {...card} /></Grid>
            ))}
      </Grid>

      <Grid container spacing={2.5}>
        <Grid size={{ xs: 12, lg: 8 }}>
          <Box sx={{ bgcolor: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: 3, p: 3, height: 340 }}>
            <Typography variant="h6" sx={{ mb: 3, fontWeight: 700 }}>Monthly Revenue Trend</Typography>
            {loading ? <Skeleton variant="rectangular" height={260} sx={{ bgcolor: 'rgba(255,255,255,0.05)', borderRadius: 2 }} /> : (
              <ResponsiveContainer width="100%" height={260}>
                <AreaChart data={revenue}>
                  <defs>
                    <linearGradient id="revGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#4361EE" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#4361EE" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                  <XAxis dataKey="month" tick={{ fill: 'rgba(255,255,255,0.4)', fontSize: 11 }} axisLine={false} tickLine={false} />
                  <YAxis tick={{ fill: 'rgba(255,255,255,0.4)', fontSize: 11 }} axisLine={false} tickLine={false} tickFormatter={(v) => `₹${(v / 1000).toFixed(0)}K`} />
                  <Tooltip contentStyle={{ background: '#1a1f3a', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 8, color: '#fff' }} formatter={(v: any) => [`₹${Number(v).toLocaleString('en-IN')}`, '']} />
                  <Area type="monotone" dataKey="net_revenue" stroke="#4361EE" strokeWidth={2} fill="url(#revGrad)" name="Net Revenue" />
                  <Area type="monotone" dataKey="platform_fee" stroke="#7209B7" strokeWidth={2} fill="none" name="Platform Fee" strokeDasharray="4 4" />
                </AreaChart>
              </ResponsiveContainer>
            )}
          </Box>
        </Grid>

        <Grid size={{ xs: 12, lg: 4 }}>
          <Box sx={{ bgcolor: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: 3, p: 3, height: 340 }}>
            <Typography variant="h6" sx={{ mb: 2, fontWeight: 700 }}>Portfolio Allocation</Typography>
            {loading ? <Skeleton variant="circular" width={180} height={180} sx={{ mx: 'auto', bgcolor: 'rgba(255,255,255,0.05)' }} /> : (
              <>
                <ResponsiveContainer width="100%" height={180}>
                  <PieChart>
                    <Pie data={allocation} cx="50%" cy="50%" innerRadius={50} outerRadius={80} dataKey="total_invested" paddingAngle={3}>
                      {allocation.map((entry, i) => <Cell key={entry.category} fill={COLORS[i % COLORS.length]} />)}
                    </Pie>
                    <Tooltip contentStyle={{ background: '#1a1f3a', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 8, color: '#fff' }} formatter={(v: any) => [formatCurrency(v, true), '']} />
                  </PieChart>
                </ResponsiveContainer>
                <Box sx={{ mt: 1 }}>
                  {allocation.slice(0, 4).map((a, i) => (
                    <Box key={a.category} sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Box sx={{ width: 8, height: 8, borderRadius: '50%', bgcolor: COLORS[i % COLORS.length] }} />
                        <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.6)' }}>{a.category}</Typography>
                      </Box>
                      <Typography variant="caption" sx={{ color: '#fff', fontWeight: 600 }}>{a.percentage?.toFixed(1)}%</Typography>
                    </Box>
                  ))}
                </Box>
              </>
            )}
          </Box>
        </Grid>
      </Grid>
    </Box>
  );
};

export default ExecutiveDashboardPage;
