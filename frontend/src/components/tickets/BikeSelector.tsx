import React, { useState, useEffect } from 'react';
import { Customer, Bike, customerService } from '../../services';
import { Select, Button } from '../ui';
import { SelectOption } from '../ui/Select';

interface BikeSelectorProps {
  customerId?: string;
  onBikeSelect: (bike: Bike | null) => void;
  selectedBike?: Bike | null;
  className?: string;
}

export const BikeSelector: React.FC<BikeSelectorProps> = ({
  customerId,
  onBikeSelect,
  selectedBike,
  className = '',
}) => {
  const [bikes, setBikes] = useState<Bike[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showAddForm, setShowAddForm] = useState(false);
  
  // Form state for new bike
  const [make, setMake] = useState('');
  const [model, setModel] = useState('');
  const [serialNumber, setSerialNumber] = useState('');
  const [purchaseDate, setPurchaseDate] = useState('');

  useEffect(() => {
    if (!customerId) {
      setBikes([]);
      return;
    }

    const fetchBikes = async () => {
      setLoading(true);
      setError('');
      
      try {
        const bikeList = await customerService.getCustomerBikes(customerId);
        setBikes(bikeList);
      } catch (err) {
        console.error('Error fetching bikes:', err);
        setError('Failed to load customer bikes');
      } finally {
        setLoading(false);
      }
    };

    fetchBikes();
  }, [customerId]);

  const handleBikeChange = (bikeId: string) => {
    if (bikeId === 'add-new') {
      setShowAddForm(true);
      onBikeSelect(null);
    } else {
      const bike = bikes.find(b => b.id === bikeId);
      onBikeSelect(bike || null);
    }
  };

  const handleAddBike = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!customerId) return;
    
    setLoading(true);
    setError('');
    
    try {
      const newBike = await customerService.createCustomerBike(customerId, {
        make,
        model,
        serial_number: serialNumber,
        purchase_date: purchaseDate,
      });
      
      setBikes(prev => [...prev, newBike]);
      onBikeSelect(newBike);
      setShowAddForm(false);
      
      // Reset form
      setMake('');
      setModel('');
      setSerialNumber('');
      setPurchaseDate('');
    } catch (err) {
      console.error('Error adding bike:', err);
      setError('Failed to add new bike');
    } finally {
      setLoading(false);
    }
  };

  // Generate options for select dropdown
  const bikeOptions: SelectOption[] = [
    ...bikes.map(bike => ({
      value: bike.id,
      label: `${bike.make} ${bike.model} (${bike.serial_number})`,
    })),
    { value: 'add-new', label: '+ Add New Bike' },
  ];

  if (!customerId) {
    return <div className={`text-gray-400 ${className}`}>Select a customer to see their bikes</div>;
  }

  if (showAddForm) {
    return (
      <div className={`bg-gray-800 p-4 rounded-md border border-gray-700 ${className}`}>
        <h3 className="text-white font-medium mb-3">Add New Bike</h3>
        <form onSubmit={handleAddBike} className="space-y-3">
          <div className="grid grid-cols-2 gap-3">
            <input 
              className="bg-gray-700 border border-gray-600 rounded-md p-2 text-white"
              placeholder="Make"
              value={make}
              onChange={e => setMake(e.target.value)}
              required
            />
            <input 
              className="bg-gray-700 border border-gray-600 rounded-md p-2 text-white"
              placeholder="Model"
              value={model}
              onChange={e => setModel(e.target.value)}
              required
            />
          </div>
          <input 
            className="bg-gray-700 border border-gray-600 rounded-md p-2 text-white w-full"
            placeholder="Serial Number"
            value={serialNumber}
            onChange={e => setSerialNumber(e.target.value)}
            required
          />
          <div>
            <label className="block text-sm text-gray-400 mb-1">Purchase Date</label>
            <input 
              type="date"
              className="bg-gray-700 border border-gray-600 rounded-md p-2 text-white w-full"
              value={purchaseDate}
              onChange={e => setPurchaseDate(e.target.value)}
            />
          </div>
          {error && <p className="text-red-500 text-sm">{error}</p>}
          <div className="flex justify-end space-x-2">
            <Button 
              variant="outline" 
              type="button" 
              onClick={() => setShowAddForm(false)}
            >
              Cancel
            </Button>
            <Button type="submit" isLoading={loading}>
              Add Bike
            </Button>
          </div>
        </form>
      </div>
    );
  }

  return (
    <div className={className}>
      <Select
        label="Select Bike"
        options={bikeOptions}
        value={selectedBike?.id || ''}
        onChange={handleBikeChange}
        disabled={loading || !customerId}
        error={error || undefined}
      />
      
      {selectedBike && (
        <div className="mt-2 bg-gray-700 p-2 rounded-md text-sm">
          <div className="grid grid-cols-2 gap-x-4 gap-y-1">
            <div className="text-gray-400">Make:</div>
            <div className="text-white">{selectedBike.make}</div>
            <div className="text-gray-400">Model:</div>
            <div className="text-white">{selectedBike.model}</div>
            <div className="text-gray-400">Serial:</div>
            <div className="text-white">{selectedBike.serial_number}</div>
            {selectedBike.purchase_date && (
              <>
                <div className="text-gray-400">Purchased:</div>
                <div className="text-white">
                  {new Date(selectedBike.purchase_date).toLocaleDateString()}
                </div>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default BikeSelector;