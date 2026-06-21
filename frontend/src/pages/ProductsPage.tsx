import React from 'react';
import { useQuery } from 'react-query';
import {
  Box, Typography, Chip, Grid, Card, CardContent, Button
} from '@mui/material';
import { productsApi } from '../api';
import { formatCurrency, formatPercent, CATEGORY_COLORS } from '../utils/formatters';
import AddIcon from '@mui/icons-material/Add';

const ProductsPage: React.FC = () => {
  const { data, isLoading } = useQuery('products', () => productsApi.list());

  return (
    <Box sx={{ p: { xs: 2, md: 4 } }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Box>
          <Typography variant="h4" sx={{ fontWeight: 800 }}>Products</Typography>
          <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.4)' }}>Manage investment products</Typography>
        </Box>
        <Button 
          variant="contained" 
          startIcon={<AddIcon />}
          sx={{ background: 'linear-gradient(135deg, #4361EE, #7209B7)' }}
        >
          Add Product
        </Button>
      </Box>

      {isLoading ? (
        <Typography>Loading products...</Typography>
      ) : (
        <Grid container spacing={3}>
          {data?.data?.items?.map((product: any) => (
            <Grid size={{ xs: 12, sm: 6, md: 4 }} key={product.product_id}>
              <Card sx={{ 
                bgcolor: 'rgba(255,255,255,0.03)', 
                border: '1px solid rgba(255,255,255,0.08)',
                borderRadius: 3,
                height: '100%',
                display: 'flex',
                flexDirection: 'column'
              }}>
                <Box sx={{ 
                  height: 4, 
                  bgcolor: CATEGORY_COLORS[product.category] || '#4361EE',
                  width: '100%' 
                }} />
                <CardContent sx={{ flex: 1, p: 3 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                    <Chip 
                      label={product.category} 
                      size="small" 
                      sx={{ 
                        bgcolor: `${CATEGORY_COLORS[product.category] || '#4361EE'}22`, 
                        color: CATEGORY_COLORS[product.category] || '#4361EE',
                        fontWeight: 600,
                        fontSize: '0.65rem'
                      }} 
                    />
                    <Chip 
                      label={product.is_active === 'Yes' ? 'Active' : 'Inactive'} 
                      size="small" 
                      sx={{ 
                        bgcolor: product.is_active === 'Yes' ? 'rgba(6,167,125,0.2)' : 'rgba(255,255,255,0.1)', 
                        color: product.is_active === 'Yes' ? '#06A77D' : '#aaa',
                        fontWeight: 600,
                        fontSize: '0.65rem'
                      }} 
                    />
                  </Box>
                  <Typography variant="h6" sx={{ fontWeight: 700, mb: 1, lineHeight: 1.2 }}>
                    {product.product_name}
                  </Typography>
                  
                  <Grid container spacing={2} sx={{ mt: 2 }}>
                    <Grid size={6}>
                      <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.4)', display: 'block' }}>Expected Return</Typography>
                      <Typography variant="body1" sx={{ color: '#06A77D', fontWeight: 700 }}>
                        {formatPercent(product.expected_return)}
                      </Typography>
                    </Grid>
                    <Grid size={6}>
                      <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.4)', display: 'block' }}>Tenure</Typography>
                      <Typography variant="body1" sx={{ color: '#fff', fontWeight: 700 }}>
                        {product.tenure_months} months
                      </Typography>
                    </Grid>
                    <Grid size={6}>
                      <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.4)', display: 'block' }}>Min Investment</Typography>
                      <Typography variant="body1" sx={{ color: '#fff', fontWeight: 600 }}>
                        {formatCurrency(product.min_investment)}
                      </Typography>
                    </Grid>
                    <Grid size={6}>
                      <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.4)', display: 'block' }}>Risk Level</Typography>
                      <Typography variant="body1" sx={{ color: '#fff', fontWeight: 600 }}>
                        {product.risk_level}
                      </Typography>
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );
};

export default ProductsPage;
