import { Routes, Route } from 'react-router-dom'
import { Suspense, lazy } from 'react'

// Layouts
const MainLayout = lazy(() => import('./components/layout/MainLayout'))

// Pages
const Dashboard = lazy(() => import('./pages/Dashboard'))
const NotFound = lazy(() => import('./pages/NotFound'))

function App() {
  return (
    <Suspense fallback={<div className="flex items-center justify-center h-screen bg-gray-900 text-white">Loading...</div>}>
      <Routes>
        <Route path="/" element={<MainLayout />}>
          <Route index element={<Dashboard />} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </Suspense>
  )
}

export default App