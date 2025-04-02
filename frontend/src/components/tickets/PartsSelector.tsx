import React, { useState, useEffect, useCallback } from 'react';
import { partService } from '../../services';
import { type Part } from '../../services/part-service';
import { Input, Button } from '../ui';
import debounce from 'lodash.debounce';

export interface SelectedPart {
  part: Part;
  quantity: number;
  price: number;
}

interface PartsSelectorProps {
  selectedParts: SelectedPart[];
  onPartsChange: (parts: SelectedPart[]) => void;
  className?: string;
}

export const PartsSelector: React.FC<PartsSelectorProps> = ({
  selectedParts,
  onPartsChange,
  className = '',
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState<Part[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showResults, setShowResults] = useState(false);

  // Debounced search function
  const debouncedSearch = useCallback(
    debounce(async (term: string) => {
      if (!term || term.length < 2) {
        setSearchResults([]);
        return;
      }

      setLoading(true);
      setError('');
      
      try {
        // This assumes the backend has a search endpoint
        // If not, we'd fetch all parts and filter client-side
        const results = await partService.searchParts(term);
        setSearchResults(results);
      } catch (err) {
        console.error('Error searching parts:', err);
        setError('Failed to search parts');
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

  const handlePartClick = (part: Part) => {
    // Check if part is already selected
    if (selectedParts.some(p => p.part.id === part.id)) {
      return;
    }
    
    // Add part to selected parts
    onPartsChange([
      ...selectedParts,
      { part, quantity: 1, price: part.retail_price }
    ]);
    
    setSearchTerm('');
    setShowResults(false);
  };

  const handleQuantityChange = (partId: string, quantity: number) => {
    if (quantity < 1) return;
    
    const updatedParts = selectedParts.map(p => 
      p.part.id === partId ? { ...p, quantity } : p
    );
    
    onPartsChange(updatedParts);
  };

  const handlePriceChange = (partId: string, price: number) => {
    if (price < 0) return;
    
    const updatedParts = selectedParts.map(p => 
      p.part.id === partId ? { ...p, price } : p
    );
    
    onPartsChange(updatedParts);
  };

  const handleRemovePart = (partId: string) => {
    const updatedParts = selectedParts.filter(p => p.part.id !== partId);
    onPartsChange(updatedParts);
  };

  // Calculate total parts cost
  const totalPartsCost = selectedParts.reduce(
    (total, { quantity, price }) => total + quantity * price,
    0
  );

  return (
    <div className={className}>
      <div className="mb-4">
        <Input
          placeholder="Search parts by name or SKU"
          value={searchTerm}
          onChange={handleInputChange}
          onFocus={() => setShowResults(true)}
        />
        
        {/* Search results dropdown */}
        {showResults && searchTerm.length > 0 && (
          <div className="relative">
             {/* Dropdown container styling for light/dark */}
            <div className="absolute z-10 w-full mt-1 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md shadow-lg max-h-60 overflow-auto">
              {loading ? (
                 /* Text color for light/dark */
                <div className="p-3 text-center text-gray-500 dark:text-gray-400">Loading...</div>
              ) : error ? (
                 /* Error color is likely fine */
                <div className="p-3 text-center text-red-500">{error}</div>
              ) : searchResults.length === 0 ? (
                 /* Text color for light/dark */
                <div className="p-3 text-center text-gray-500 dark:text-gray-400">
                  {searchTerm.length < 2 ? 'Type to search' : 'No parts found'}
                </div>
              ) : (
                <ul>
                  {searchResults.map((part) => (
                    <li
                      key={part.id}
                       /* List item styling for light/dark */
                      className={`px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer border-b border-gray-200 dark:border-gray-700 last:border-0 ${
                        selectedParts.some(p => p.part.id === part.id) ? 'opacity-50 cursor-not-allowed' : '' /* Adjusted disabled style */
                      }`}
                      onClick={() => !selectedParts.some(p => p.part.id === part.id) && handlePartClick(part)} // Prevent clicking if already selected
                    >
                       {/* Text colors for light/dark */}
                      <div className="font-medium text-gray-900 dark:text-white">{part.name}</div>
                      <div className="text-sm text-gray-500 dark:text-gray-400 flex justify-between">
                        <span>SKU: {part.sku}</span>
                        <span>${part.retail_price.toFixed(2)}</span>
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Selected parts table */}
      {selectedParts.length > 0 && (
         /* Table container styling for light/dark */
        <div className="border border-gray-200 dark:border-gray-700 rounded-md overflow-hidden">
           {/* Table divider color for light/dark */}
          <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
             {/* Table header styling for light/dark */}
            <thead className="bg-gray-50 dark:bg-gray-800">
              <tr>
                 {/* Table header text color for light/dark */}
                <th scope="col" className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Part
                </th>
                <th scope="col" className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Quantity
                </th>
                <th scope="col" className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Price
                </th>
                <th scope="col" className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Total
                </th>
                <th scope="col" className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
             {/* Table body styling for light/dark */}
            <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              {selectedParts.map(({ part, quantity, price }) => (
                <tr key={part.id}>
                  <td className="px-4 py-2 whitespace-nowrap">
                     {/* Text colors for light/dark */}
                    <div className="text-sm font-medium text-gray-900 dark:text-white">{part.name}</div>
                    <div className="text-xs text-gray-500 dark:text-gray-400">SKU: {part.sku}</div>
                  </td>
                  <td className="px-4 py-2 whitespace-nowrap">
                     {/* Use .form-input for theme-aware styling */}
                    <input
                      type="number"
                      min="1"
                      value={quantity}
                      onChange={(e) => handleQuantityChange(part.id, parseInt(e.target.value) || 1)}
                      className="form-input w-16 p-1 text-sm" /* Adjusted padding/size */
                    />
                  </td>
                  <td className="px-4 py-2 whitespace-nowrap">
                    <div className="flex items-center">
                       {/* Text color for light/dark */}
                      <span className="mr-1 text-gray-500 dark:text-gray-400">$</span>
                       {/* Use .form-input for theme-aware styling */}
                      <input
                        type="number"
                        min="0"
                        step="0.01"
                        value={price}
                        onChange={(e) => handlePriceChange(part.id, parseFloat(e.target.value) || 0)}
                        className="form-input w-20 p-1 text-sm" /* Adjusted padding/size */
                      />
                    </div>
                  </td>
                   {/* Text color for light/dark */}
                  <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                    ${(quantity * price).toFixed(2)}
                  </td>
                  <td className="px-4 py-2 whitespace-nowrap text-right">
                    <button
                      onClick={() => handleRemovePart(part.id)}
                       /* Remove button color is likely fine */
                      className="text-red-500 hover:text-red-400"
                    >
                      Remove
                    </button>
                  </td>
                </tr>
              ))}
               {/* Table footer styling for light/dark */}
              <tr className="bg-gray-50 dark:bg-gray-700">
                 {/* Text color for light/dark */}
                <td colSpan={3} className="px-4 py-2 text-right text-sm font-medium text-gray-900 dark:text-white">
                  Total Parts Cost:
                </td>
                 {/* Text color for light/dark */}
                <td className="px-4 py-2 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                  ${totalPartsCost.toFixed(2)}
                </td>
                <td></td>
              </tr>
            </tbody>
          </table>
        </div>
      )}
      
      {selectedParts.length === 0 && (
         /* Placeholder styling for light/dark */
        <div className="text-center py-6 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md">
          <p className="text-gray-500 dark:text-gray-400">No parts added yet</p>
          <p className="text-gray-400 dark:text-gray-500 text-sm mt-1">Search above to add parts to this ticket</p>
        </div>
      )}
    </div>
  );
};

export default PartsSelector;
