/**
 * Generate a random ticket number in the format EE-YYYY-XXXXX
 * where YYYY is the current year and XXXXX is a random 5-digit number
 */
export function generateTicketNumber(): string {
  const year = new Date().getFullYear();
  const randomNum = Math.floor(10000 + Math.random() * 90000); // 5-digit number
  return `EE-${year}-${randomNum}`;
}

/**
 * Format a timestamp string as a readable date
 */
export function formatDate(dateString: string | null | undefined): string {
  if (!dateString) return 'N/A';
  
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
}

/**
 * Format a currency value as USD
 */
export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(amount);
}

export const ticketStatusColors: Record<string, string> = {
  intake: 'bg-blue-600 text-white',
  diagnosis: 'bg-purple-600 text-white',
  awaiting_parts: 'bg-yellow-500 text-black',
  in_progress: 'bg-orange-500 text-white',
  complete: 'bg-green-600 text-white',
  delivered: 'bg-gray-500 text-white',
};

export const ticketPriorityColors: Record<string, string> = {
  low: 'bg-gray-600 text-white',
  medium: 'bg-blue-600 text-white',
  high: 'bg-orange-500 text-white',
  urgent: 'bg-red-600 text-white',
};