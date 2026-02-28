import api from './api'

export const tenantService = {
  getAll: async () => {
    const response = await api.get('/admin/tenants')
    return response.data
  },

  getById: async (tenantId) => {
    const response = await api.get(`/admin/tenants/${tenantId}`)
    return response.data
  },

  create: async (data) => {
    const response = await api.post('/onboarding/create', data)
    return response.data
  },

  update: async (tenantId, data) => {
    const response = await api.put(`/admin/tenants/${tenantId}`, data)
    return response.data
  },

  delete: async (tenantId) => {
    await api.delete(`/admin/tenants/${tenantId}`)
  },

  getSchema: async (tenantId) => {
    const response = await api.get(`/schema/${tenantId}`)
    return response.data
  },

  getUIConfig: async (tenantId) => {
    const response = await api.get(`/onboarding/status/${tenantId}`)
    return response.data
  },

  getOnboardingQuestions: async () => {
    const response = await api.get('/onboarding/questions')
    return response.data
  },

  getTemplates: async () => {
    const response = await api.get('/onboarding/templates')
    return response.data
  },
}
