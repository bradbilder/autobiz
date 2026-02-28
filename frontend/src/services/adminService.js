import api from './api'

export const adminService = {
  getStats: async () => {
    const response = await api.get('/admin/dashboard/stats')
    return response.data
  },

  getTenants: async (params = {}) => {
    const response = await api.get('/admin/tenants', { params })
    return response.data
  },

  getTenant: async (tenantId) => {
    const response = await api.get(`/admin/tenants/${tenantId}`)
    return response.data
  },

  createTenant: async (data) => {
    const response = await api.post('/admin/tenants', data)
    return response.data
  },

  updateTenant: async (tenantId, data) => {
    const response = await api.put(`/admin/tenants/${tenantId}`, data)
    return response.data
  },

  deleteTenant: async (tenantId) => {
    await api.delete(`/admin/tenants/${tenantId}`)
  },

  getUsers: async (params = {}) => {
    const response = await api.get('/admin/users', { params })
    return response.data
  },

  getUser: async (userId) => {
    const response = await api.get(`/admin/users/${userId}`)
    return response.data
  },

  updateUser: async (userId, data) => {
    const response = await api.put(`/admin/users/${userId}`, data)
    return response.data
  },

  deleteUser: async (userId) => {
    await api.delete(`/admin/users/${userId}`)
  },

  getSettings: async () => {
    const response = await api.get('/admin/settings')
    return response.data
  },

  updateSettings: async (data) => {
    const response = await api.post('/admin/settings', data)
    return response.data
  },

  createBackup: async () => {
    const response = await api.post('/admin/maintenance/backup')
    return response.data
  },

  runCleanup: async () => {
    const response = await api.post('/admin/maintenance/cleanup')
    return response.data
  },
}
