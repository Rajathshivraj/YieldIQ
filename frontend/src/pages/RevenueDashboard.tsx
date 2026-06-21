import React from 'react';
import { useQuery } from 'react-query';
import {
  Box, Typography, Grid, Paper, Skeleton, Button
} from '@mui/material';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend
} from 'recharts';
import { analyticsApi, reportsApi } from '../api';
import { formatCurrency } from '../utils/formatters';

const RevenueDashboard: React.FC = () => {
  const { data, isLoading } = useQuery('revenue', () => analyticsApi.revenue(24));

  const handleDownloadExcel = () => {
    window.open(reportsApi.revenueExcel(), '_blank');
  };

  const handleDownloadPdf = () => {
    window.open(reportsApi.revenuePdf(), '_blank');
  };

  const revenueData = data?.data?.monthly_revenue || [];
  const topProducts = data?.data?.top_products || [];

  return (
    <Box sx={{ p: { xs: 2, md: 4 } }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Box>
          <Typography variant="h4" sx={{ fontWeight: 800 }}>Revenue Analytics</Typography>
          <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.4)' }}>Deep dive into platform earnings</Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button variant="outlined" onClick={handleDownloadExcel} sx={{ color: '#fff', borderColor: 'rgba(255,255,255,0.2)' }}>
            Excel
          </Button>
          <Button variant="outlined" onClick={handleDownloadPdf} sx={{ color: '#fff', borderColor: 'rgba(255,255,255,0.2)' }}>
            PDF
          </Button>
        </Box>
      </Box>

      <Grid container spacing={3}>
        <Grid size={12}>
          <Paper sx={{ p: 3, bgcolor: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: 3 }}>
            <Typography variant="h6" sx={{ mb: 3, fontWeight: 700 }}>Revenue Breakdown (Last 24 Months)</Typography>
            {isLoading ? <Skeleton variant="rectangular" height={400} sx={{ bgcolor: 'rgba(255,255,255,0.05)' }} /> : (
              <Box sx={{ height: 400 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={revenueData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                    <XAxis dataKey="month" tick={{ fill: 'rgba(255,255,255,0.4)', fontSize: 12 }} axisLine={false} tickLine={false} />
                    <YAxis tick={{ fill: 'rgba(255,255,255,0.4)', fontSize: 12 }} axisLine={false} tickLine={false} tickFormatter={(v) => `₹${(v/1000).toFixed(0)}K`} />
                    <Tooltip 
                      contentStyle={{ background: '#1a1f3a', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 8, color: '#fff' }}
                      formatter={(v: any) => [formatCurrency(v), '']}
                    />
                    <Legend wrapperStyle={{ paddingTop: 20 }} />
                    <Bar dataKey="platform_fee" name="Platform Fee" stackId="a" fill="#4361EE" radius={[0, 0, 4, 4]} />
                    <Bar dataKey="brokerage_fee" name="Brokerage Fee" stackId="a" fill="#7209B7" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </Box>
            )}
          </Paper>
        </Grid>

        <Grid size={12}>
          <Paper sx={{ p: 3, bgcolor: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: 3 }}>
            <Typography variant="h6" sx={{ mb: 3, fontWeight: 700 }}>Top Revenue Generating Products</Typography>
            {isLoading ? <Skeleton variant="rectangular" height={300} sx={{ bgcolor: 'rgba(255,255,255,0.05)' }} /> : (
              <Box sx={{ overflowX: 'auto' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                  <thead>
                    <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
                      <th style={{ padding: '12px 8px', color: 'rgba(255,255,255,0.5)', fontWeight: 500 }}>Product Name</th>
                      <th style={{ padding: '12px 8px', color: 'rgba(255,255,255,0.5)', fontWeight: 500 }}>Category</th>
                      <th style={{ padding: '12px 8px', color: 'rgba(255,255,255,0.5)', fontWeight: 500 }}>Transactions</th>
                      <th style={{ padding: '12px 8px', color: 'rgba(255,255,255,0.5)', fontWeight: 500, textAlign: 'right' }}>Total Invested</th>
                      <th style={{ padding: '12px 8px', color: 'rgba(255,255,255,0.5)', fontWeight: 500, textAlign: 'right' }}>Net Revenue</th>
                    </tr>
                  </thead>
                  <tbody>
                    {topProducts.map((p: any, i: number) => (
                      <tr key={i} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                        <td style={{ padding: '16px 8px', fontWeight: 600 }}>{p.product_name}</td>
                        <td style={{ padding: '16px 8px', color: 'rgba(255,255,255,0.7)' }}>{p.category}</td>
                        <td style={{ padding: '16px 8px' }}>{p.transaction_count}</td>
                        <td style={{ padding: '16px 8px', textAlign: 'right' }}>{formatCurrency(p.total_invested)}</td>
                        <td style={{ padding: '16px 8px', textAlign: 'right', color: '#06A77D', fontWeight: 700 }}>{formatCurrency(p.net_revenue)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </Box>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default RevenueDashboard;
