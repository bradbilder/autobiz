import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { tenantService } from '@/services/tenantService'

export const useTenantStore = create(
  persist(
    (set, get) => ({
      currentTenant: null,
      tenants: [],
      schema: null,
      uiConfig: null,
      isLoading: false,
      error: null,

      setCurrentTenant: (tenant) => {
        set({ currentTenant: tenant })
        // Carregar schema e configurações do tenant
        if (tenant) {
          get().loadTenantConfig(tenant.id)
        }
      },

      loadTenantConfig: async (tenantId) => {
        try {
          const [schema, uiConfig] = await Promise.all([
            tenantService.getSchema(tenantId),
            tenantService.getUIConfig(tenantId),
          ])
          set({ schema, uiConfig })
        } catch (error) {
          console.error('Erro ao carregar configurações do tenant:', error)
        }
      },

      createTenant: async (data) => {
        set({ isLoading: true, error: null })
        try {
          const response = await tenantService.create(data)
          set((state) => ({
            tenants: [...state.tenants, response.tenant],
            isLoading: false,
          }))
          return response
        } catch (error) {
          set({
            error: error.response?.data?.detail || 'Erro ao criar tenant',
            isLoading: false,
          })
          throw error
        }
      },

      updateTenant: async (tenantId, data) => {
        try {
          const response = await tenantService.update(tenantId, data)
          set((state) => ({
            tenants: state.tenants.map((t) =>
              t.id === tenantId ? { ...t, ...response } : t
            ),
            currentTenant:
              state.currentTenant?.id === tenantId
                ? { ...state.currentTenant, ...response }
                : state.currentTenant,
          }))
          return response
        } catch (error) {
          throw error
        }
      },

      clearError: () => set({ error: null }),
    }),
    {
      name: 'tenant-storage',
      partialize: (state) => ({
        currentTenant: state.currentTenant,
        tenants: state.tenants,
      }),
    }
  )
)
