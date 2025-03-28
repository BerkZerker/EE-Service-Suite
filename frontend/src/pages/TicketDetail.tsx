import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { ticketService, customerService } from '../services';
import { TicketStatus, type TicketWithDetails } from '../services/ticket-service';
import { Spinner, Card, Button } from '../components/ui';
import { 
  StatusHistory,
  StatusUpdateForm,
  CustomerBikeInfo,
  PartsManagement
} from '../components/tickets';
import { formatDate, formatCurrency, ticketStatusColors, ticketPriorityColors } from '../utils/ticketUtils';
import { Customer } from '../services/customer-service';

const TicketDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  
  const [ticket, setTicket] = useState<TicketWithDetails | null>(null);
  const [customer, setCustomer] = useState<Customer | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  const fetchTicket = useCallback(async () => {
    if (!id) return;
    
    setLoading(true);
    setError('');
    
    try {
      const ticketData = await ticketService.getTicket(id);
      setTicket(ticketData);
      
      // If the ticket has a bike with customer_id, fetch customer
      if (ticketData.bike?.customer_id) {
        try {
          const customerData = await customerService.getCustomer(ticketData.bike.customer_id);
          setCustomer(customerData);
        } catch (err) {
          console.error('Error fetching customer:', err);
          // Don't set overall error - we can still show the ticket
        }
      }
    } catch (err) {
      console.error('Error fetching ticket:', err);
      setError('Failed to load ticket information');
    } finally {
      setLoading(false);
    }
  }, [id]);
  
  // Refresh ticket data after updates
  const handleTicketUpdated = useCallback(() => {
    fetchTicket();
  }, [fetchTicket]);
  
  useEffect(() => {
    fetchTicket();
  }, [fetchTicket]);
  
  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <Spinner size="lg" />
      </div>
    );
  }
  
  if (!ticket) {
    return (
      <div className="text-center py-12">
        <h2 className="text-xl font-medium text-red-500">Ticket not found</h2>
        <p className="mt-2 text-gray-400">The ticket you're looking for doesn't exist or was deleted</p>
        <Button 
          onClick={() => navigate('/tickets')}
          className="mt-4"
        >
          Back to Tickets
        </Button>
      </div>
    );
  }
  
  // Latest updates will be shown by the StatusHistory component
  
  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header with ticket info and actions */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6">
        <div>
          <div className="flex items-center gap-3 mb-1">
            <Link to="/tickets" className="text-blue-400 hover:text-blue-300">
              &larr; Back to Tickets
            </Link>
          </div>
          <div className="flex items-center gap-3 flex-wrap">
            <h1 className="text-2xl font-bold text-white">
              Ticket #{ticket.ticket_number}
            </h1>
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${ticketStatusColors[ticket.status]}`}>
              {ticket.status.charAt(0).toUpperCase() + ticket.status.slice(1)}
            </span>
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${ticketPriorityColors[ticket.priority]}`}>
              {ticket.priority.charAt(0).toUpperCase() + ticket.priority.slice(1)}
            </span>
          </div>
          <p className="text-gray-400 mt-1">Created: {formatDate(ticket.created_at)}</p>
          {error && <p className="mt-2 text-red-500">{error}</p>}
        </div>
        
        <div className="flex mt-4 md:mt-0 space-x-3">
          <Link to={`/tickets/${ticket.id}/edit`}>
            <Button size="sm">
              Edit Ticket
            </Button>
          </Link>
        </div>
      </div>
      
      {/* Main Content - 2 column layout on larger screens */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          {/* Ticket Overview Card */}
          <Card>
            <h2 className="text-xl font-semibold text-white mb-4">Ticket Details</h2>
            
            <div className="space-y-4">
              <div>
                <h3 className="text-sm font-medium text-gray-400 mb-1">Problem Description</h3>
                <p className="text-white whitespace-pre-line">{ticket.problem_description}</p>
              </div>
              
              {ticket.diagnosis && (
                <div>
                  <h3 className="text-sm font-medium text-gray-400 mb-1">Diagnosis</h3>
                  <p className="text-white whitespace-pre-line">{ticket.diagnosis}</p>
                </div>
              )}
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <h3 className="text-sm font-medium text-gray-400 mb-1">Estimated Completion</h3>
                  <p className="text-white">
                    {ticket.estimated_completion 
                      ? formatDate(ticket.estimated_completion)
                      : 'Not specified'}
                  </p>
                </div>
                
                <div>
                  <h3 className="text-sm font-medium text-gray-400 mb-1">Technician</h3>
                  <p className="text-white">
                    {ticket.technician_id 
                      ? `ID: ${ticket.technician_id}` // You'll need to fetch the technician name in a real implementation
                      : 'Not assigned'}
                  </p>
                </div>
              </div>
            </div>
          </Card>
          
          {/* Customer & Bike Information Component */}
          <CustomerBikeInfo 
            customer={customer}
            bike={ticket.bike}
            className="mb-6"
          />
          
          {/* Parts Management Component */}
          <PartsManagement
            ticketId={ticket.id}
            parts={ticket.parts || []}
            laborCost={ticket.labor_cost}
            onPartsUpdated={handleTicketUpdated}
          />
        </div>
        
        <div className="space-y-6">
          {/* Status Update Form Component */}
          <StatusUpdateForm
            ticketId={ticket.id}
            currentStatus={ticket.status}
            onStatusUpdated={handleTicketUpdated}
          />
          
          {/* Ticket Summary */}
          <Card>
            <h2 className="text-xl font-semibold text-white mb-4">Ticket Summary</h2>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-gray-400">Parts Total:</span>
                <span className="text-white">{formatCurrency(ticket.total_parts_cost)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Labor Cost:</span>
                <span className="text-white">{formatCurrency(ticket.labor_cost)}</span>
              </div>
              <div className="flex justify-between pt-2 border-t border-gray-700">
                <span className="font-medium text-white">Total:</span>
                <span className="font-medium text-white">{formatCurrency(ticket.total)}</span>
              </div>
            </div>
          </Card>
          
          {/* Quick Actions */}
          <Card>
            <h2 className="text-xl font-semibold text-white mb-4">Actions</h2>
            <div className="space-y-3">
              <Button variant="outline" className="w-full justify-start" onClick={() => navigate(`/tickets/${ticket.id}/edit`)}>
                <span className="mr-2">✏️</span> Edit Ticket
              </Button>
              <Button variant="outline" className="w-full justify-start">
                <span className="mr-2">📁</span> Archive Ticket
              </Button>
              <Button variant="outline" className="w-full justify-start">
                <span className="mr-2">🖨️</span> Print Ticket
              </Button>
              {ticket.status === TicketStatus.COMPLETE && (
                <Button variant="outline" className="w-full justify-start">
                  <span className="mr-2">✓</span> Mark as Delivered
                </Button>
              )}
            </div>
          </Card>
          
          {/* Status History Component */}
          <StatusHistory
            updates={ticket.updates || []}
          />
        </div>
      </div>
    </div>
  );
};

export default TicketDetail;