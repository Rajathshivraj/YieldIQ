import React from 'react';
import { useQuery } from 'react-query';
import {
  Box, Typography, Paper
} from '@mui/material';
import { DataGrid, GridColDef, GridRenderCellParams } from '@mui/x-data-grid';
import { analyticsApi } from '../api';
import { formatCurrency } from '../utils/formatters';

const ProductAnalyticsDashboard: React.FC = () => {
  const { data, isLoading } = useQuery('productPerformance', () => analyticsApi.productPerformance());

  const columns: GridColDef[] = [
    { field: 'product_name', headerName: 'Product Name', flex: 1, minWidth: 250 },
    { field: 'category', headerName: 'Category', width: 180 },
    { 
      field: 'total_invested', 
      headerName: 'Total Invested', 
      width: 160,
      valueFormatter: (value: number) => formatCurrency(value)
    },
    { 
      field: 'revenue', 
      headerName: 'Platform Revenue', 
      width: 160,
      renderCell: (params: GridRenderCellParams) => (
        <Typography sx={{ color: '#06A77D', fontWeight: 700, fontSize: '0.875rem' }}>
          {formatCurrency(params.value)}
        </Typography>
      )
    },
    { field: 'transaction_count', headerName: 'Transactions', width: 120 },
    { field: 'investor_count', headerName: 'Unique Investors', width: 140 },
    { 
      field: 'expected_return', 
      headerName: 'Exp %', 
      width: 100,
      valueFormatter: (value: number) => `${value}%`
    },
    { 
      field: 'avg_actual_return', 
      headerName: 'Act %', 
      width: 100,
      valueFormatter: (value: number | null) => value ? `${value.toFixed(2)}%` : '-'
    },
  ];

  return (
    <Box sx={{ p: { xs: 2, md: 4 } }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" sx={{ fontWeight: 800 }}>Product Analytics</Typography>
        <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.4)' }}>Analyze performance and engagement across product lines</Typography>
      </Box>

      <Paper sx={{ height: 600, bgcolor: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.08)' }}>
        <DataGrid
          rows={data?.data || []}
          loading={isLoading}
          columns={columns}
          getRowId={(row) => row.product_id}
          disableRowSelectionOnClick
          sx={{
            border: 'none',
            color: '#fff',
            '& .MuiDataGrid-cell': { borderBottom: '1px solid rgba(255,255,255,0.05)' },
            '& .MuiDataGrid-columnHeaders': { bgcolor: 'rgba(255,255,255,0.02)', borderBottom: '1px solid rgba(255,255,255,0.1)' },
            '& .MuiDataGrid-footerContainer': { borderTop: '1px solid rgba(255,255,255,0.1)' },
          }}
        />
      </Paper>
    </Box>
  );
};

export default ProductAnalyticsDashboard;
