import { Outlet } from 'react-router-dom'
import { useState } from 'react'

const MainLayout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <aside 
        className={`fixed inset-y-0 z-10 flex flex-col flex-shrink-0 w-64 max-h-screen overflow-hidden transition-all transform bg-white border-r shadow-lg lg:z-auto lg:static lg:shadow-none ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        <div className="flex items-center justify-between flex-shrink-0 p-4 border-b">
          <span className="text-xl font-semibold">EE Service Suite</span>
          <button 
            onClick={() => setSidebarOpen(false)}
            className="p-1 transition-colors duration-200 rounded-md lg:hidden hover:bg-gray-100"
          >
            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <nav className="flex-1 overflow-auto">
          <ul className="p-2 overflow-auto">
            <li>
              <a href="/" className="flex items-center p-2 space-x-2 rounded-md hover:bg-gray-100">
                <span>Dashboard</span>
              </a>
            </li>
            {/* Add more menu items here */}
          </ul>
        </nav>
      </aside>

      {/* Main content */}
      <div className="flex flex-col flex-1 max-h-screen overflow-x-hidden overflow-y-auto">
        {/* Header */}
        <header className="flex items-center justify-between flex-shrink-0 h-16 px-6 border-b bg-white">
          <button 
            onClick={() => setSidebarOpen(true)}
            className="p-1 transition-colors duration-200 rounded-md lg:hidden hover:bg-gray-100"
          >
            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          
          <div className="ml-auto">
            {/* User menu */}
            <button className="flex items-center space-x-2">
              <span>User</span>
            </button>
          </div>
        </header>
        
        {/* Main content container */}
        <main className="flex-1 p-6 overflow-auto">
          <Outlet />
        </main>
      </div>
    </div>
  )
}

export default MainLayout