import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { TicketForm } from '../components/tickets';
import { ticketService } from '../services';
import { type TicketCreateRequest } from '../services/ticket-service';

const CreateTicket: React.FC = () => {
  const navigate = useNavigate();
  const [error, setError] = useState('');
  
  // Cast to handle the form prop type requirement
  const handleSubmit = async (ticketData: TicketCreateRequest | any) => {
    // We know this is always a TicketCreateRequest when creating
    try {
      const newTicket = await ticketService.createTicket(ticketData);
      // Redirect to ticket detail page
      navigate(`/tickets/${newTicket.id}`);
    } catch (err) {
      console.error('Error creating ticket:', err);
      setError('Failed to create ticket. Please try again.');
    }
  };
  
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Create New Service Ticket</h1>
        <p className="text-gray-400">Fill out the form below to create a new service ticket</p>
        {error && <p className="mt-2 text-red-500">{error}</p>}
      </div>
      
      <TicketForm onSubmit={handleSubmit} />
    </div>
  );
};

export default CreateTicket;