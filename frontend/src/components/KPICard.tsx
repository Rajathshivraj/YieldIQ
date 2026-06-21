import React from 'react';
import {
  Box, Card, CardContent, Typography, Chip, Skeleton,
} from '@mui/material';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';
import RemoveIcon from '@mui/icons-material/Remove';

interface KPICardProps {
  title: string;
  value: string | number;
  change?: number;
  subtitle?: string;
  icon: React.ReactNode;
  color?: string;
  loading?: boolean;
}

const KPICard: React.FC<KPICardProps> = ({
  title, value, change, subtitle, icon, color = '#4361EE', loading = false,
}) => {
  const trend = change === undefined ? null : change > 0 ? 'up' : change < 0 ? 'down' : 'flat';

  return (
    <Card
      sx={{
        background: 'linear-gradient(135deg, #1a1f3a 0%, #252a4a 100%)',
        border: '1px solid rgba(255,255,255,0.08)',
        borderRadius: 3,
        height: '100%',
        transition: 'transform 0.2s, box-shadow 0.2s',
        '&:hover': {
          transform: 'translateY(-4px)',
          boxShadow: `0 12px 40px ${color}33`,
        },
      }}
    >
      <CardContent sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
          <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.6)', fontWeight: 500, textTransform: 'uppercase', letterSpacing: 1, fontSize: '0.7rem' }}>
            {title}
          </Typography>
          <Box sx={{ p: 1, borderRadius: 2, background: `${color}22`, color, display: 'flex' }}>
            {icon}
          </Box>
        </Box>

        {loading ? (
          <>
            <Skeleton variant="text" width="60%" height={48} sx={{ bgcolor: 'rgba(255,255,255,0.1)' }} />
            <Skeleton variant="text" width="40%" height={24} sx={{ bgcolor: 'rgba(255,255,255,0.05)' }} />
          </>
        ) : (
          <>
            <Typography variant="h4" sx={{ color: '#fff', fontWeight: 700, mb: 1, lineHeight: 1.1 }}>
              {value}
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              {trend && (
                <Chip
                  size="small"
                  icon={trend === 'up' ? <TrendingUpIcon fontSize="small" /> : trend === 'down' ? <TrendingDownIcon fontSize="small" /> : <RemoveIcon fontSize="small" />}
                  label={`${change! > 0 ? '+' : ''}${change!.toFixed(1)}%`}
                  sx={{
                    bgcolor: trend === 'up' ? 'rgba(0,200,100,0.15)' : trend === 'down' ? 'rgba(255,60,60,0.15)' : 'rgba(255,255,255,0.1)',
                    color: trend === 'up' ? '#00C864' : trend === 'down' ? '#FF3C3C' : '#aaa',
                    fontWeight: 600,
                    fontSize: '0.7rem',
                    '& .MuiChip-icon': { color: 'inherit' },
                  }}
                />
              )}
              {subtitle && (
                <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.4)' }}>
                  {subtitle}
                </Typography>
              )}
            </Box>
          </>
        )}
      </CardContent>
    </Card>
  );
};

export default KPICard;
