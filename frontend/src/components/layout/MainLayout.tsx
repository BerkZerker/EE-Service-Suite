import { Outlet, Link, NavLink } from 'react-router-dom'; // Import NavLink
import { useState } from 'react';
import { useAuth } from '../../contexts/auth-context';
import ThemeToggle from '../ui/ThemeToggle'; // Import ThemeToggle
import { LuBike, LuComponent } from 'react-icons/lu'; // Revert to correct submodule import path

// Placeholder Icons (Replace with actual icons later if needed)
const PlaceholderIcon = () => (
  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" /> {/* Simple plus sign */}
  </svg>
);
const DashboardIcon = () => (
  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
  </svg>
);
const TicketIcon = () => (
  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
  </svg>
);
const CustomerIcon = () => (
  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
  </svg>
);
// Removed BikeIcon and PartIcon placeholder components
const SettingsIcon = () => ( // Placeholder - using a cog
  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
  </svg>
);

const navLinks = [
  { text: 'Dashboard', to: '/', icon: <DashboardIcon /> },
  { text: 'Tickets', to: '/tickets', icon: <TicketIcon /> },
  { text: 'Customers', to: '/customers', icon: <CustomerIcon /> },
  { text: 'Bikes', to: '/bikes', icon: <LuBike className="w-5 h-5" /> }, // Use LuBike
  { text: 'Parts', to: '/parts', icon: <LuComponent className="w-5 h-5" /> }, // Use LuComponent
  { text: 'Settings', to: '/settings', icon: <SettingsIcon /> },
];

const MainLayout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [userMenuOpen, setUserMenuOpen] = useState(false)
  const { user, logout } = useAuth()

  return (
    // Use CSS variables for background and text
    <div className="flex h-screen bg-[var(--color-background)] text-[var(--color-text)]">
      {/* Sidebar */}
      <aside
        // Use CSS variables for background and border
        className={`fixed inset-y-0 z-10 flex flex-col flex-shrink-0 w-64 max-h-screen overflow-hidden transition-all transform bg-[var(--color-background)] border-r border-[var(--color-border)] shadow-lg lg:z-auto lg:static lg:shadow-none ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        {/* Sidebar Header */}
        {/* Use CSS variables for border */}
        <div className="flex items-center justify-between flex-shrink-0 h-16 px-6 border-b border-[var(--color-border)]">
          {/* Use CSS variable for title color */}
          <span className="text-xl font-semibold text-[var(--color-primary)]">EE Service Suite</span>
          <button
            onClick={() => setSidebarOpen(false)}
            // Use CSS variables for text and hover background, ensure hover text uses --color-text
            className="p-1 transition-colors duration-200 rounded-md lg:hidden text-[var(--color-text)] hover:bg-[var(--color-accent)] hover:text-[var(--color-text)]"
          >
            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <nav className="flex-1 overflow-y-auto"> {/* Changed overflow-auto to overflow-y-auto */}
          <ul className="p-2 space-y-1"> {/* Adjusted padding and added space-y */}
            {navLinks.map((link) => (
              <li key={link.text}>
                <NavLink 
                  to={link.to} 
                  className={({ isActive }) =>
                    `flex items-center p-2 space-x-2 rounded-md transition-colors duration-150 ${
                      isActive
                        // Use CSS variables for active link style - Use --color-text for dark mode text
                        ? 'bg-[var(--color-primary)] text-[var(--color-text)] dark:text-[var(--color-text)]' // Explicitly set dark text
                        // Use CSS variables for inactive link style, ensure hover text uses --color-text
                        : 'text-[var(--color-text)] hover:bg-[var(--color-accent)] hover:text-[var(--color-text)]'
                    }`
                  }
                  end // Use 'end' prop for Dashboard link to avoid matching all routes starting with '/'
                >
                  {link.icon}
                  <span>{link.text}</span>
                </NavLink>
              </li>
            ))}
            {/* Keep Admin link separate if needed, or integrate into navLinks with conditional rendering */}
            {user?.is_admin && (
              <li className="mt-2"> {/* Add margin-top if keeping separate */}
                <NavLink 
                  to="/admin" 
                  className={({ isActive }) =>
                    `flex items-center p-2 space-x-2 rounded-md transition-colors duration-150 ${
                      isActive
                        // Use CSS variables for active link style - Use --color-text for dark mode text
                        ? 'bg-[var(--color-primary)] text-[var(--color-text)] dark:text-[var(--color-text)]' // Explicitly set dark text
                        // Use CSS variables for inactive link style, ensure hover text uses --color-text
                        : 'text-[var(--color-text)] hover:bg-[var(--color-accent)] hover:text-[var(--color-text)]'
                    }`
                  }
                >
                  <SettingsIcon /> {/* Using SettingsIcon as placeholder for Admin */}
                  <span>Admin</span>
                </NavLink>
              </li>
            )}
          </ul>
        </nav>
      </aside>

      {/* Main content */}
      <div className="flex flex-col flex-1 max-h-screen overflow-x-hidden overflow-y-auto">
        {/* Header */}
        {/* Use CSS variables for background and border */}
        <header className="flex items-center justify-between flex-shrink-0 h-16 px-6 bg-[var(--color-background)] border-b border-[var(--color-border)]">
          <button
            onClick={() => setSidebarOpen(true)}
             // Use CSS variables for text and hover background, ensure hover text uses --color-text
            className="p-1 transition-colors duration-200 rounded-md lg:hidden text-[var(--color-text)] hover:bg-[var(--color-accent)] hover:text-[var(--color-text)]"
          >
            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          
          {/* Right side of header: Theme Toggle + User Menu */}
          <div className="ml-auto flex items-center space-x-4"> 
            <ThemeToggle /> {/* Add Theme Toggle Button */}

            {/* User menu */}
            <div className="relative">
              <button
                onClick={() => setUserMenuOpen(!userMenuOpen)}
                 // Use CSS variables for text and hover background, ensure hover text uses --color-text
                className="flex items-center space-x-2 p-2 rounded-md text-[var(--color-text)] hover:bg-[var(--color-accent)] hover:text-[var(--color-text)]"
              >
                {/* Text color uses CSS variable from parent */}
                <span>{user?.full_name || user?.email}</span>
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              {/* Dropdown menu */}
              {userMenuOpen && (
                 // Use CSS variables for background and border
                <div className="absolute right-0 w-48 mt-2 bg-[var(--color-background)] rounded-md shadow-lg z-10 border border-[var(--color-border)]">
                  <div className="py-1">
                    <button
                      onClick={logout}
                      // Use CSS variables for text and hover background, ensure hover text uses --color-text
                      className="block w-full text-left px-4 py-2 text-sm text-[var(--color-text)] hover:bg-[var(--color-accent)] hover:text-[var(--color-text)]"
                    >
                      Sign out
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </header>
        
        {/* Main content container */}
        {/* Use CSS variable for background */}
        <main className="flex-1 p-6 overflow-auto bg-[var(--color-background)]">
          <Outlet />
        </main>
      </div>
    </div>
  )
}

export default MainLayout
