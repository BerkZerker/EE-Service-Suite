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
         {/* Heading text color inherits from Card */}
        <h2 className="text-xl font-semibold">Status History</h2>
        <button 
          onClick={toggleSortOrder} 
           /* Button text color for light/dark */
          className="text-sm text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 transition-colors"
        >
          Sort: {sortOrder === 'newest' ? 'Newest First' : 'Oldest First'}
        </button>
      </div>
      
      {sortedUpdates.length > 0 ? (
        <div className="space-y-4">
          {sortedUpdates.map(update => (
             /* History item container styling for light/dark */
            <div key={update.id} className="flex items-start space-x-4 p-4 rounded-lg bg-gray-50 dark:bg-gray-800">
              {/* Status indicator color likely fine, assuming ticketStatusColors provides appropriate classes */}
              <div className={`h-8 w-8 flex-shrink-0 rounded-full ${ticketStatusColors[update.status]} flex items-center justify-center`}>
                 {/* Text color inside indicator might need adjustment depending on background */}
                <span className="text-xs font-bold text-white">{update.status.charAt(0).toUpperCase()}</span>
              </div>
              <div className="flex-grow">
                <div className="flex justify-between">
                   {/* Status text color for light/dark */}
                  <h4 className="text-gray-900 dark:text-white font-medium">
                    {update.status.charAt(0).toUpperCase() + update.status.slice(1)}
                  </h4>
                   {/* Date text color for light/dark */}
                  <span className="text-sm text-gray-500 dark:text-gray-400">{formatDate(update.created_at)}</span>
                </div>
                 {/* Note text color for light/dark */}
                <p className="text-gray-700 dark:text-gray-300 mt-1">{update.note}</p>
                 {/* User text color for light/dark */}
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
                  By: {update.user_name || 'Unknown'}
                </p>
              </div>
            </div>
          ))}
        </div>
      ) : (
         /* Placeholder styling for light/dark */
        <div className="bg-gray-50 dark:bg-gray-800 rounded p-4 text-center">
          <p className="text-gray-500 dark:text-gray-400">No status updates for this ticket</p>
        </div>
      )}
    </Card>
  );
};

export default StatusHistory;
