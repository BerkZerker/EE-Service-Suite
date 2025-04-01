import React, { useState } from 'react';
import { TicketStatus } from '../../services/ticket-service';
import { ticketService } from '../../services';
import { Select, TextArea, Button, Card } from '../ui';

interface StatusUpdateFormProps {
  ticketId: string;
  currentStatus: TicketStatus;
  onStatusUpdated: () => void;
  className?: string;
}

const StatusUpdateForm: React.FC<StatusUpdateFormProps> = ({
  ticketId,
  currentStatus,
  onStatusUpdated,
  className = '',
}) => {
  const [status, setStatus] = useState<TicketStatus>(currentStatus);
  const [note, setNote] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Status options
  const statusOptions = [
    { value: TicketStatus.INTAKE, label: 'Intake' },
    { value: TicketStatus.DIAGNOSIS, label: 'Diagnosis' },
    { value: TicketStatus.AWAITING_PARTS, label: 'Awaiting Parts' },
    { value: TicketStatus.IN_PROGRESS, label: 'In Progress' },
    { value: TicketStatus.COMPLETE, label: 'Complete' },
    { value: TicketStatus.DELIVERED, label: 'Delivered' },
  ];
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!note.trim()) {
      setError('Please provide a note for this status update');
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      await ticketService.addStatusUpdate(ticketId, status, note);
      setNote('');
      onStatusUpdated();
    } catch (err) {
      console.error('Error updating status:', err);
      setError('Failed to update ticket status');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <Card className={className}>
       {/* Heading text color inherits from Card */}
      <h2 className="text-xl font-semibold mb-4">Update Status</h2>
      
      <form onSubmit={handleSubmit}>
        <div className="space-y-4">
          <Select
            label="Status"
            options={statusOptions}
            value={status}
            onChange={(value) => setStatus(value as TicketStatus)}
          />
          
          <TextArea
            label="Update Note"
            value={note}
            onChange={(e) => setNote(e.target.value)}
            placeholder="Provide details about this status change..."
            rows={3}
            required
          />
          
          {error && <p className="text-red-500">{error}</p>}
          
          <div className="flex justify-end">
            <Button
              type="submit"
              isLoading={loading}
              disabled={status === currentStatus && !note.trim()}
            >
              Add Update
            </Button>
          </div>
        </div>
      </form>
    </Card>
  );
};

export default StatusUpdateForm;
