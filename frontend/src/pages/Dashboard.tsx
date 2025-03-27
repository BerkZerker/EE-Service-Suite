import { useState, useEffect } from 'react'
import Card from '../components/ui/Card'
import Spinner from '../components/ui/Spinner'
import { useAuth } from '../contexts/auth-context'

type ApiStatus = 'loading' | 'success' | 'error'

const Dashboard = () => {
  const { user } = useAuth()
  const [apiStatus, setApiStatus] = useState<ApiStatus>('loading')
  const [ticketCount, setTicketCount] = useState<number | null>(null)
  const [customerCount, setCustomerCount] = useState<number | null>(null)

  useEffect(() => {
    const checkApiStatus = async () => {
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
    }

    // Mock data for now - in real implementation we'd fetch from API
    const loadDashboardData = async () => {
      // Simulate loading
      await new Promise(resolve => setTimeout(resolve, 500))
      setTicketCount(12) // Placeholder
      setCustomerCount(8) // Placeholder
    }

    checkApiStatus()
    loadDashboardData()
  }, [])

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
          <div className="flex flex-col items-center justify-center py-4">
            {ticketCount === null ? (
              <Spinner size="lg" variant="primary" />
            ) : (
              <>
                <span className="text-4xl font-bold text-primary-400">{ticketCount}</span>
                <span className="text-gray-400 mt-1">Tickets in progress</span>
              </>
            )}
          </div>
        </Card>

        {/* Customers card */}
        <Card title="Customers">
          <div className="flex flex-col items-center justify-center py-4">
            {customerCount === null ? (
              <Spinner size="lg" variant="primary" />
            ) : (
              <>
                <span className="text-4xl font-bold text-secondary-400">{customerCount}</span>
                <span className="text-gray-400 mt-1">Total customers</span>
              </>
            )}
          </div>
        </Card>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        <Card title="Recent Tickets" className="lg:col-span-2">
          <div className="py-8 flex flex-col items-center justify-center text-gray-400">
            <p>Ticket listing will appear here</p>
          </div>
        </Card>
      </div>
    </div>
  )
}

export default Dashboard