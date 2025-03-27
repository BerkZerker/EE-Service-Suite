import axios, { AxiosError, AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

// Types
export interface ApiError {
  detail: string;
  status_code: number;
}

// API client class with interceptors and error handling
class ApiClient {
  private client: AxiosInstance;

  constructor(baseURL: string) {
    this.client = axios.create({
      baseURL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        // Get token from local storage
        const tokens = localStorage.getItem('auth_tokens');
        if (tokens) {
          const { access_token } = JSON.parse(tokens);
          // Set auth header if token exists
          if (access_token && config.headers) {
            config.headers.Authorization = `Bearer ${access_token}`;
          }
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean };
        
        // Handle 401 errors (unauthorized) by trying to refresh token
        if (error.response?.status === 401 && !originalRequest._retry) {
          // Mark this request as retried to prevent infinite loops
          originalRequest._retry = true;
          
          try {
            // Get refresh token
            const tokens = localStorage.getItem('auth_tokens');
            if (!tokens) {
              // No tokens, redirect to login
              window.location.href = '/login';
              return Promise.reject(error);
            }
            
            const { refresh_token } = JSON.parse(tokens);
            
            // Call refresh token endpoint
            const response = await axios.post('/api/auth/refresh', {
              refresh_token,
            });
            
            // Save new tokens
            localStorage.setItem('auth_tokens', JSON.stringify(response.data));
            
            // Update auth header
            const { access_token } = response.data;
            this.client.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
            
            // Retry original request with new token
            if (originalRequest.headers) {
              originalRequest.headers.Authorization = `Bearer ${access_token}`;
            }
            
            return this.client(originalRequest);
          } catch (refreshError) {
            // Refresh token failed, redirect to login
            localStorage.removeItem('auth_tokens');
            window.location.href = '/login';
            return Promise.reject(refreshError);
          }
        }
        
        // Handle other errors
        return Promise.reject(error);
      }
    );
  }

  // Basic CRUD methods
  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.get<T>(url, config);
    return response.data;
  }

  async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.post<T>(url, data, config);
    return response.data;
  }

  async put<T>(url: string, data: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.put<T>(url, data, config);
    return response.data;
  }

  async patch<T>(url: string, data: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.patch<T>(url, data, config);
    return response.data;
  }

  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.delete<T>(url, config);
    return response.data;
  }
}

// Create API instance
const apiClient = new ApiClient('/api');

export default apiClient;