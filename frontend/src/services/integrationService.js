import api from './api'

export const integrationService = {
  // WhatsApp
  getWhatsAppStatus: async (tenantId) => {
    const response = await api.get(`/integrations/${tenantId}/whatsapp/status`)
    return response.data
  },

  connectWhatsApp: async (tenantId, data) => {
    const response = await api.post(`/integrations/${tenantId}/whatsapp/connect`, data)
    return response.data
  },

  sendWhatsAppMessage: async (tenantId, data) => {
    const response = await api.post(`/integrations/${tenantId}/whatsapp/send`, data)
    return response.data
  },

  getWhatsAppTemplates: async (tenantId) => {
    const response = await api.get(`/integrations/${tenantId}/whatsapp/templates`)
    return response.data
  },

  // Mercado Pago
  getMercadoPagoStatus: async (tenantId) => {
    const response = await api.get(`/integrations/${tenantId}/mercadopago/status`)
    return response.data
  },

  connectMercadoPago: async (tenantId, data) => {
    const response = await api.post(`/integrations/${tenantId}/mercadopago/connect`, data)
    return response.data
  },

  createPreference: async (tenantId, data) => {
    const response = await api.post(`/integrations/${tenantId}/mercadopago/create-preference`, data)
    return response.data
  },

  // Google Calendar
  getGoogleCalendarStatus: async (tenantId) => {
    const response = await api.get(`/integrations/${tenantId}/google-calendar/status`)
    return response.data
  },

  connectGoogleCalendar: async (tenantId, data) => {
    const response = await api.post(`/integrations/${tenantId}/google-calendar/connect`, data)
    return response.data
  },

  // Email
  getEmailStatus: async (tenantId) => {
    const response = await api.get(`/integrations/${tenantId}/email/status`)
    return response.data
  },

  sendEmail: async (tenantId, data) => {
    const response = await api.post(`/integrations/${tenantId}/email/send`, data)
    return response.data
  },

  // Geral
  getAvailableIntegrations: async (tenantId) => {
    const response = await api.get(`/integrations/${tenantId}/available`)
    return response.data
  },

  getConfiguredIntegrations: async (tenantId) => {
    const response = await api.get(`/integrations/${tenantId}/configured`)
    return response.data
  },
}
