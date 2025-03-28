import React, { useState } from 'react';
import { TicketUpdate } from '../../services/ticket-service';
import { formatDate, ticketStatusColors } from '../../utils/ticketUtils';
import { Card } from '../ui';

interface StatusHistoryProps {
  updates: TicketUpdate[];
  className?: string;
}

const StatusHistory: React.FC<StatusHistoryProps> = ({ updates, className = '' }) => {
  const [sortOrder, setSortOrder] = useState<'newest' | 'oldest'>('newest');
  
  // Sort updates based on selected order
  const sortedUpdates = [...updates].sort((a, b) => {
    const dateA = new Date(a.created_at).getTime();
    const dateB = new Date(b.created_at).getTime();
    return sortOrder === 'newest' ? dateB - dateA : dateA - dateB;
  });

  const toggleSortOrder = () => {
    setSortOrder(sortOrder === 'newest' ? 'oldest' : 'newest');
  };

  return (
    <Card className={className}>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold text-white">Status History</h2>
        <button 
          onClick={toggleSortOrder} 
          className="text-sm text-blue-400 hover:text-blue-300 transition-colors"
        >
          Sort: {sortOrder === 'newest' ? 'Newest First' : 'Oldest First'}
        </button>
      </div>
      
      {sortedUpdates.length > 0 ? (
        <div className="space-y-4">
          {sortedUpdates.map(update => (
            <div key={update.id} className="flex items-start space-x-4 p-4 rounded-lg bg-gray-800">
              <div className={`h-8 w-8 flex-shrink-0 rounded-full ${ticketStatusColors[update.status]} flex items-center justify-center`}>
                <span className="text-xs font-bold">{update.status.charAt(0).toUpperCase()}</span>
              </div>
              <div className="flex-grow">
                <div className="flex justify-between">
                  <h4 className="text-white font-medium">
                    {update.status.charAt(0).toUpperCase() + update.status.slice(1)}
                  </h4>
                  <span className="text-sm text-gray-400">{formatDate(update.created_at)}</span>
                </div>
                <p className="text-gray-300 mt-1">{update.note}</p>
                <p className="text-sm text-gray-400 mt-2">
                  By: {update.user_name || 'Unknown'}
                </p>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-gray-800 rounded p-4 text-center">
          <p className="text-gray-400">No status updates for this ticket</p>
        </div>
      )}
    </Card>
  );
};

export default StatusHistory;