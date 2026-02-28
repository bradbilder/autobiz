import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './store/authStore'

// Layouts
import AuthLayout from './components/layout/AuthLayout'
import DashboardLayout from './components/layout/DashboardLayout'

// Pages
import Login from './pages/Login'
import Register from './pages/Register'
import Onboarding from './pages/Onboarding'
import Dashboard from './pages/Dashboard'
import DynamicList from './pages/DynamicList'
import DynamicForm from './pages/DynamicForm'
import DynamicDetail from './pages/DynamicDetail'
import Reports from './pages/Reports'
import Settings from './pages/Settings'
import Integrations from './pages/Integrations'
import Plugins from './pages/Plugins'
import NotFound from './pages/NotFound'

// Admin Pages
import AdminDashboard from './pages/admin/AdminDashboard'
import AdminTenants from './pages/admin/AdminTenants'
import AdminUsers from './pages/admin/AdminUsers'

// Protected Route Component
const ProtectedRoute = ({ children, requireAdmin = false }) => {
  const { user, isAuthenticated } = useAuthStore()
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }
  
  if (requireAdmin && !user?.is_master_admin) {
    return <Navigate to="/" replace />
  }
  
  return children
}

function App() {
  return (
    <Routes>
      {/* Auth Routes */}
      <Route element={<AuthLayout />}>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Route>
      
      {/* Onboarding */}
      <Route path="/onboarding" element={
        <ProtectedRoute>
          <Onboarding />
        </ProtectedRoute>
      } />
      
      {/* Dashboard Routes */}
      <Route element={
        <ProtectedRoute>
          <DashboardLayout />
        </ProtectedRoute>
      }>
        <Route path="/" element={<Dashboard />} />
        <Route path="/:entity" element={<DynamicList />} />
        <Route path="/:entity/new" element={<DynamicForm />} />
        <Route path="/:entity/:id" element={<DynamicDetail />} />
        <Route path="/:entity/:id/edit" element={<DynamicForm />} />
        <Route path="/relatorios" element={<Reports />} />
        <Route path="/configuracoes" element={<Settings />} />
        <Route path="/integracoes" element={<Integrations />} />
        <Route path="/plugins" element={<Plugins />} />
      </Route>
      
      {/* Admin Routes */}
      <Route element={
        <ProtectedRoute requireAdmin={true}>
          <DashboardLayout />
        </ProtectedRoute>
      }>
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/admin/tenants" element={<AdminTenants />} />
        <Route path="/admin/users" element={<AdminUsers />} />
      </Route>
      
      {/* 404 */}
      <Route path="*" element={<NotFound />} />
    </Routes>
  )
}

export default App
