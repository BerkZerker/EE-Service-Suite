import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ticketService } from '../services';
import { TicketStatus, TicketPriority, type Ticket } from '../services/ticket-service';
import { Card, Button, Spinner, Select } from '../components/ui'; // Remove ToggleSwitch import
import { formatDate, formatCurrency, ticketStatusColors, ticketPriorityColors, archivedTicketStyles } from '../utils/ticketUtils';

const TicketList: React.FC = () => {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [isArchiving, setIsArchiving] = useState<string | null>(null);
  
  // Filtering state
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [priorityFilter, setPriorityFilter] = useState<string>('all');
  const [showArchived, setShowArchived] = useState<boolean>(false);
  
  const statusOptions = [
    { value: 'all', label: 'All Statuses' },
    { value: TicketStatus.INTAKE, label: 'Intake' },
    { value: TicketStatus.DIAGNOSIS, label: 'Diagnosis' },
    { value: TicketStatus.AWAITING_PARTS, label: 'Awaiting Parts' },
    { value: TicketStatus.IN_PROGRESS, label: 'In Progress' },
    { value: TicketStatus.COMPLETE, label: 'Complete' },
    { value: TicketStatus.DELIVERED, label: 'Delivered' },
  ];
  
  const priorityOptions = [
    { value: 'all', label: 'All Priorities' },
    { value: TicketPriority.LOW, label: 'Low' },
    { value: TicketPriority.MEDIUM, label: 'Medium' },
    { value: TicketPriority.HIGH, label: 'High' },
    { value: TicketPriority.URGENT, label: 'Urgent' },
  ];
  
  useEffect(() => {
    const fetchTickets = async () => {
      setLoading(true);
      setError('');
      
      try {
        if (showArchived) {
          const ticketList = await ticketService.getArchivedTickets();
          setTickets(ticketList);
        } else {
          const ticketList = await ticketService.getTickets();
          setTickets(ticketList);
        }
      } catch (err) {
        console.error('Error fetching tickets:', err);
        setError('Failed to load tickets');
      } finally {
        setLoading(false);
      }
    };
    
    fetchTickets();
  }, [showArchived]);
  
  const filteredTickets = tickets.filter(ticket => {
    let statusMatch = true;
    let priorityMatch = true;
    
    if (statusFilter !== 'all') {
      statusMatch = ticket.status === statusFilter;
    }
    
    if (priorityFilter !== 'all') {
      priorityMatch = ticket.priority === priorityFilter;
    }
    
    return statusMatch && priorityMatch;
  });
  
  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <Spinner size="lg" />
      </div>
    );
  }
  
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold text-text-primary">Service Tickets</h1>
          <p className="text-text-secondary">Manage customer service tickets</p>
        </div>
        <Link to="/tickets/new">
          <Button>Create New Ticket</Button>
        </Link>
      </div>
      
      {error && (
        <div className="bg-red-900/50 border border-red-700 text-red-100 px-4 py-3 rounded mb-6">
          {error}
        </div>
      )}
      
      <Card className="mb-6">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1">
            <Select
              className="w-full"
              label="Filter by Status"
              options={statusOptions}
              value={statusFilter}
              onChange={setStatusFilter}
            />
          </div>
          <div className="flex-1">
            <Select
              className="w-full"
              label="Filter by Priority"
              options={priorityOptions}
              value={priorityFilter}
              onChange={setPriorityFilter}
            />
          </div>
          <div className="flex items-end"> {/* Removed md:items-center to align button baseline */}
            <Button
              // Use default primary styling by removing variant="outline"
              onClick={() => setShowArchived(!showArchived)}
            >
              {showArchived ? 'View Active' : 'View Archived'}
            </Button>
          </div>
        </div>
      </Card>
      
      <div className="space-y-4">
        {filteredTickets.length === 0 ? (
          <div className="card text-center"> {/* Use the .card component class */}
            <h3 className="text-lg font-medium text-text-primary mb-2">No Tickets Found</h3>
            <p className="text-text-secondary mb-4">
              {tickets.length === 0
                ? 'There are no service tickets in the system.'
                : 'No tickets match your current filters.'}
            </p>
            {tickets.length > 0 && (
              <Button
                variant="outline"
                onClick={() => {
                  setStatusFilter('all');
                  setPriorityFilter('all');
                }}
              >
                Clear Filters
              </Button>
            )}
          </div>
        ) : (
          filteredTickets.map(ticket => {
            const handleArchiveToggle = async () => {
              setIsArchiving(ticket.id);
              try {
                if (ticket.is_archived) {
                  // Unarchive
                  await ticketService.unarchiveTicket(ticket.id);
                } else {
                  // Archive
                  await ticketService.archiveTicket(ticket.id);
                }
                // Reload tickets
                const newTickets = showArchived 
                  ? await ticketService.getArchivedTickets()
                  : await ticketService.getTickets();
                setTickets(newTickets);
              } catch (err) {
                console.error('Error toggling archive state:', err);
                setError('Failed to update ticket archive status');
              } finally {
                setIsArchiving(null);
              }
            };
            
            return (
              <Card 
                key={ticket.id} 
                className={`transition-transform hover:scale-[1.01] ${ticket.is_archived ? archivedTicketStyles.card : ''}`}
              >
                <div className="flex flex-col md:flex-row justify-between gap-4">
                  <div>
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-lg font-medium text-text-primary">
                        Ticket #{ticket.ticket_number}
                      </h3>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${ticketStatusColors[ticket.status]}`}>
                        {ticket.status.charAt(0).toUpperCase() + ticket.status.slice(1)}
                      </span>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${ticketPriorityColors[ticket.priority]}`}>
                        {ticket.priority.charAt(0).toUpperCase() + ticket.priority.slice(1)}
                      </span>
                      {ticket.is_archived && (
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${archivedTicketStyles.badge}`}>
                          Archived
                        </span>
                      )}
                    </div>
                    <p className="text-text-secondary mb-2 line-clamp-2">{ticket.problem_description}</p>
                    <div className="text-sm text-text-secondary">
                      Created: {formatDate(ticket.created_at)}
                      {ticket.estimated_completion && (
                        <span className="ml-4">
                          Est. Completion: {formatDate(ticket.estimated_completion)}
                        </span>
                      )}
                    </div>
                  </div>
                  <div className="flex flex-col items-end justify-between">
                    <div className="text-right">
                      <div className="text-lg font-medium text-text-primary">
                        {formatCurrency(ticket.total ?? 0)}
                      </div>
                      <div className="text-sm text-text-secondary">
                        Parts: {formatCurrency(ticket.total_parts_cost ?? 0)} |
                        Labor: {formatCurrency(ticket.labor_cost ?? 0)}
                      </div>
                    </div>
                    <div className="flex space-x-2 mt-3 md:mt-0">
                      <Link to={`/tickets/${ticket.id}`}>
                        <Button size="sm" variant="outline">
                          View
                        </Button>
                      </Link>
                      {!ticket.is_archived && (
                        <Link to={`/tickets/${ticket.id}/edit`}>
                          <Button size="sm">
                            Edit
                          </Button>
                        </Link>
                      )}
                      <Button 
                        size="sm" 
                        variant={ticket.is_archived ? "outline" : "subtle"}
                        onClick={handleArchiveToggle}
                        disabled={isArchiving === ticket.id}
                      >
                        {isArchiving === ticket.id ? (
                          <span className="flex items-center">
                            <Spinner size="sm" className="mr-1" />
                            Processing...
                          </span>
                        ) : (
                          ticket.is_archived ? 'Restore' : 'Archive'
                        )}
                      </Button>
                    </div>
                  </div>
                </div>
              </Card>
            );
          })
        )}
      </div>
    </div>
  );
};

export default TicketList;
