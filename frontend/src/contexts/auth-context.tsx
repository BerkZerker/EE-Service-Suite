import { createContext, useState, useContext, useEffect, ReactNode } from 'react';
import axios from 'axios';

// Types
type User = {
  id: string;
  email: string;
  full_name: string;
  is_admin: boolean;
};

type AuthTokens = {
  access_token: string;
  refresh_token: string;
  token_type: string;
};

type AuthContextType = {
  user: User | null;
  loading: boolean;
  error: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<void>;
};

// Create context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Provider component
export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Initialize auth state from localStorage
  useEffect(() => {
    const initializeAuth = async () => {
      const tokens = localStorage.getItem('auth_tokens');
      
      if (tokens) {
        try {
          // Set axios default headers with token
          const parsedTokens: AuthTokens = JSON.parse(tokens);
          axios.defaults.headers.common['Authorization'] = `Bearer ${parsedTokens.access_token}`;
          
          // Validate token and get user info
          const response = await axios.post('/api/auth/test-token');
          setUser(response.data.user);
        } catch (err) {
          // Token might be expired, try to refresh
          try {
            await refreshToken();
          } catch (refreshErr) {
            // If refresh fails, clear everything
            localStorage.removeItem('auth_tokens');
            setUser(null);
            setError('Session expired. Please login again.');
          }
        } finally {
          setLoading(false);
        }
      } else {
        setLoading(false);
      }
    };

    initializeAuth();
  }, []);

  // Login function
  const login = async (email: string, password: string) => {
    try {
      setLoading(true);
      setError(null);
      
      const formData = new FormData();
      formData.append('username', email); // OAuth2 expects username field
      formData.append('password', password);
      
      const response = await axios.post<AuthTokens>('/api/auth/login', formData);
      
      // Save tokens
      localStorage.setItem('auth_tokens', JSON.stringify(response.data));
      
      // Set default auth header
      axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access_token}`;
      
      // Get user info
      const userResponse = await axios.post('/api/auth/test-token');
      setUser(userResponse.data.user);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to login');
    } finally {
      setLoading(false);
    }
  };

  // Logout function
  const logout = () => {
    localStorage.removeItem('auth_tokens');
    delete axios.defaults.headers.common['Authorization'];
    setUser(null);
  };

  // Refresh token
  const refreshToken = async () => {
    const tokens = localStorage.getItem('auth_tokens');
    if (!tokens) {
      throw new Error('No refresh token available');
    }
    
    const parsedTokens: AuthTokens = JSON.parse(tokens);
    
    try {
      const response = await axios.post<AuthTokens>('/api/auth/refresh', {
        refresh_token: parsedTokens.refresh_token
      });
      
      // Save new tokens
      localStorage.setItem('auth_tokens', JSON.stringify(response.data));
      
      // Update auth header
      axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access_token}`;
      
      // Get user info
      const userResponse = await axios.post('/api/auth/test-token');
      setUser(userResponse.data.user);
    } catch (err) {
      // If refresh fails, force logout
      logout();
      throw err;
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        error,
        isAuthenticated: !!user,
        login,
        logout,
        refreshToken
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

// Hook for easy context use
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};