import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { TicketForm } from '../components/tickets';
import { ticketService } from '../services';
import { type TicketUpdateRequest, type Ticket } from '../services/ticket-service';
import { Spinner } from '../components/ui';

const EditTicket: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  
  const [ticket, setTicket] = useState<Ticket | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  useEffect(() => {
    const fetchTicket = async () => {
      if (!id) return;
      
      try {
        const ticketData = await ticketService.getTicket(id);
        setTicket(ticketData);
      } catch (err) {
        console.error('Error fetching ticket:', err);
        setError('Failed to load ticket information');
      } finally {
        setLoading(false);
      }
    };
    
    fetchTicket();
  }, [id]);
  
  const handleSubmit = async (ticketData: TicketUpdateRequest) => {
    if (!id) return;
    
    try {
      await ticketService.updateTicket(id, ticketData);
      // Redirect to ticket detail page
      navigate(`/tickets/${id}`);
    } catch (err) {
      console.error('Error updating ticket:', err);
      setError('Failed to update ticket. Please try again.');
    }
  };
  
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
        <button 
          onClick={() => navigate('/tickets')}
          className="mt-4 px-4 py-2 bg-primary-600 text-white rounded-md"
        >
          Back to Tickets
        </button>
      </div>
    );
  }
  
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">
          Edit Ticket #{ticket.ticket_number}
        </h1>
        <p className="text-gray-400">Update the service ticket information</p>
        {error && <p className="mt-2 text-red-500">{error}</p>}
      </div>
      
      <TicketForm 
        ticket={ticket}
        onSubmit={handleSubmit}
        isEditing
      />
    </div>
  );
};

export default EditTicket;