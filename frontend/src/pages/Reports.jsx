import { useState, useEffect } from 'react'
import { useTenantStore } from '@/store/tenantStore'
import { reportService } from '@/services/reportService'
import {
  BarChart3,
  TrendingUp,
  Users,
  Package,
  DollarSign,
  Download,
  Calendar,
} from 'lucide-react'
import { formatCurrency, formatDate } from '@/utils/helpers'
import { cn } from '@/utils/helpers'

const reportTypes = [
  { id: 'vendas', label: 'Vendas', icon: TrendingUp },
  { id: 'financeiro', label: 'Financeiro', icon: DollarSign },
  { id: 'estoque', label: 'Estoque', icon: Package },
  { id: 'clientes', label: 'Clientes', icon: Users },
]

export default function Reports() {
  const { currentTenant } = useTenantStore()
  const [activeReport, setActiveReport] = useState('vendas')
  const [dateRange, setDateRange] = useState({
    start: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    end: new Date().toISOString().split('T')[0],
  })
  const [reportData, setReportData] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    if (currentTenant?.id) {
      loadReport()
    }
  }, [currentTenant, activeReport, dateRange])

  const loadReport = async () => {
    setIsLoading(true)
    try {
      let data
      switch (activeReport) {
        case 'vendas':
          data = await reportService.getVendasPorPeriodo(
            currentTenant.id,
            dateRange.start,
            dateRange.end
          )
          break
        case 'estoque':
          data = await reportService.getPosicaoEstoque(currentTenant.id)
          break
        case 'clientes':
          data = await reportService.getAnaliseClientes(currentTenant.id)
          break
        default:
          data = null
      }
      setReportData(data)
    } catch (error) {
      console.error('Erro ao carregar relatório:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Relatórios</h1>
          <p className="text-muted-foreground">
            Análises e relatórios do seu negócio
          </p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 border border-border rounded-lg hover:bg-muted transition-colors">
          <Download className="w-5 h-5" />
          Exportar
        </button>
      </div>

      {/* Report Types */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {reportTypes.map((type) => (
          <button
            key={type.id}
            onClick={() => setActiveReport(type.id)}
            className={cn(
              'p-4 rounded-xl border-2 transition-all flex items-center gap-3',
              activeReport === type.id
                ? 'border-primary bg-primary/5'
                : 'border-border hover:border-primary/50'
            )}
          >
            <type.icon className="w-5 h-5" />
            <span className="font-medium">{type.label}</span>
          </button>
        ))}
      </div>

      {/* Date Range */}
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <Calendar className="w-5 h-5 text-muted-foreground" />
          <input
            type="date"
            value={dateRange.start}
            onChange={(e) => setDateRange((prev) => ({ ...prev, start: e.target.value }))}
            className="px-3 py-2 bg-card border border-border rounded-lg"
          />
          <span className="text-muted-foreground">até</span>
          <input
            type="date"
            value={dateRange.end}
            onChange={(e) => setDateRange((prev) => ({ ...prev, end: e.target.value }))}
            className="px-3 py-2 bg-card border border-border rounded-lg"
          />
        </div>
      </div>

      {/* Report Content */}
      <div className="bg-card border border-border rounded-xl p-6">
        {isLoading ? (
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary" />
          </div>
        ) : (
          <div className="space-y-6">
            {activeReport === 'vendas' && reportData && (
              <>
                <div className="grid grid-cols-3 gap-4">
                  <div className="p-4 bg-muted rounded-lg">
                    <p className="text-sm text-muted-foreground">Total de Vendas</p>
                    <p className="text-2xl font-bold">{reportData.summary?.total_sales || 0}</p>
                  </div>
                  <div className="p-4 bg-muted rounded-lg">
                    <p className="text-sm text-muted-foreground">Valor Total</p>
                    <p className="text-2xl font-bold">
                      {formatCurrency(reportData.summary?.total_value || 0)}
                    </p>
                  </div>
                  <div className="p-4 bg-muted rounded-lg">
                    <p className="text-sm text-muted-foreground">Ticket Médio</p>
                    <p className="text-2xl font-bold">
                      {formatCurrency(
                        (reportData.summary?.total_value || 0) /
                          (reportData.summary?.total_sales || 1)
                      )}
                    </p>
                  </div>
                </div>

                <div>
                  <h3 className="font-semibold mb-4">Vendas por Dia</h3>
                  <div className="overflow-x-auto">
                    <table className="w-full">
                      <thead className="bg-muted">
                        <tr>
                          <th className="px-4 py-3 text-left">Data</th>
                          <th className="px-4 py-3 text-right">Quantidade</th>
                          <th className="px-4 py-3 text-right">Total</th>
                          <th className="px-4 py-3 text-right">Desconto</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-border">
                        {reportData.items?.map((item, index) => (
                          <tr key={index}>
                            <td className="px-4 py-3">{formatDate(item.date)}</td>
                            <td className="px-4 py-3 text-right">{item.count}</td>
                            <td className="px-4 py-3 text-right">
                              {formatCurrency(item.total)}
                            </td>
                            <td className="px-4 py-3 text-right">
                              {formatCurrency(item.discount)}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </>
            )}

            {activeReport === 'estoque' && reportData && (
              <>
                <div className="grid grid-cols-2 gap-4 mb-6">
                  <div className="p-4 bg-muted rounded-lg">
                    <p className="text-sm text-muted-foreground">Total de Produtos</p>
                    <p className="text-2xl font-bold">{reportData.summary?.total_products || 0}</p>
                  </div>
                  <div className="p-4 bg-muted rounded-lg">
                    <p className="text-sm text-muted-foreground">Valor em Estoque</p>
                    <p className="text-2xl font-bold">
                      {formatCurrency(reportData.summary?.total_stock_value || 0)}
                    </p>
                  </div>
                </div>

                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead className="bg-muted">
                      <tr>
                        <th className="px-4 py-3 text-left">Produto</th>
                        <th className="px-4 py-3 text-left">Código</th>
                        <th className="px-4 py-3 text-right">Estoque</th>
                        <th className="px-4 py-3 text-right">Preço Custo</th>
                        <th className="px-4 py-3 text-right">Preço Venda</th>
                        <th className="px-4 py-3 text-right">Valor Estoque</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-border">
                      {reportData.items?.map((item, index) => (
                        <tr key={index}>
                          <td className="px-4 py-3">{item.name}</td>
                          <td className="px-4 py-3">{item.code}</td>
                          <td className="px-4 py-3 text-right">
                            <span
                              className={cn(
                                item.stock <= item.min_stock && 'text-destructive font-medium'
                              )}
                            >
                              {item.stock}
                            </span>
                          </td>
                          <td className="px-4 py-3 text-right">
                            {formatCurrency(item.cost_price)}
                          </td>
                          <td className="px-4 py-3 text-right">
                            {formatCurrency(item.sale_price)}
                          </td>
                          <td className="px-4 py-3 text-right">
                            {formatCurrency(item.stock_value)}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </>
            )}

            {activeReport === 'clientes' && reportData && (
              <>
                <div className="grid grid-cols-2 gap-4 mb-6">
                  <div className="p-4 bg-muted rounded-lg">
                    <p className="text-sm text-muted-foreground">Total de Clientes</p>
                    <p className="text-2xl font-bold">{reportData.summary?.total_customers || 0}</p>
                  </div>
                  <div className="p-4 bg-muted rounded-lg">
                    <p className="text-sm text-muted-foreground">Clientes com Compras</p>
                    <p className="text-2xl font-bold">
                      {reportData.summary?.customers_with_purchases || 0}
                    </p>
                  </div>
                </div>

                <div>
                  <h3 className="font-semibold mb-4">Top Clientes</h3>
                  <div className="overflow-x-auto">
                    <table className="w-full">
                      <thead className="bg-muted">
                        <tr>
                          <th className="px-4 py-3 text-left">Cliente</th>
                          <th className="px-4 py-3 text-right">Compras</th>
                          <th className="px-4 py-3 text-right">Total</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-border">
                        {reportData.top_customers?.map((item, index) => (
                          <tr key={index}>
                            <td className="px-4 py-3">{item.name}</td>
                            <td className="px-4 py-3 text-right">{item.purchases}</td>
                            <td className="px-4 py-3 text-right">
                              {formatCurrency(item.total)}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
