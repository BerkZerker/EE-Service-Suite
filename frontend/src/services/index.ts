export { default as apiClient } from './api-client';
export { default as authService } from './auth-service';
export { default as customerService } from './customer-service';
export { 
  default as ticketService,
  TicketStatus,
  TicketPriority,
  type Ticket,
  type TicketWithDetails,
  type TicketCreateRequest,
  type TicketUpdateRequest,
  type TicketPart,
  type TicketUpdate
} from './ticket-service';
export { default as partService } from './part-service';