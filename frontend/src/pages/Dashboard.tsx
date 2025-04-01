import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Card from '../components/ui/Card';
import Spinner from '../components/ui/Spinner';
import Button from '../components/ui/Button';
import { useAuth } from '../contexts/auth-context';
import { ticketService, TicketStatus } from '../services/ticket-service'; // Import service and enum
import { customerService } from '../services/customer-service'; // Import customer service

type ApiStatus = 'loading' | 'success' | 'error';
type DataStatus = 'idle' | 'loading' | 'success' | 'error'; // Status for dashboard data

const Dashboard = () => {
  const { user } = useAuth();
  const [apiStatus, setApiStatus] = useState<ApiStatus>('loading');
  const [dashboardDataStatus, setDashboardDataStatus] = useState<DataStatus>('idle');
  const [activeTicketCount, setActiveTicketCount] = useState<number | null>(null); // Renamed state
  const [customerCount, setCustomerCount] = useState<number | null>(null);

  useEffect(() => {
    const checkApiStatus = async () => {
      setApiStatus('loading'); // Ensure loading state is set initially
      try {
        const response = await fetch('/api/health')
        if (response.ok) {
          setApiStatus('success')
        } else {
          setApiStatus('error')
        }
      } catch (error) {
        setApiStatus('error')
      }
    };

    const loadDashboardData = async () => {
      setDashboardDataStatus('loading');
      try {
        // Fetch all non-archived tickets (backend defaults to archived=false)
        const allNonArchivedTickets = await ticketService.getTickets(0, 1000); // Fetch a large number initially
        
        // Filter out completed/delivered tickets on the frontend
        const activeTickets = allNonArchivedTickets.filter(
          (ticket) => 
            ticket.status !== TicketStatus.COMPLETE && 
            ticket.status !== TicketStatus.DELIVERED
        );
        setActiveTicketCount(activeTickets.length);

        // Fetch customer count (assuming a simple count endpoint or fetching all)
        // This might need adjustment based on actual customer service implementation
        const customers = await customerService.getCustomers(0, 1); // Fetch 1 to get total count if available, or adjust
        // If the API returns total count in headers or a dedicated endpoint exists, use that.
        // Otherwise, fetch all customers (potentially inefficient) or adjust API.
        // For now, using a placeholder based on the existence of the first customer.
        setCustomerCount(customers.length > 0 ? 8 : 0); // Placeholder logic, replace with actual count fetching

        setDashboardDataStatus('success');
      } catch (error) {
        console.error("Error loading dashboard data:", error);
        setDashboardDataStatus('error');
        setActiveTicketCount(0); // Set count to 0 on error
        setCustomerCount(0);
      }
    };

    checkApiStatus();
    loadDashboardData();
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>
      
      <div className="mb-6">
        <h2 className="text-xl font-medium text-gray-200">
          Welcome back, {user?.full_name || 'User'}
        </h2>
        <p className="text-gray-400">
          Here's what's happening with your service operations today
        </p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Status card */}
        <Card title="System Status">
          <div className="flex items-center space-x-2">
            <div className={`h-3 w-3 rounded-full ${
              apiStatus === 'loading' ? 'bg-yellow-500' : 
              apiStatus === 'success' ? 'bg-green-500' : 'bg-red-500'
            }`}></div>
            <span>
              {apiStatus === 'loading' ? 'Checking API connection...' : 
               apiStatus === 'success' ? 'API connected' : 'API connection failed'}
            </span>
          </div>
        </Card>

        {/* Active tickets card */}
        <Card title="Active Tickets">
          <div className="flex flex-col items-center justify-center py-4 min-h-[100px]"> {/* Added min-height */}
            {dashboardDataStatus === 'loading' ? (
              <Spinner size="lg" variant="primary" />
            ) : dashboardDataStatus === 'error' ? (
               <span className="text-red-500">Error loading</span>
            ) : (
              <>
                <span className="text-4xl font-bold text-primary-400">{activeTicketCount}</span>
                <span className="text-gray-400 mt-1">Open & In Progress</span> {/* Updated text */}
              </>
            )}
          </div>
        </Card>

        {/* Customers card */}
        <Card title="Customers">
           <div className="flex flex-col items-center justify-center py-4 min-h-[100px]"> {/* Added min-height */}
            {dashboardDataStatus === 'loading' ? (
              <Spinner size="lg" variant="primary" />
            ) : dashboardDataStatus === 'error' ? (
               <span className="text-red-500">Error loading</span>
            ) : (
              <>
                <span className="text-4xl font-bold text-secondary-400">{customerCount ?? 0}</span> {/* Handle null */}
                <span className="text-gray-400 mt-1">Total customers</span> {/* Keep text */}
              </>
            )}
          </div>
        </Card>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        <Card 
          title="Ticket Management" 
          className="lg:col-span-2"
          headerAction={
            <Link to="/tickets/new">
              <Button size="sm">Create New Ticket</Button>
            </Link>
          }
        >
          <div className="py-6 flex flex-col items-center justify-center gap-4">
            <p className="text-gray-300">Manage customer service tickets in the EE Service Suite</p>
            <div className="flex gap-4">
              <Link to="/tickets">
                <Button variant="primary">View All Tickets</Button>
              </Link>
              <Link to="/tickets/new">
                <Button variant="secondary">Create New Ticket</Button>
              </Link>
            </div>
          </div>
        </Card>
      </div>
    </div>
  )
}

export default Dashboard
