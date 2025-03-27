import React, { useState, useEffect } from 'react';
import { 
  Card,
  FormGroup,
  Button,
  Input,
  TextArea,
  Select,
  DatePicker,
  RadioGroup
} from '../ui';
import CustomerSelector from './CustomerSelector';
import BikeSelector from './BikeSelector';
import PartsSelector, { SelectedPart } from './PartsSelector';
import { Customer, Bike, ticketService } from '../../services';
import {
  TicketStatus,
  TicketPriority,
  type Ticket,
  type TicketCreateRequest,
  type TicketUpdateRequest
} from '../../services/ticket-service';

interface TicketFormProps {
  ticket?: Ticket;
  onSubmit: (ticketData: TicketCreateRequest | TicketUpdateRequest) => Promise<void>;
  isEditing?: boolean;
  className?: string;
}

export const TicketForm: React.FC<TicketFormProps> = ({
  ticket,
  onSubmit,
  isEditing = false,
  className = '',
}) => {
  // Customer and bike state
  const [selectedCustomer, setSelectedCustomer] = useState<Customer | null>(null);
  const [selectedBike, setSelectedBike] = useState<Bike | null>(null);
  
  // Ticket details state
  const [problemDescription, setProblemDescription] = useState('');
  const [diagnosis, setDiagnosis] = useState('');
  const [priority, setPriority] = useState<TicketPriority>(TicketPriority.MEDIUM);
  const [status, setStatus] = useState<TicketStatus>(TicketStatus.INTAKE);
  const [estimatedCompletionDate, setEstimatedCompletionDate] = useState('');
  const [laborCost, setLaborCost] = useState('0.00');
  
  // Parts state
  const [selectedParts, setSelectedParts] = useState<SelectedPart[]>([]);
  
  // Form state
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
  
  // Priority options with descriptions
  const priorityOptions = [
    { 
      value: TicketPriority.LOW, 
      label: 'Low', 
      description: 'No rush, can be worked on when convenient' 
    },
    { 
      value: TicketPriority.MEDIUM, 
      label: 'Medium',
      description: 'Standard turnaround time' 
    },
    { 
      value: TicketPriority.HIGH, 
      label: 'High',
      description: 'Customer needs this soon, prioritize this work' 
    },
    { 
      value: TicketPriority.URGENT, 
      label: 'Urgent',
      description: 'Drop everything, customer waiting or special situation' 
    },
  ];

  // Load ticket data if editing
  useEffect(() => {
    if (isEditing && ticket) {
      setProblemDescription(ticket.problem_description);
      setDiagnosis(ticket.diagnosis || '');
      setPriority(ticket.priority);
      setStatus(ticket.status);
      setEstimatedCompletionDate(ticket.estimated_completion || '');
      setLaborCost(ticket.labor_cost.toString());
      
      // Need to fetch customer and bike details separately
      // This would normally come from the API when loading a ticket
    }
  }, [isEditing, ticket]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!selectedBike && !isEditing) {
      setError('Please select a bike');
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      // Prepare form data
      const formData: TicketCreateRequest | TicketUpdateRequest = {
        problem_description: problemDescription,
        diagnosis: diagnosis || undefined,
        priority,
        ...(isEditing ? { status } : {}),
        estimated_completion: estimatedCompletionDate || undefined,
        labor_cost: parseFloat(laborCost) || 0,
      };
      
      // If creating new ticket, bike ID is required
      if (!isEditing && selectedBike) {
        (formData as TicketCreateRequest).bike_id = selectedBike.id;
      }
      
      // Submit form
      await onSubmit(formData);
      
      // Handle selected parts in a separate call if needed
      // This would depend on your API design
    } catch (err) {
      console.error('Error submitting ticket:', err);
      setError('Failed to submit ticket');
    } finally {
      setLoading(false);
    }
  };

  // Calculate total cost (parts + labor)
  const totalPartsCost = selectedParts.reduce(
    (total, { quantity, price }) => total + quantity * price,
    0
  );
  const totalCost = totalPartsCost + (parseFloat(laborCost) || 0);

  return (
    <form onSubmit={handleSubmit} className={className}>
      <Card className="mb-6">
        <FormGroup title="Customer & Bike Information">
          <div className="space-y-4">
            <CustomerSelector
              onCustomerSelect={setSelectedCustomer}
              selectedCustomer={selectedCustomer}
            />
            
            <BikeSelector
              customerId={selectedCustomer?.id}
              onBikeSelect={setSelectedBike}
              selectedBike={selectedBike}
            />
          </div>
        </FormGroup>
      </Card>
      
      <Card className="mb-6">
        <FormGroup title="Ticket Details">
          <TextArea
            label="Problem Description"
            value={problemDescription}
            onChange={(e) => setProblemDescription(e.target.value)}
            placeholder="Describe the problem or service needed"
            rows={3}
            required
          />
          
          <TextArea
            label="Diagnosis"
            value={diagnosis}
            onChange={(e) => setDiagnosis(e.target.value)}
            placeholder="Technical assessment (can be filled later)"
            rows={3}
          />
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {isEditing && (
              <Select
                label="Status"
                options={statusOptions}
                value={status}
                onChange={(value) => setStatus(value as TicketStatus)}
              />
            )}
            
            <RadioGroup
              label="Priority"
              name="priority"
              options={priorityOptions}
              value={priority}
              onChange={(value) => setPriority(value as TicketPriority)}
              className="md:col-span-2"
            />
            
            <DatePicker
              label="Estimated Completion Date"
              value={estimatedCompletionDate}
              onChange={setEstimatedCompletionDate}
            />
            
            <Input
              label="Labor Cost"
              type="number"
              min="0"
              step="0.01"
              value={laborCost}
              onChange={(e) => setLaborCost(e.target.value)}
              leftIcon={<span className="text-gray-400">$</span>}
            />
          </div>
        </FormGroup>
      </Card>
      
      <Card className="mb-6">
        <FormGroup title="Parts">
          <PartsSelector
            selectedParts={selectedParts}
            onPartsChange={setSelectedParts}
          />
        </FormGroup>
      </Card>
      
      <Card>
        <div className="flex justify-between items-center">
          <div>
            <h3 className="text-lg font-medium text-white">Ticket Total</h3>
            <div className="mt-2 space-y-1">
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Parts:</span>
                <span className="text-white">${totalPartsCost.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Labor:</span>
                <span className="text-white">${(parseFloat(laborCost) || 0).toFixed(2)}</span>
              </div>
              <div className="flex justify-between font-medium pt-1 border-t border-gray-700">
                <span>Total:</span>
                <span>${totalCost.toFixed(2)}</span>
              </div>
            </div>
          </div>
          
          <div className="flex space-x-3">
            <Button
              variant="outline"
              type="button"
            >
              Cancel
            </Button>
            <Button
              type="submit"
              isLoading={loading}
            >
              {isEditing ? 'Update' : 'Create'} Ticket
            </Button>
          </div>
        </div>
        
        {error && <p className="mt-4 text-red-500">{error}</p>}
      </Card>
    </form>
  );
};

export default TicketForm;