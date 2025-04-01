import React, { useState, useEffect, useCallback } from 'react';
import { customerService } from '../../services';
import { type Customer } from '../../services/customer-service';
import { Input, Button } from '../ui';
import debounce from 'lodash.debounce';

interface CustomerSelectorProps {
  onCustomerSelect: (customer: Customer) => void;
  selectedCustomer?: Customer | null;
  className?: string;
}

export const CustomerSelector: React.FC<CustomerSelectorProps> = ({
  onCustomerSelect,
  selectedCustomer,
  className = '',
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showResults, setShowResults] = useState(false);

  // Debounced search function
  const debouncedSearch = useCallback(
    debounce(async (term: string) => {
      if (!term || term.length < 2) {
        setCustomers([]);
        return;
      }

      setLoading(true);
      setError('');
      
      try {
        const results = await customerService.getCustomers();
        // Filter customers by search term (name, email, phone)
        const filtered = results.filter(customer => 
          customer.full_name.toLowerCase().includes(term.toLowerCase()) ||
          customer.email.toLowerCase().includes(term.toLowerCase()) ||
          customer.phone.includes(term)
        );
        setCustomers(filtered);
      } catch (err) {
        console.error('Error searching customers:', err);
        setError('Failed to search customers');
      } finally {
        setLoading(false);
      }
    }, 300),
    []
  );

  useEffect(() => {
    debouncedSearch(searchTerm);
    return () => {
      debouncedSearch.cancel();
    };
  }, [searchTerm, debouncedSearch]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setSearchTerm(value);
    setShowResults(true);
  };

  const handleCustomerClick = (customer: Customer) => {
    onCustomerSelect(customer);
    setShowResults(false);
    setSearchTerm('');
  };

  const handleCreateCustomer = () => {
    // This would typically open a modal or navigate to customer creation page
    console.log('Create new customer from', searchTerm);
  };

  return (
    <div className={`relative ${className}`}>
      <div className="flex gap-2">
        {selectedCustomer ? (
           /* Selected customer display styling for light/dark */
          <div className="flex-1 bg-gray-100 dark:bg-gray-700 rounded-md p-3 border border-gray-200 dark:border-gray-600">
            <div className="flex justify-between items-start">
              <div>
                 {/* Text colors for light/dark */}
                <h3 className="font-medium text-gray-900 dark:text-white">{selectedCustomer.full_name}</h3>
                <p className="text-sm text-gray-600 dark:text-gray-300">{selectedCustomer.email}</p>
                <p className="text-sm text-gray-600 dark:text-gray-300">{selectedCustomer.phone}</p>
              </div>
              <Button
                variant="ghost" /* Assuming Button component handles its own theme variants */
                size="xs"
                onClick={() => onCustomerSelect(null as unknown as Customer)}
              >
                Change
              </Button>
            </div>
          </div>
        ) : (
          <>
            <Input
              className="flex-1"
              placeholder="Search by customer name, email, or phone"
              value={searchTerm}
              onChange={handleInputChange}
              onFocus={() => setShowResults(true)}
            />
            <Button onClick={handleCreateCustomer}>New</Button>
          </>
        )}
      </div>

      {/* Search results dropdown */}
      {showResults && !selectedCustomer && (
         /* Dropdown container styling for light/dark */
        <div className="absolute z-10 w-full mt-1 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md shadow-lg max-h-60 overflow-auto">
          {loading ? (
             /* Text color for light/dark */
            <div className="p-3 text-center text-gray-500 dark:text-gray-400">Loading...</div>
          ) : error ? (
             /* Error color is likely fine */
            <div className="p-3 text-center text-red-500">{error}</div>
          ) : customers.length === 0 ? (
             /* Text color for light/dark */
            <div className="p-3 text-center text-gray-500 dark:text-gray-400">
              {searchTerm.length < 2 ? 'Type to search' : 'No customers found'}
            </div>
          ) : (
            <ul>
              {customers.map((customer) => (
                <li
                  key={customer.id}
                   /* List item styling for light/dark */
                  className="px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer border-b border-gray-200 dark:border-gray-700 last:border-0"
                  onClick={() => handleCustomerClick(customer)}
                >
                   {/* Text colors for light/dark */}
                  <div className="font-medium text-gray-900 dark:text-white">{customer.full_name}</div>
                  <div className="text-sm text-gray-500 dark:text-gray-400 flex gap-3">
                    <span>{customer.email}</span>
                    <span>{customer.phone}</span>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
};

export default CustomerSelector;
