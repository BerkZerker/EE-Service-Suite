import { Link } from 'react-router-dom'

const NotFound = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-[70vh] text-center px-4">
      <h1 className="text-6xl font-bold text-primary-600">404</h1>
      <h2 className="mt-4 text-2xl font-semibold">Page Not Found</h2>
      <p className="mt-2 text-gray-300">
        The page you are looking for doesn't exist or has been moved.
      </p>
      <Link 
        to="/" 
        className="mt-6 btn-primary"
      >
        Return to Dashboard
      </Link>
    </div>
  )
}

export default NotFound