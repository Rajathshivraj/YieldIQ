import React from 'react';
import { useQuery } from 'react-query';
import {
  Box, Typography, Grid, Paper, Skeleton, Button
} from '@mui/material';
import {
  PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend
} from 'recharts';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import { analyticsApi, reportsApi } from '../api';
import { formatCurrency, CATEGORY_COLORS } from '../utils/formatters';

const PortfolioDashboard: React.FC = () => {
  const { data, isLoading } = useQuery('portfolio', () => analyticsApi.portfolio());

  const handleDownloadPdf = () => {
    window.open(reportsApi.portfolioPdf(), '_blank');
  };

  const allocation = data?.data?.allocation || [];

  return (
    <Box sx={{ p: { xs: 2, md: 4 } }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Box>
          <Typography variant="h4" sx={{ fontWeight: 800 }}>Portfolio Dashboard</Typography>
          <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.4)' }}>Analyze total platform asset distribution</Typography>
        </Box>
        <Button 
          variant="outlined" 
          startIcon={<FileDownloadIcon />}
          onClick={handleDownloadPdf}
          sx={{ color: '#fff', borderColor: 'rgba(255,255,255,0.2)' }}
        >
          Export PDF
        </Button>
      </Box>

      <Grid container spacing={3}>
        <Grid size={{ xs: 12, md: 6 }}>
          <Paper sx={{ p: 3, bgcolor: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: 3, height: 450 }}>
            <Typography variant="h6" sx={{ mb: 3, fontWeight: 700 }}>Asset Class Allocation</Typography>
            {isLoading ? <Skeleton variant="circular" width={300} height={300} sx={{ mx: 'auto', bgcolor: 'rgba(255,255,255,0.05)' }} /> : (
              <ResponsiveContainer width="100%" height={350}>
                <PieChart>
                  <Pie 
                    data={allocation} cx="50%" cy="50%" innerRadius={80} outerRadius={130} 
                    dataKey="total_invested" paddingAngle={2}
                  >
                    {allocation.map((entry: any) => (
                      <Cell key={entry.category} fill={CATEGORY_COLORS[entry.category] || '#4361EE'} />
                    ))}
                  </Pie>
                  <Tooltip 
                    contentStyle={{ background: '#1a1f3a', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 8, color: '#fff' }}
                    formatter={(v: any) => [formatCurrency(v, true), '']}
                  />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            )}
          </Paper>
        </Grid>

        <Grid size={{ xs: 12, md: 6 }}>
          <Paper sx={{ p: 3, bgcolor: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: 3, height: 450, overflowY: 'auto' }}>
            <Typography variant="h6" sx={{ mb: 3, fontWeight: 700 }}>Allocation Details</Typography>
            {isLoading ? <Skeleton variant="rectangular" height={300} sx={{ bgcolor: 'rgba(255,255,255,0.05)' }} /> : (
              <Box>
                {allocation.map((item: any) => (
                  <Box key={item.category} sx={{ mb: 3, p: 2, bgcolor: 'rgba(255,255,255,0.02)', borderRadius: 2 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Box sx={{ width: 12, height: 12, borderRadius: '50%', bgcolor: CATEGORY_COLORS[item.category] || '#4361EE' }} />
                        <Typography sx={{ fontWeight: 600 }}>{item.category}</Typography>
                      </Box>
                      <Typography sx={{ fontWeight: 700 }}>{item.percentage.toFixed(1)}%</Typography>
                    </Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', color: 'rgba(255,255,255,0.5)', fontSize: '0.875rem' }}>
                      <Typography variant="body2">AUM: {formatCurrency(item.total_invested)}</Typography>
                      <Typography variant="body2">Txns: {item.transaction_count}</Typography>
                    </Box>
                  </Box>
                ))}
              </Box>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default PortfolioDashboard;
