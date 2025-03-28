import apiClient from './api-client';
import { Bike } from './customer-service';

// Types
export enum TicketStatus {
  INTAKE = 'intake',
  DIAGNOSIS = 'diagnosis',
  AWAITING_PARTS = 'awaiting_parts',
  IN_PROGRESS = 'in_progress',
  COMPLETE = 'complete',
  DELIVERED = 'delivered'
}

export enum TicketPriority {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  URGENT = 'urgent'
}

export interface TicketPart {
  id: string;
  ticket_id: string;
  part_id: string;
  quantity: number;
  price: number;
  part_name: string;
  created_at: string;
  updated_at: string;
}

export interface TicketUpdate {
  id: string;
  ticket_id: string;
  status: TicketStatus;
  note: string;
  user_id: string;
  user_name: string;
  created_at: string;
}

export interface Ticket {
  id: string;
  ticket_number: string;
  problem_description: string;
  diagnosis: string | null;
  status: TicketStatus;
  priority: TicketPriority;
  estimated_completion: string | null;
  bike_id: string;
  technician_id: string | null;
  labor_cost: number;
  total_parts_cost: number;
  created_at: string;
  updated_at: string;
  is_archived: boolean;
  total?: number; // Optional field calculated on frontend
}

export interface TicketWithDetails extends Ticket {
  updates: TicketUpdate[];
  parts: TicketPart[];
  bike?: Bike;
}

export interface TicketCreateRequest {
  problem_description: string;
  diagnosis?: string;
  priority: TicketPriority;
  bike_id: string;
  technician_id?: string;
  labor_cost?: number;
  estimated_completion?: string;
}

export interface TicketUpdateRequest {
  problem_description?: string;
  diagnosis?: string;
  status?: TicketStatus;
  priority?: TicketPriority;
  estimated_completion?: string;
  technician_id?: string;
  labor_cost?: number;
  note?: string;
}

export interface AddPartRequest {
  part_id: string;
  quantity: number;
  price: number;
}

export interface ArchiveRequest {
  note?: string;
}

// Ticket service functions
export const ticketService = {
  /**
   * Get all tickets
   */
  getTickets: async (skip = 0, limit = 100): Promise<Ticket[]> => {
    const tickets = await apiClient.get<Ticket[]>(`/tickets/?skip=${skip}&limit=${limit}`);
    // Calculate total for each ticket
    return tickets.map(ticket => ({
      ...ticket,
      total: ticket.labor_cost + ticket.total_parts_cost
    }));
  },

  /**
   * Get ticket by ID
   */
  getTicket: async (id: string): Promise<TicketWithDetails> => {
    const ticket = await apiClient.get<TicketWithDetails>(`/tickets/${id}`);
    return {
      ...ticket,
      total: ticket.labor_cost + ticket.total_parts_cost
    };
  },

  /**
   * Create a new ticket
   */
  createTicket: async (ticket: TicketCreateRequest): Promise<Ticket> => {
    return apiClient.post<Ticket>('/tickets/', ticket);
  },

  /**
   * Update an existing ticket
   */
  updateTicket: async (id: string, ticket: TicketUpdateRequest): Promise<Ticket> => {
    return apiClient.put<Ticket>(`/tickets/${id}`, ticket);
  },

  /**
   * Delete a ticket
   */
  deleteTicket: async (id: string): Promise<void> => {
    return apiClient.delete<void>(`/tickets/${id}`);
  },

  /**
   * Add a part to a ticket
   */
  addPart: async (ticketId: string, part: AddPartRequest): Promise<TicketPart> => {
    return apiClient.post<TicketPart>(`/tickets/${ticketId}/parts`, part);
  },

  /**
   * Remove a part from a ticket
   */
  removePart: async (ticketId: string, partId: string): Promise<void> => {
    return apiClient.delete<void>(`/tickets/${ticketId}/parts/${partId}`);
  },

  /**
   * Update a part on a ticket
   */
  updatePart: async (ticketId: string, partId: string, quantity: number, price: number): Promise<TicketPart> => {
    return apiClient.put<TicketPart>(`/tickets/${ticketId}/parts/${partId}`, { quantity, price });
  },

  /**
   * Add a status update to a ticket
   */
  addStatusUpdate: async (ticketId: string, status: TicketStatus, note: string): Promise<TicketUpdate> => {
    return apiClient.post<TicketUpdate>(`/tickets/${ticketId}/updates`, { status, note });
  },

  /**
   * Get status updates for a ticket
   */
  getStatusUpdates: async (ticketId: string): Promise<TicketUpdate[]> => {
    return apiClient.get<TicketUpdate[]>(`/tickets/${ticketId}/updates`);
  },

  /**
   * Archive a ticket
   */
  archiveTicket: async (ticketId: string, data: ArchiveRequest = {}): Promise<Ticket> => {
    return apiClient.patch<Ticket>(`/tickets/${ticketId}/archive`, data);
  },

  /**
   * Unarchive (restore) a ticket
   */
  unarchiveTicket: async (ticketId: string, data: ArchiveRequest = {}): Promise<Ticket> => {
    return apiClient.patch<Ticket>(`/tickets/${ticketId}/unarchive`, data);
  },

  /**
   * Get all tickets including archives
   */
  getArchivedTickets: async (skip = 0, limit = 100): Promise<Ticket[]> => {
    const tickets = await apiClient.get<Ticket[]>(`/tickets/?skip=${skip}&limit=${limit}&archived=true`);
    // Calculate total for each ticket
    return tickets.map(ticket => ({
      ...ticket,
      total: ticket.labor_cost + ticket.total_parts_cost
    }));
  }
};

export default ticketService;