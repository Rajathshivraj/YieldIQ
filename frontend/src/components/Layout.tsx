import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  Box, Drawer, AppBar, Toolbar, Typography, List, ListItem,
  ListItemButton, ListItemIcon, ListItemText, IconButton, Avatar,
  Tooltip, Divider, Chip,
} from '@mui/material';
import DashboardIcon from '@mui/icons-material/Dashboard';
import PeopleIcon from '@mui/icons-material/People';
import AccountBalanceIcon from '@mui/icons-material/AccountBalance';
import ReceiptLongIcon from '@mui/icons-material/ReceiptLong';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import BarChartIcon from '@mui/icons-material/BarChart';
import PieChartIcon from '@mui/icons-material/PieChart';
import GroupsIcon from '@mui/icons-material/Groups';
import LogoutIcon from '@mui/icons-material/Logout';
import MenuIcon from '@mui/icons-material/Menu';
import { useAuth } from '../store/AuthContext';

const DRAWER_WIDTH = 260;

const navItems = [
  { label: 'Executive Dashboard', icon: <DashboardIcon />, path: '/' },
  { label: 'Investors', icon: <PeopleIcon />, path: '/investors' },
  { label: 'Transactions', icon: <ReceiptLongIcon />, path: '/transactions' },
  { label: 'Products', icon: <AccountBalanceIcon />, path: '/products' },
  { label: 'Portfolio', icon: <PieChartIcon />, path: '/portfolio' },
  { label: 'Revenue', icon: <TrendingUpIcon />, path: '/revenue' },
  { label: 'Cohort Analysis', icon: <GroupsIcon />, path: '/cohorts' },
  { label: 'Product Analytics', icon: <BarChartIcon />, path: '/product-analytics' },
];

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [mobileOpen, setMobileOpen] = useState(false);

  const drawer = (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column', bgcolor: '#0D1117' }}>
      {/* Logo */}
      <Box sx={{ p: 3, display: 'flex', alignItems: 'center', gap: 1.5 }}>
        <Box
          sx={{
            width: 38, height: 38, borderRadius: 2,
            background: 'linear-gradient(135deg, #4361EE, #7209B7)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
          }}
        >
          <TrendingUpIcon sx={{ color: '#fff', fontSize: 22 }} />
        </Box>
        <Box>
          <Typography variant="h6" sx={{ color: '#fff', fontWeight: 800, lineHeight: 1.1 }}>
            YieldIQ
          </Typography>
          <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.4)', fontSize: '0.65rem' }}>
            Fixed Income Analytics
          </Typography>
        </Box>
      </Box>

      <Divider sx={{ bgcolor: 'rgba(255,255,255,0.06)' }} />

      {/* Nav items */}
      <List sx={{ flex: 1, px: 1.5, py: 2 }}>
        {navItems.map((item) => {
          const active = location.pathname === item.path;
          return (
            <ListItem key={item.path} disablePadding sx={{ mb: 0.5 }}>
              <ListItemButton
                onClick={() => { navigate(item.path); setMobileOpen(false); }}
                sx={{
                  borderRadius: 2,
                  color: active ? '#fff' : 'rgba(255,255,255,0.5)',
                  bgcolor: active ? 'rgba(67,97,238,0.2)' : 'transparent',
                  borderLeft: active ? '3px solid #4361EE' : '3px solid transparent',
                  '&:hover': { bgcolor: 'rgba(255,255,255,0.06)', color: '#fff' },
                  transition: 'all 0.15s',
                }}
              >
                <ListItemIcon sx={{ color: 'inherit', minWidth: 40 }}>
                  {item.icon}
                </ListItemIcon>
                <ListItemText
                  primary={item.label}
                  slotProps={{ primary: { style: { fontSize: '0.875rem', fontWeight: active ? 600 : 400 } } }}
                />
              </ListItemButton>
            </ListItem>
          );
        })}
      </List>

      <Divider sx={{ bgcolor: 'rgba(255,255,255,0.06)' }} />

      {/* User section */}
      <Box sx={{ p: 2, display: 'flex', alignItems: 'center', gap: 1.5 }}>
        <Avatar sx={{ width: 36, height: 36, bgcolor: '#4361EE', fontSize: '0.875rem', fontWeight: 700 }}>
          {user?.full_name?.charAt(0) || 'U'}
        </Avatar>
        <Box sx={{ flex: 1, minWidth: 0 }}>
          <Typography variant="body2" sx={{ color: '#fff', fontWeight: 600 }} noWrap>
            {user?.full_name}
          </Typography>
          <Chip
            label={user?.role}
            size="small"
            sx={{ height: 18, fontSize: '0.6rem', bgcolor: 'rgba(67,97,238,0.3)', color: '#a0b4ff' }}
          />
        </Box>
        <Tooltip title="Logout">
          <IconButton size="small" onClick={logout} sx={{ color: 'rgba(255,255,255,0.4)', '&:hover': { color: '#FF3C3C' } }}>
            <LogoutIcon fontSize="small" />
          </IconButton>
        </Tooltip>
      </Box>
    </Box>
  );

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: '#0A0E1A' }}>
      {/* Mobile AppBar */}
      <AppBar
        position="fixed"
        sx={{ display: { md: 'none' }, bgcolor: '#0D1117', boxShadow: 'none', borderBottom: '1px solid rgba(255,255,255,0.06)' }}
      >
        <Toolbar>
          <IconButton color="inherit" edge="start" onClick={() => setMobileOpen(!mobileOpen)} sx={{ mr: 2 }}>
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" sx={{ fontWeight: 800 }}>YieldIQ</Typography>
        </Toolbar>
      </AppBar>

      {/* Drawer */}
      <Box component="nav" sx={{ width: { md: DRAWER_WIDTH }, flexShrink: { md: 0 } }}>
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={() => setMobileOpen(false)}
          ModalProps={{ keepMounted: true }}
          sx={{ display: { xs: 'block', md: 'none' }, '& .MuiDrawer-paper': { width: DRAWER_WIDTH, bgcolor: '#0D1117', border: 'none' } }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{ display: { xs: 'none', md: 'block' }, '& .MuiDrawer-paper': { width: DRAWER_WIDTH, bgcolor: '#0D1117', border: 'none', borderRight: '1px solid rgba(255,255,255,0.06)' } }}
          open
        >
          {drawer}
        </Drawer>
      </Box>

      {/* Main content */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          width: { md: `calc(100% - ${DRAWER_WIDTH}px)` },
          mt: { xs: 8, md: 0 },
          minHeight: '100vh',
          overflow: 'auto',
        }}
      >
        {children}
      </Box>
    </Box>
  );
};

export default Layout;
