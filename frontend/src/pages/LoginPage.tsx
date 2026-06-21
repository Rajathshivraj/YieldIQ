import React, { useState } from 'react';
import {
  Box, Paper, Typography, TextField, Button, Alert,
  InputAdornment, IconButton, CircularProgress, Divider, Chip,
} from '@mui/material';
import EmailIcon from '@mui/icons-material/Email';
import LockIcon from '@mui/icons-material/Lock';
import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../store/AuthContext';

const LoginPage: React.FC = () => {
  const { login, loading, error } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState('admin@yieldiq.com');
  const [password, setPassword] = useState('Admin@123');
  const [showPass, setShowPass] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await login(email, password);
      navigate('/');
    } catch {}
  };

  const quickLogin = (role: string) => {
    const creds: Record<string, { email: string; password: string }> = {
      admin: { email: 'admin@yieldiq.com', password: 'Admin@123' },
      analyst: { email: 'analyst@yieldiq.com', password: 'Analyst@123' },
      viewer: { email: 'viewer@yieldiq.com', password: 'Viewer@123' },
    };
    setEmail(creds[role].email);
    setPassword(creds[role].password);
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #0A0E1A 0%, #0D1117 40%, #131929 100%)',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* Background decorations */}
      <Box sx={{
        position: 'absolute', width: 600, height: 600, borderRadius: '50%',
        background: 'radial-gradient(circle, rgba(67,97,238,0.12) 0%, transparent 70%)',
        top: -200, right: -200, pointerEvents: 'none',
      }} />
      <Box sx={{
        position: 'absolute', width: 400, height: 400, borderRadius: '50%',
        background: 'radial-gradient(circle, rgba(114,9,183,0.10) 0%, transparent 70%)',
        bottom: -100, left: -100, pointerEvents: 'none',
      }} />

      <Paper
        elevation={0}
        sx={{
          width: '100%', maxWidth: 460, mx: 2,
          bgcolor: 'rgba(255,255,255,0.03)',
          backdropFilter: 'blur(20px)',
          border: '1px solid rgba(255,255,255,0.1)',
          borderRadius: 4, p: 5,
        }}
      >
        {/* Brand */}
        <Box sx={{ textAlign: 'center', mb: 4 }}>
          <Box sx={{
            width: 56, height: 56, borderRadius: 3, mx: 'auto', mb: 2,
            background: 'linear-gradient(135deg, #4361EE, #7209B7)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            boxShadow: '0 8px 32px rgba(67,97,238,0.4)',
          }}>
            <TrendingUpIcon sx={{ color: '#fff', fontSize: 32 }} />
          </Box>
          <Typography variant="h4" sx={{ color: '#fff', fontWeight: 800, mb: 0.5 }}>
            YieldIQ
          </Typography>
          <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.4)' }}>
            Fixed Income Analytics Platform
          </Typography>
        </Box>

        {/* Quick login chips */}
        <Box sx={{ mb: 3, display: 'flex', gap: 1, justifyContent: 'center', flexWrap: 'wrap' }}>
          <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.3)', width: '100%', textAlign: 'center', mb: 0.5 }}>
            Quick login:
          </Typography>
          {['admin', 'analyst', 'viewer'].map((role) => (
            <Chip
              key={role}
              label={role}
              size="small"
              onClick={() => quickLogin(role)}
              sx={{
                bgcolor: 'rgba(67,97,238,0.15)', color: '#a0b4ff', cursor: 'pointer',
                textTransform: 'capitalize',
                '&:hover': { bgcolor: 'rgba(67,97,238,0.3)' },
              }}
            />
          ))}
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 3, bgcolor: 'rgba(255,60,60,0.1)', color: '#FF3C3C', border: '1px solid rgba(255,60,60,0.2)' }}>
            {error}
          </Alert>
        )}

        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth label="Email" type="email" value={email}
            onChange={(e) => setEmail(e.target.value)}
            required autoComplete="email"
            slotProps={{
              input: {
                startAdornment: <InputAdornment position="start"><EmailIcon sx={{ color: 'rgba(255,255,255,0.3)', fontSize: 20 }} /></InputAdornment>,
              }
            }}
            sx={{
              mb: 2.5,
              '& .MuiOutlinedInput-root': {
                color: '#fff',
                '& fieldset': { borderColor: 'rgba(255,255,255,0.15)' },
                '&:hover fieldset': { borderColor: 'rgba(255,255,255,0.3)' },
                '&.Mui-focused fieldset': { borderColor: '#4361EE' },
              },
              '& .MuiInputLabel-root': { color: 'rgba(255,255,255,0.4)' },
              '& .MuiInputLabel-root.Mui-focused': { color: '#4361EE' },
            }}
          />

          <TextField
            fullWidth label="Password" type={showPass ? 'text' : 'password'}
            value={password} onChange={(e) => setPassword(e.target.value)}
            required autoComplete="current-password"
            slotProps={{
              input: {
                startAdornment: <InputAdornment position="start"><LockIcon sx={{ color: 'rgba(255,255,255,0.3)', fontSize: 20 }} /></InputAdornment>,
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton onClick={() => setShowPass(!showPass)} size="small" sx={{ color: 'rgba(255,255,255,0.3)' }}>
                      {showPass ? <VisibilityOffIcon /> : <VisibilityIcon />}
                    </IconButton>
                  </InputAdornment>
                ),
              }
            }}
            sx={{
              mb: 3,
              '& .MuiOutlinedInput-root': {
                color: '#fff',
                '& fieldset': { borderColor: 'rgba(255,255,255,0.15)' },
                '&:hover fieldset': { borderColor: 'rgba(255,255,255,0.3)' },
                '&.Mui-focused fieldset': { borderColor: '#4361EE' },
              },
              '& .MuiInputLabel-root': { color: 'rgba(255,255,255,0.4)' },
              '& .MuiInputLabel-root.Mui-focused': { color: '#4361EE' },
            }}
          />

          <Button
            type="submit" fullWidth variant="contained" size="large"
            disabled={loading}
            sx={{
              py: 1.5, fontWeight: 700, fontSize: '1rem',
              background: 'linear-gradient(135deg, #4361EE, #7209B7)',
              borderRadius: 2,
              boxShadow: '0 8px 32px rgba(67,97,238,0.4)',
              '&:hover': { background: 'linear-gradient(135deg, #3451DE, #6009A7)', boxShadow: '0 12px 40px rgba(67,97,238,0.6)' },
              '&:disabled': { opacity: 0.6 },
            }}
          >
            {loading ? <CircularProgress size={24} color="inherit" /> : 'Sign In'}
          </Button>
        </form>

        <Divider sx={{ my: 3, bgcolor: 'rgba(255,255,255,0.06)' }} />

        <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.25)', textAlign: 'center', display: 'block' }}>
          YieldIQ v1.0 · Fixed Income Analytics · Secured with JWT
        </Typography>
      </Paper>
    </Box>
  );
};

export default LoginPage;
