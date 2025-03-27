import apiClient from './api-client';

// Types
export interface Part {
  id: string;
  name: string;
  description: string;
  sku: string;
  category: string;
  cost_price: number;
  retail_price: number;
  quantity_on_hand: number;
  reorder_threshold: number;
  created_at: string;
  updated_at: string;
}

export interface PartCreateRequest {
  name: string;
  description: string;
  sku: string;
  category: string;
  cost_price: number;
  retail_price: number;
  quantity_on_hand: number;
  reorder_threshold: number;
}

export interface PartUpdateRequest {
  name?: string;
  description?: string;
  sku?: string;
  category?: string;
  cost_price?: number;
  retail_price?: number;
  quantity_on_hand?: number;
  reorder_threshold?: number;
}

// Part service functions
export const partService = {
  /**
   * Get all parts
   */
  getParts: async (skip = 0, limit = 100): Promise<Part[]> => {
    return apiClient.get<Part[]>(`/parts/?skip=${skip}&limit=${limit}`);
  },

  /**
   * Get part by ID
   */
  getPart: async (id: string): Promise<Part> => {
    return apiClient.get<Part>(`/parts/${id}`);
  },

  /**
   * Create a new part
   */
  createPart: async (part: PartCreateRequest): Promise<Part> => {
    return apiClient.post<Part>('/parts/', part);
  },

  /**
   * Update an existing part
   */
  updatePart: async (id: string, part: PartUpdateRequest): Promise<Part> => {
    return apiClient.put<Part>(`/parts/${id}`, part);
  },

  /**
   * Delete a part
   */
  deletePart: async (id: string): Promise<void> => {
    return apiClient.delete<void>(`/parts/${id}`);
  },

  /**
   * Search parts by name or SKU
   */
  searchParts: async (query: string): Promise<Part[]> => {
    return apiClient.get<Part[]>(`/parts/search?q=${encodeURIComponent(query)}`);
  }
};

export default partService;