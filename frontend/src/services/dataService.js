import api from './api'

export const dataService = {
  // CRUD operations
  list: async (tenantId, entity, params = {}) => {
    const response = await api.get(`/data/${tenantId}/${entity}`, { params })
    return response.data
  },

  get: async (tenantId, entity, id) => {
    const response = await api.get(`/data/${tenantId}/${entity}/${id}`)
    return response.data
  },

  create: async (tenantId, entity, data) => {
    const response = await api.post(`/data/${tenantId}/${entity}`, data)
    return response.data
  },

  update: async (tenantId, entity, id, data) => {
    const response = await api.put(`/data/${tenantId}/${entity}/${id}`, data)
    return response.data
  },

  delete: async (tenantId, entity, id) => {
    await api.delete(`/data/${tenantId}/${entity}/${id}`)
  },

  // Custom actions
  executeAction: async (tenantId, entity, id, action, data = {}) => {
    const response = await api.post(
      `/data/${tenantId}/${entity}/${id}/${action}`,
      data
    )
    return response.data
  },

  // Search
  search: async (tenantId, query, entities = []) => {
    const response = await api.get('/search', {
      params: { q: query, entities, tenant_id: tenantId },
    })
    return response.data
  },

  autocomplete: async (tenantId, entity, query) => {
    const response = await api.get('/search/autocomplete', {
      params: { q: query, entity, tenant_id: tenantId },
    })
    return response.data
  },
}
