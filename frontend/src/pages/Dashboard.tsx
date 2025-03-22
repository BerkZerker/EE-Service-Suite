import { useState, useEffect } from 'react'

type ApiStatus = 'loading' | 'success' | 'error'

const Dashboard = () => {
  const [apiStatus, setApiStatus] = useState<ApiStatus>('loading')

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

    checkApiStatus()
  }, [])

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Status card */}
        <div className="card">
          <h2 className="text-lg font-semibold mb-3">System Status</h2>
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
        </div>

        {/* More cards would go here */}
      </div>
      
      <div className="mt-8">
        <h2 className="text-xl font-semibold mb-4">Welcome to EE Service Suite</h2>
        <p className="text-gray-300">
          This dashboard will display key metrics and information about your service operations.
        </p>
      </div>
    </div>
  )
}

export default Dashboard