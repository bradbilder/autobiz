import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '@/store/authStore'

export function useAuth(requireAuth = true) {
  const navigate = useNavigate()
  const { isAuthenticated, user, isLoading } = useAuthStore()

  useEffect(() => {
    if (!isLoading && requireAuth && !isAuthenticated) {
      navigate('/login')
    }
  }, [isAuthenticated, isLoading, requireAuth, navigate])

  return { isAuthenticated, user, isLoading }
}

export function usePermission(permission) {
  const { user } = useAuthStore()
  
  if (!user) return false
  
  // Admin master tem todas as permissões
  if (user.is_master_admin) return true
  
  // TODO: Verificar permissões específicas do tenant
  return true
}
