import React, { useState } from 'react';
import { useQuery } from 'react-query';
import {
  Box, Typography, Paper, TextField, InputAdornment, Chip, Button
} from '@mui/material';
import { DataGrid, GridColDef, GridRenderCellParams } from '@mui/x-data-grid';
import SearchIcon from '@mui/icons-material/Search';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import { transactionsApi, reportsApi } from '../api';
import { formatCurrency, formatDate, CATEGORY_COLORS } from '../utils/formatters';

const TransactionsPage: React.FC = () => {
  const [paginationModel, setPaginationModel] = useState({ page: 0, pageSize: 50 });
  const [search, setSearch] = useState('');
  
  const [debouncedSearch, setDebouncedSearch] = useState('');
  React.useEffect(() => {
    const timer = setTimeout(() => setDebouncedSearch(search), 500);
    return () => clearTimeout(timer);
  }, [search]);

  const { data, isLoading } = useQuery(
    ['transactions', paginationModel.page, paginationModel.pageSize, debouncedSearch],
    () => transactionsApi.list({ page: paginationModel.page + 1, page_size: paginationModel.pageSize, search: debouncedSearch }),
    { keepPreviousData: true }
  );

  const handleDownloadCsv = () => {
    window.open(reportsApi.transactionsCsv(), '_blank');
  };

  const columns: GridColDef[] = [
    { field: 'investor_name', headerName: 'Investor', flex: 1, minWidth: 150 },
    { field: 'product_name', headerName: 'Product', flex: 1, minWidth: 200 },
    { 
      field: 'product_category', 
      headerName: 'Category', 
      width: 160,
      renderCell: (params: GridRenderCellParams) => (
        <Chip 
          label={params.value} 
          size="small" 
          sx={{ 
            bgcolor: `${CATEGORY_COLORS[params.value as string] || '#4361EE'}22`, 
            color: CATEGORY_COLORS[params.value as string] || '#4361EE',
            fontWeight: 600,
            fontSize: '0.7rem'
          }} 
        />
      )
    },
    { 
      field: 'investment_amount', 
      headerName: 'Amount', 
      width: 140,
      valueFormatter: (value: number) => formatCurrency(value)
    },
    { 
      field: 'expected_return', 
      headerName: 'Expected %', 
      width: 120,
      valueFormatter: (value: number) => `${value}%`
    },
    { 
      field: 'investment_date', 
      headerName: 'Inv. Date', 
      width: 120,
      valueFormatter: (value: string) => formatDate(value)
    },
    { 
      field: 'transaction_status', 
      headerName: 'Status', 
      width: 120,
      renderCell: (params: GridRenderCellParams) => {
        const colors: Record<string, string> = {
          'Active': '#06A77D', 'Matured': '#4361EE', 'Cancelled': '#FFB703', 'Defaulted': '#F72585'
        };
        const color = colors[params.value as string] || '#aaa';
        return (
          <Chip 
            label={params.value} 
            size="small" 
            sx={{ bgcolor: `${color}22`, color, fontWeight: 600, fontSize: '0.7rem' }} 
          />
        );
      }
    }
  ];

  return (
    <Box sx={{ p: { xs: 2, md: 4 } }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h4" sx={{ fontWeight: 800 }}>Transactions</Typography>
          <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.4)' }}>View and search all platform transactions</Typography>
        </Box>
        <Button 
          variant="outlined" 
          startIcon={<FileDownloadIcon />}
          onClick={handleDownloadCsv}
          sx={{ color: '#fff', borderColor: 'rgba(255,255,255,0.2)' }}
        >
          Export CSV
        </Button>
      </Box>

      <Paper sx={{ p: 2, mb: 3, bgcolor: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.08)' }}>
        <TextField
          fullWidth
          placeholder="Search by investor name or email..."
          variant="outlined"
          size="small"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          slotProps={{
            input: {
              startAdornment: <InputAdornment position="start"><SearchIcon sx={{ color: 'rgba(255,255,255,0.4)' }} /></InputAdornment>,
              sx: { color: '#fff', '& fieldset': { borderColor: 'rgba(255,255,255,0.1)' } }
            }
          }}
        />
      </Paper>

      <Paper sx={{ height: 600, bgcolor: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.08)' }}>
        <DataGrid
          rows={data?.data?.items || []}
          rowCount={data?.data?.total || 0}
          loading={isLoading}
          paginationMode="server"
          paginationModel={paginationModel}
          onPaginationModelChange={setPaginationModel}
          columns={columns}
          getRowId={(row) => row.transaction_id}
          disableRowSelectionOnClick
          sx={{
            border: 'none',
            color: '#fff',
            '& .MuiDataGrid-cell': { borderBottom: '1px solid rgba(255,255,255,0.05)' },
            '& .MuiDataGrid-columnHeaders': { bgcolor: 'rgba(255,255,255,0.02)', borderBottom: '1px solid rgba(255,255,255,0.1)' },
            '& .MuiDataGrid-footerContainer': { borderTop: '1px solid rgba(255,255,255,0.1)' },
            '& .MuiTablePagination-root': { color: '#fff' }
          }}
        />
      </Paper>
    </Box>
  );
};

export default TransactionsPage;
