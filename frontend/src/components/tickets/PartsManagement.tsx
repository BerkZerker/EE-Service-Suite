import React, { useState } from 'react';
import { TicketPart, AddPartRequest } from '../../services/ticket-service';
import { ticketService } from '../../services';
import { Card, Button } from '../ui';
import { formatCurrency } from '../../utils/ticketUtils';
import PartsSelector from './PartsSelector';

interface SelectedPart {
  part_id: string;
  part_name: string;
  quantity: number;
  price: number;
}

interface PartsManagementProps {
  ticketId: string;
  parts: TicketPart[];
  laborCost: number;
  onPartsUpdated: () => void;
  className?: string;
}

const PartsManagement: React.FC<PartsManagementProps> = ({
  ticketId,
  parts,
  laborCost,
  onPartsUpdated,
  className = '',
}) => {
  const [addingParts, setAddingParts] = useState(false);
  const [selectedParts, setSelectedParts] = useState<SelectedPart[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Calculate total costs
  const totalPartsCost = parts.reduce(
    (total, { quantity, price }) => total + quantity * price,
    0
  );
  const totalCost = totalPartsCost + laborCost;
  
  const handleAddParts = async () => {
    if (!selectedParts.length) {
      setError('Please select at least one part to add');
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      // Add each selected part to the ticket
      for (const part of selectedParts) {
        const request: AddPartRequest = {
          part_id: part.part_id,
          quantity: part.quantity,
          price: part.price,
        };
        
        await ticketService.addPart(ticketId, request);
      }
      
      // Clear selected parts and hide the add form
      setSelectedParts([]);
      setAddingParts(false);
      
      // Refresh ticket data
      onPartsUpdated();
    } catch (err) {
      console.error('Error adding parts to ticket:', err);
      setError('Failed to add parts to the ticket');
    } finally {
      setLoading(false);
    }
  };
  
  const handleRemovePart = async (partId: string) => {
    try {
      await ticketService.removePart(ticketId, partId);
      onPartsUpdated();
    } catch (err) {
      console.error('Error removing part:', err);
      setError('Failed to remove part from the ticket');
    }
  };
  
  return (
    <Card className={className}>
      <div className="flex justify-between items-center mb-4">
        {/* Heading text color inherits from Card */}
        <h2 className="text-xl font-semibold">Parts & Labor</h2>
        {!addingParts && (
          <Button
            size="sm"
            onClick={() => setAddingParts(true)}
          >
            Add Parts
          </Button>
        )}
      </div>
      
      {error && (
        // Error message styling for light/dark
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4 dark:bg-red-900/50 dark:border-red-700 dark:text-red-100">
          {error}
        </div>
      )}
      
      {/* Add Parts Form */}
      {addingParts && (
        // Section border for light/dark
        <div className="mb-6 p-4 border border-gray-200 rounded-lg dark:border-gray-700">
          <div className="flex justify-between items-center mb-4">
             {/* Heading text color inherits */}
            <h3 className="text-lg font-medium">Add Parts</h3>
            <Button
              size="sm"
              variant="outline"
              onClick={() => {
                setAddingParts(false);
                setSelectedParts([]);
              }}
            >
              Cancel
            </Button>
          </div>
          
          <PartsSelector
            selectedParts={[]}
            onPartsChange={(parts) => {
              // Transform Parts from PartsSelector to our local SelectedPart format
              const transformedParts = parts.map(p => ({
                part_id: p.part.id,
                part_name: p.part.name,
                quantity: p.quantity,
                price: p.price
              }));
              setSelectedParts(transformedParts);
            }}
          />
          
          <div className="flex justify-end mt-4">
            <Button
              onClick={handleAddParts}
              isLoading={loading}
              disabled={selectedParts.length === 0}
            >
              Add Selected Parts
            </Button>
          </div>
        </div>
      )}
      
      {/* Parts Table */}
      {parts.length > 0 ? (
        <div className="overflow-x-auto">
           {/* Table divider color for light/dark */}
          <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead>
              <tr>
                 {/* Table header text color for light/dark */}
                <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider dark:text-gray-400">Part</th>
                <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider dark:text-gray-400">Quantity</th>
                <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider dark:text-gray-400">Price</th>
                <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider dark:text-gray-400">Total</th>
                <th className="px-3 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider dark:text-gray-400"></th>
              </tr>
            </thead>
             {/* Table body divider color for light/dark */}
            <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
              {parts.map(part => (
                <tr key={part.id}>
                   {/* Table cell text color for light/dark */}
                  <td className="px-3 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">{part.part_name}</td>
                  <td className="px-3 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-300">{part.quantity}</td>
                  <td className="px-3 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-300">{formatCurrency(part.price)}</td>
                  <td className="px-3 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-300">{formatCurrency(part.price * part.quantity)}</td>
                  <td className="px-3 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button
                      onClick={() => handleRemovePart(part.part_id)}
                       // Remove button text color already theme-aware (red)
                      className="text-red-500 hover:text-red-400 transition-colors"
                    >
                      Remove
                    </button>
                  </td>
                </tr>
              ))}
              {/* Labor row */}
              <tr>
                 {/* Table cell text color for light/dark */}
                <td className="px-3 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">Labor</td>
                <td className="px-3 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-300">-</td>
                <td className="px-3 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-300">-</td>
                <td className="px-3 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-300">{formatCurrency(laborCost)}</td>
                <td></td>
              </tr>
            </tbody>
            <tfoot>
              <tr>
                 {/* Table footer text color for light/dark */}
                <td colSpan={3} className="px-3 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white text-right">Total</td>
                <td className="px-3 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">{formatCurrency(totalCost)}</td>
                <td></td>
              </tr>
            </tfoot>
          </table>
        </div>
      ) : (
        <div className="bg-[var(--color-background)] rounded p-4 text-center">
          <p className="text-theme-text">No parts added to this ticket</p>
          <p className="text-theme-secondary text-sm mt-1">Click "Add Parts" to add parts to this ticket</p>
        </div>
      )}
    </Card>
  );
};

export default PartsManagement;
