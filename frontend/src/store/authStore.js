import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { authService } from '@/services/authService'

export const useAuthStore = create(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      refreshToken: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      login: async (email, password) => {
        set({ isLoading: true, error: null })
        try {
          const response = await authService.login(email, password)
          set({
            user: response.user,
            token: response.access_token,
            refreshToken: response.refresh_token,
            isAuthenticated: true,
            isLoading: false,
          })
          return true
        } catch (error) {
          set({
            error: error.response?.data?.detail || 'Erro ao fazer login',
            isLoading: false,
          })
          return false
        }
      },

      register: async (name, email, password, phone) => {
        set({ isLoading: true, error: null })
        try {
          const response = await authService.register(name, email, password, phone)
          set({
            user: response.user,
            token: response.access_token,
            refreshToken: response.refresh_token,
            isAuthenticated: true,
            isLoading: false,
          })
          return true
        } catch (error) {
          set({
            error: error.response?.data?.detail || 'Erro ao criar conta',
            isLoading: false,
          })
          return false
        }
      },

      logout: () => {
        set({
          user: null,
          token: null,
          refreshToken: null,
          isAuthenticated: false,
          error: null,
        })
      },

      updateUser: (userData) => {
        set({ user: { ...get().user, ...userData } })
      },

      clearError: () => set({ error: null }),
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        refreshToken: state.refreshToken,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)
