import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../../contexts/auth-context';

const ProtectedRoute = () => {
  const { isAuthenticated, loading } = useAuth();

  // Show loading state while checking authentication
  if (loading) {
    return (
      // Loading screen background/text for light/dark
      <div className="flex items-center justify-center h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
        {/* Spinner color uses primary */}
        <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  // Redirect to login if not authenticated
  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }

  // Render child routes if authenticated
  return <Outlet />;
};

export default ProtectedRoute;
