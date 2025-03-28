import apiClient from './api-client';

// Types
export interface Customer {
  id: string;
  full_name: string;
  email: string;
  phone: string;
  address: string;
  created_at: string;
  updated_at: string;
  bikes?: Bike[];
}

export interface Bike {
  id: string;
  customer_id: string;
  make: string;
  model: string;
  serial_number: string;
  purchase_date: string;
  created_at: string;
  updated_at: string;
}

export interface CustomerCreateRequest {
  full_name: string;
  email: string;
  phone: string;
  address: string;
}

export interface CustomerUpdateRequest {
  full_name?: string;
  email?: string;
  phone?: string;
  address?: string;
}

// Customer service functions
export const customerService = {
  /**
   * Get all customers
   */
  getCustomers: async (skip = 0, limit = 100): Promise<Customer[]> => {
    return apiClient.get<Customer[]>(`/customers/?skip=${skip}&limit=${limit}`);
  },

  /**
   * Get customer by ID
   */
  getCustomer: async (id: string): Promise<Customer> => {
    return apiClient.get<Customer>(`/customers/${id}`);
  },

  /**
   * Create a new customer
   */
  createCustomer: async (customer: CustomerCreateRequest): Promise<Customer> => {
    return apiClient.post<Customer>('/customers/', customer);
  },

  /**
   * Update an existing customer
   */
  updateCustomer: async (id: string, customer: CustomerUpdateRequest): Promise<Customer> => {
    return apiClient.put<Customer>(`/customers/${id}`, customer);
  },

  /**
   * Delete a customer
   */
  deleteCustomer: async (id: string): Promise<void> => {
    return apiClient.delete<void>(`/customers/${id}`);
  },

  /**
   * Get all bikes for a customer
   */
  getCustomerBikes: async (customerId: string): Promise<Bike[]> => {
    return apiClient.get<Bike[]>(`/customers/${customerId}/bikes`);
  },
  
  /**
   * Get bike by ID
   */
  getBike: async (bikeId: string): Promise<Bike> => {
    return apiClient.get<Bike>(`/bikes/${bikeId}`);
  },

  /**
   * Create a bike for a customer
   */
  createCustomerBike: async (customerId: string, bike: Omit<Bike, 'id' | 'customer_id' | 'created_at' | 'updated_at'>): Promise<Bike> => {
    return apiClient.post<Bike>(`/customers/${customerId}/bikes`, bike);
  }
};

export default customerService;