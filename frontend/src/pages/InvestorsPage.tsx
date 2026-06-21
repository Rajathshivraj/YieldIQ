import React, { useState } from 'react';
import { useQuery } from 'react-query';
import {
  Box, Typography, Paper, TextField, InputAdornment, Chip, IconButton, Button,
  Dialog, DialogTitle, DialogContent, DialogActions
} from '@mui/material';
import { DataGrid, GridColDef, GridRenderCellParams } from '@mui/x-data-grid';
import SearchIcon from '@mui/icons-material/Search';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import VisibilityIcon from '@mui/icons-material/Visibility';
import { investorsApi, reportsApi } from '../api';
import { getSegmentColor, getStatusColor, formatDate } from '../utils/formatters';

const InvestorsPage: React.FC = () => {
  const [paginationModel, setPaginationModel] = useState({ page: 0, pageSize: 50 });
  const [search, setSearch] = useState('');
  
  // Debounce search slightly
  const [debouncedSearch, setDebouncedSearch] = useState('');
  React.useEffect(() => {
    const timer = setTimeout(() => setDebouncedSearch(search), 500);
    return () => clearTimeout(timer);
  }, [search]);

  const { data, isLoading } = useQuery(
    ['investors', paginationModel.page, paginationModel.pageSize, debouncedSearch],
    () => investorsApi.list({ page: paginationModel.page + 1, page_size: paginationModel.pageSize, search: debouncedSearch }),
    { keepPreviousData: true }
  );

  const handleDownloadCsv = () => {
    window.open(reportsApi.investorsCsv(), '_blank');
  };

  const [selectedInvestorId, setSelectedInvestorId] = useState<string | null>(null);

  const columns: GridColDef[] = [
    { field: 'full_name', headerName: 'Name', flex: 1, minWidth: 200 },
    { field: 'email', headerName: 'Email', flex: 1, minWidth: 200 },
    { field: 'city', headerName: 'City', width: 150 },
    { 
      field: 'investor_segment', 
      headerName: 'Segment', 
      width: 150,
      renderCell: (params: GridRenderCellParams) => (
        <Chip 
          label={params.value} 
          size="small" 
          sx={{ 
            bgcolor: `${getSegmentColor(params.value)}22`, 
            color: getSegmentColor(params.value),
            fontWeight: 600 
          }} 
        />
      )
    },
    { field: 'risk_profile', headerName: 'Risk Profile', width: 150 },
    { 
      field: 'status', 
      headerName: 'Status', 
      width: 120,
      renderCell: (params: GridRenderCellParams) => (
        <Chip 
          label={params.value} 
          color={getStatusColor(params.value)} 
          size="small" 
          variant="outlined"
        />
      )
    },
    { 
      field: 'registration_date', 
      headerName: 'Registered On', 
      width: 150,
      valueFormatter: (value: string) => formatDate(value)
    },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 100,
      sortable: false,
      renderCell: (params: GridRenderCellParams) => (
        <IconButton size="small" onClick={() => setSelectedInvestorId(params.row.investor_id)}>
          <VisibilityIcon fontSize="small" sx={{ color: 'rgba(255,255,255,0.6)' }} />
        </IconButton>
      )
    }
  ];

  return (
    <Box sx={{ p: { xs: 2, md: 4 } }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h4" sx={{ fontWeight: 800 }}>Investors</Typography>
          <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.4)' }}>Manage investor profiles and segments</Typography>
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
          placeholder="Search by name, email, or city..."
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
          getRowId={(row) => row.investor_id}
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

      {/* Portfolio Dialog Placeholder */}
      <Dialog open={!!selectedInvestorId} onClose={() => setSelectedInvestorId(null)} maxWidth="md" fullWidth>
        <DialogTitle sx={{ bgcolor: '#0D1117', color: '#fff' }}>Investor Details</DialogTitle>
        <DialogContent sx={{ bgcolor: '#0D1117', color: '#fff', pt: 2 }}>
           <Typography>Detailed portfolio view goes here for {selectedInvestorId}.</Typography>
        </DialogContent>
        <DialogActions sx={{ bgcolor: '#0D1117' }}>
          <Button onClick={() => setSelectedInvestorId(null)} sx={{ color: '#fff' }}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default InvestorsPage;
