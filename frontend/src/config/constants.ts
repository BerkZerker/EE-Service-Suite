// API Configuration
export const API_BASE_URL = '/api';

// Authentication
export const AUTH_TOKEN_KEY = 'auth_tokens';
export const ACCESS_TOKEN_EXPIRE_MINUTES = 30;

// Pagination
export const DEFAULT_PAGE_SIZE = 25;
export const DEFAULT_PAGE = 1;

// Status values
export const TICKET_STATUS = {
  INTAKE: 'intake',
  DIAGNOSIS: 'diagnosis',
  AWAITING_PARTS: 'awaiting_parts',
  IN_PROGRESS: 'in_progress',
  COMPLETE: 'complete',
  DELIVERED: 'delivered',
} as const;

export type TicketStatus = typeof TICKET_STATUS[keyof typeof TICKET_STATUS];

export const TICKET_STATUS_LABELS: Record<TicketStatus, string> = {
  [TICKET_STATUS.INTAKE]: 'Intake',
  [TICKET_STATUS.DIAGNOSIS]: 'Diagnosis',
  [TICKET_STATUS.AWAITING_PARTS]: 'Awaiting Parts',
  [TICKET_STATUS.IN_PROGRESS]: 'In Progress',
  [TICKET_STATUS.COMPLETE]: 'Complete',
  [TICKET_STATUS.DELIVERED]: 'Delivered',
};

export const PRIORITY_LEVELS = {
  LOW: 'low',
  MEDIUM: 'medium',
  HIGH: 'high',
  URGENT: 'urgent',
} as const;

export type PriorityLevel = typeof PRIORITY_LEVELS[keyof typeof PRIORITY_LEVELS];

export const PRIORITY_LEVEL_LABELS: Record<PriorityLevel, string> = {
  [PRIORITY_LEVELS.LOW]: 'Low',
  [PRIORITY_LEVELS.MEDIUM]: 'Medium',
  [PRIORITY_LEVELS.HIGH]: 'High',
  [PRIORITY_LEVELS.URGENT]: 'Urgent',
};

export const PRIORITY_LEVEL_COLORS: Record<PriorityLevel, string> = {
  [PRIORITY_LEVELS.LOW]: 'bg-gray-500',
  [PRIORITY_LEVELS.MEDIUM]: 'bg-blue-500',
  [PRIORITY_LEVELS.HIGH]: 'bg-yellow-500',
  [PRIORITY_LEVELS.URGENT]: 'bg-red-500',
};