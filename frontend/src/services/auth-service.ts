import apiClient from './api-client';

// Types
export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface UserResponse {
  success: boolean;
  msg: string;
  user: {
    id: string;
    email: string;
    full_name: string;
    is_admin: boolean;
  };
}

// Auth service functions
export const authService = {
  /**
   * Login with email and password
   */
  login: async (email: string, password: string): Promise<AuthTokens> => {
    const formData = new FormData();
    formData.append('username', email); // OAuth2 expects username field
    formData.append('password', password);
    
    return apiClient.post<AuthTokens>('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  /**
   * Refresh access token using refresh token
   */
  refreshToken: async (refreshToken: string): Promise<AuthTokens> => {
    return apiClient.post<AuthTokens>('/auth/refresh', {
      refresh_token: refreshToken,
    });
  },

  /**
   * Get current user info (validate token)
   */
  getCurrentUser: async (): Promise<UserResponse> => {
    return apiClient.post<UserResponse>('/auth/test-token');
  },
};

export default authService;