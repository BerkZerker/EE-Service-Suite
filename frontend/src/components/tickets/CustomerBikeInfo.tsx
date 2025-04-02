import React, { useState, useEffect } from 'react';
import { Card, Spinner } from '../ui';
import { type Customer } from '../../services/customer-service';
import { type Bike } from '../../services/customer-service';
import { customerService } from '../../services';

interface CustomerBikeInfoProps {
  customer?: Customer | null;
  bike?: Bike | null;
  bikeId?: string;
  className?: string;
}

const CustomerBikeInfo: React.FC<CustomerBikeInfoProps> = ({
  customer: propCustomer,
  bike: propBike,
  bikeId,
  className = '',
}) => {
  const [bike, setBike] = useState<Bike | null>(propBike || null);
  const [customer, setCustomer] = useState<Customer | null>(propCustomer || null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  useEffect(() => {
    // If we already have props data, use it
    if (propBike) setBike(propBike);
    if (propCustomer) setCustomer(propCustomer);
    
    // If we have a bikeId but no bike data, fetch it
    const fetchData = async () => {
      if (!bikeId || propBike) return;
      
      setLoading(true);
      setError('');
      
      try {
        // Fetch bike data
        const bikeData = await customerService.getBike(bikeId);
        setBike(bikeData);
        
        // If the bike has a customer_id, fetch the customer data
        if (bikeData.customer_id) {
          const customerData = await customerService.getCustomer(bikeData.customer_id);
          setCustomer(customerData);
        }
      } catch (err) {
        console.error('Error fetching bike/customer data:', err);
        setError('Failed to load bike or customer information');
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, [bikeId, propBike, propCustomer]);
  
  if (loading) {
    return (
      <Card className={className}>
        <div className="flex justify-center items-center py-8">
          <Spinner size="md" />
        </div>
      </Card>
    );
  }
  
  if (!bike && !customer) {
    return (
      <Card className={className}>
        <div className="text-center py-6">
           {/* Placeholder text color for light/dark */}
          <p className="text-gray-500 dark:text-gray-400">No customer or bike information available</p>
        </div>
      </Card>
    );
  }
  
  return (
    <Card className={className}>
       {/* Heading text color inherits from Card */}
      <h2 className="text-xl font-semibold mb-4">Customer & Bike Information</h2>
      
      {error ? (
         /* Error message styling for light/dark */
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded dark:bg-red-900/50 dark:border-red-700 dark:text-red-100">
          {error}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-4">
          {/* Bike Information */}
          <div>
             {/* Sub-heading text color for light/dark */}
            <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Bike Details</h3>
            {bike ? (
              <div className="mt-2">
                 {/* Main text color inherits from Card */}
                <p>{bike.make} {bike.model}</p>
                 {/* Secondary text color for light/dark */}
                {bike.serial_number && <p className="text-sm text-gray-600 dark:text-gray-300">Serial Number: {bike.serial_number}</p>}
                {bike.purchase_date && (
                  <p className="text-sm text-gray-600 dark:text-gray-300">
                    Purchase Date: {new Date(bike.purchase_date).toLocaleDateString()}
                  </p>
                )}
              </div>
            ) : (
               /* Placeholder text color for light/dark */
              <p className="mt-1 text-gray-500 dark:text-gray-400">Bike information not available</p>
            )}
          </div>
          
          {/* Customer Information */}
          <div>
             {/* Sub-heading text color for light/dark */}
            <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Customer Details</h3>
            {customer ? (
              <div className="mt-2">
                 {/* Main text color inherits from Card */}
                <p>{customer.full_name}</p>
                 {/* Secondary text color for light/dark */}
                <p className="text-sm text-gray-600 dark:text-gray-300">{customer.email}</p>
                <p className="text-sm text-gray-600 dark:text-gray-300">{customer.phone}</p>
                {customer.address && <p className="text-sm text-gray-600 dark:text-gray-300">{customer.address}</p>}
              </div>
            ) : (
               /* Placeholder text color for light/dark */
              <p className="mt-1 text-gray-500 dark:text-gray-400">Customer information not available</p>
            )}
          </div>
        </div>
      )}
    </Card>
  );
};

export default CustomerBikeInfo;
