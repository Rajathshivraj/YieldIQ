import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import { User, AuthState } from '../types';
import { authApi } from '../api';

interface AuthContextType extends AuthState {
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  loading: boolean;
  error: string | null;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const storedToken = localStorage.getItem('yieldiq_token');
  const storedUser = localStorage.getItem('yieldiq_user');

  const [token, setToken] = useState<string | null>(storedToken);
  const [user, setUser] = useState<User | null>(storedUser ? JSON.parse(storedUser) : null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const login = useCallback(async (email: string, password: string) => {
    setLoading(true);
    setError(null);
    try {
      const res = await authApi.login(email, password);
      const { access_token, role, full_name, email: userEmail } = res.data;

      const userData: User = {
        id: '',
        email: userEmail,
        full_name,
        role,
        is_active: true,
      };

      localStorage.setItem('yieldiq_token', access_token);
      localStorage.setItem('yieldiq_user', JSON.stringify(userData));
      setToken(access_token);
      setUser(userData);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed. Please try again.');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem('yieldiq_token');
    localStorage.removeItem('yieldiq_user');
    setToken(null);
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider
      value={{ user, token, isAuthenticated: !!token, login, logout, loading, error }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
};
