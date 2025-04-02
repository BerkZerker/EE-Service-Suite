import { Routes, Route } from 'react-router-dom';
import { Suspense, lazy } from 'react';
import Spinner from './components/ui/Spinner'; // Import Spinner

// Layouts
const MainLayout = lazy(() => import('./components/layout/MainLayout'))

// Auth Component
const ProtectedRoute = lazy(() => import('./components/auth/ProtectedRoute'))

// Pages
const Dashboard = lazy(() => import('./pages/Dashboard'))
const NotFound = lazy(() => import('./pages/NotFound'))
const Login = lazy(() => import('./pages/Login'))
const TicketList = lazy(() => import('./pages/TicketList'))
const CreateTicket = lazy(() => import('./pages/CreateTicket'))
const EditTicket = lazy(() => import('./pages/EditTicket'))
const TicketDetail = lazy(() => import('./pages/TicketDetail'));

function App() {
  return (
    // Update Suspense fallback to use theme variables and Spinner
    <Suspense
      fallback={
        <div className="flex items-center justify-center h-screen bg-[var(--color-background)] text-[var(--color-text)]">
          <Spinner size="lg" variant="primary" /> {/* Use themed spinner */}
        </div>
      }
    >
      <Routes>
        {/* Public routes */}
        <Route path="/login" element={<Login />} />

        {/* Protected routes */}
        <Route element={<ProtectedRoute />}>
          <Route path="/" element={<MainLayout />}>
            <Route index element={<Dashboard />} />
            <Route path="tickets" element={<TicketList />} />
            <Route path="tickets/new" element={<CreateTicket />} />
            <Route path="tickets/:id" element={<TicketDetail />} />
            <Route path="tickets/:id/edit" element={<EditTicket />} />
            <Route path="*" element={<NotFound />} />
          </Route>
        </Route>
      </Routes>
    </Suspense>
  )
}

export default App
