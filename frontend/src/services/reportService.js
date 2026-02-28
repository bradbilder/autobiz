import api from './api'

export const reportService = {
  getDashboard: async (tenantId, period = 'month') => {
    const response = await api.get(`/reports/${tenantId}/dashboard`, {
      params: { period },
    })
    return response.data
  },

  getAvailableReports: async (tenantId) => {
    const response = await api.get(`/reports/${tenantId}/available`)
    return response.data
  },

  getVendasPorPeriodo: async (tenantId, dataInicio, dataFim, formato = 'json') => {
    const response = await api.get(`/reports/${tenantId}/vendas/por-periodo`, {
      params: { data_inicio: dataInicio, data_fim: dataFim, formato },
    })
    return response.data
  },

  getVendasPorProduto: async (tenantId, dataInicio, dataFim, limit = 20) => {
    const response = await api.get(`/reports/${tenantId}/vendas/por-produto`, {
      params: { data_inicio: dataInicio, data_fim: dataFim, limit },
    })
    return response.data
  },

  getFluxoCaixa: async (tenantId, dataInicio, dataFim) => {
    const response = await api.get(`/reports/${tenantId}/financeiro/fluxo-caixa`, {
      params: { data_inicio: dataInicio, data_fim: dataFim },
    })
    return response.data
  },

  getPosicaoEstoque: async (tenantId) => {
    const response = await api.get(`/reports/${tenantId}/estoque/posicao`)
    return response.data
  },

  getAnaliseClientes: async (tenantId) => {
    const response = await api.get(`/reports/${tenantId}/clientes/analise`)
    return response.data
  },

  createCustomReport: async (tenantId, config) => {
    const response = await api.post(`/reports/${tenantId}/custom`, config)
    return response.data
  },
}
