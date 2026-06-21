import React from 'react';
import { useQuery } from 'react-query';
import {
  Box, Typography, Paper, Skeleton
} from '@mui/material';
import { analyticsApi } from '../api';

const CohortDashboard: React.FC = () => {
  const { data, isLoading } = useQuery('cohorts', () => analyticsApi.cohorts());

  const cohorts = data?.data || [];
  const maxRetentionMonths = cohorts.length > 0 ? Math.max(...cohorts.map((c: any) => Object.keys(c.retention_by_month).length)) : 12;
  const monthLabels = Array.from({ length: maxRetentionMonths }, (_, i) => i + 1);

  const getColor = (pct: number) => {
    if (pct >= 80) return 'rgba(6,167,125,0.8)';
    if (pct >= 60) return 'rgba(6,167,125,0.5)';
    if (pct >= 40) return 'rgba(255,183,3,0.6)';
    if (pct >= 20) return 'rgba(247,37,133,0.5)';
    return 'rgba(247,37,133,0.8)';
  };

  return (
    <Box sx={{ p: { xs: 2, md: 4 } }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" sx={{ fontWeight: 800 }}>Cohort Analysis</Typography>
        <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.4)' }}>Investor retention tracking by signup month</Typography>
      </Box>

      <Paper sx={{ p: 3, bgcolor: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: 3, overflowX: 'auto' }}>
        {isLoading ? <Skeleton variant="rectangular" height={500} sx={{ bgcolor: 'rgba(255,255,255,0.05)' }} /> : (
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'center', fontSize: '0.875rem' }}>
            <thead>
              <tr>
                <th style={{ padding: 12, textAlign: 'left', width: 120 }}>Cohort</th>
                <th style={{ padding: 12, width: 80 }}>Size</th>
                {monthLabels.map(m => (
                  <th key={m} style={{ padding: 12 }}>M{m}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {cohorts.map((cohort: any) => (
                <tr key={cohort.cohort_month}>
                  <td style={{ padding: 12, textAlign: 'left', fontWeight: 600 }}>{cohort.cohort_month}</td>
                  <td style={{ padding: 12 }}>{cohort.cohort_size}</td>
                  {monthLabels.map(m => {
                    const val = cohort.retention_by_month[m];
                    return (
                      <td key={m} style={{ padding: 2 }}>
                        {val !== undefined ? (
                          <Box sx={{ 
                            bgcolor: getColor(val), 
                            color: '#fff', 
                            py: 1, 
                            borderRadius: 1,
                            fontWeight: 600,
                            minWidth: 50
                          }}>
                            {val}%
                          </Box>
                        ) : (
                          <Box sx={{ py: 1, color: 'rgba(255,255,255,0.2)' }}>-</Box>
                        )}
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </Paper>
    </Box>
  );
};

export default CohortDashboard;
