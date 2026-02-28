import { useEffect, useState } from 'react'
import {
  TrendingUp,
  TrendingDown,
  DollarSign,
  Users,
  Package,
  ShoppingCart,
  AlertTriangle,
} from 'lucide-react'
import { useTenantStore } from '@/store/tenantStore'
import { reportService } from '@/services/reportService'
import { formatCurrency, formatDate } from '@/utils/helpers'
import KPICard from '@/components/dashboard/KPICard'
import ChartWidget from '@/components/dashboard/ChartWidget'
import ActivityFeed from '@/components/dashboard/ActivityFeed'

export default function Dashboard() {
  const { currentTenant } = useTenantStore()
  const [dashboardData, setDashboardData] = useState(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    if (currentTenant?.id) {
      loadDashboardData()
    }
  }, [currentTenant])

  const loadDashboardData = async () => {
    try {
      setIsLoading(true)
      const data = await reportService.getDashboard(currentTenant.id, 'month')
      setDashboardData(data)
    } catch (error) {
      console.error('Erro ao carregar dashboard:', error)
    } finally {
      setIsLoading(false)
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary" />
      </div>
    )
  }

  const kpis = dashboardData?.kpis || {}
  const charts = dashboardData?.charts || {}
  const activities = dashboardData?.activities || []
  const alerts = dashboardData?.alerts || []

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Dashboard</h1>
          <p className="text-muted-foreground">
            Visão geral do seu negócio
          </p>
        </div>
        <div className="flex gap-2">
          <select className="px-4 py-2 bg-card border border-border rounded-lg text-sm">
            <option value="day">Hoje</option>
            <option value="week">Esta semana</option>
            <option value="month" selected>Este mês</option>
            <option value="year">Este ano</option>
          </select>
        </div>
      </div>

      {/* Alerts */}
      {alerts.length > 0 && (
        <div className="space-y-2">
          {alerts.map((alert, index) => (
            <div
              key={index}
              className="flex items-center gap-3 p-4 bg-warning/10 border border-warning/20 rounded-lg"
            >
              <AlertTriangle className="w-5 h-5 text-warning" />
              <div>
                <p className="font-medium text-warning">{alert.title}</p>
                <p className="text-sm text-warning/80">{alert.message}</p>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard
          title="Vendas Totais"
          value={formatCurrency(kpis.vendas_total || 0)}
          change="+12.5%"
          trend="up"
          icon={DollarSign}
          color="primary"
        />
        <KPICard
          title="Total de Vendas"
          value={kpis.vendas_count || 0}
          change="+8.2%"
          trend="up"
          icon={ShoppingCart}
          color="success"
        />
        <KPICard
          title="Ticket Médio"
          value={formatCurrency(kpis.ticket_medio || 0)}
          change="-2.4%"
          trend="down"
          icon={TrendingUp}
          color="accent"
        />
        <KPICard
          title="Clientes Novos"
          value={kpis.clientes_novos || 0}
          change="+15.3%"
          trend="up"
          icon={Users}
          color="secondary"
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ChartWidget
          title="Vendas por Período"
          data={charts.vendas_por_dia || []}
          type="line"
        />
        <ChartWidget
          title="Produtos Mais Vendidos"
          data={charts.produtos_mais_vendidos || []}
          type="bar"
        />
      </div>

      {/* Activity & Quick Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <ActivityFeed activities={activities} />
        </div>
        <div className="bg-card border border-border rounded-xl p-6">
          <h3 className="font-semibold mb-4">Ações Rápidas</h3>
          <div className="space-y-2">
            <button className="w-full flex items-center gap-3 p-3 hover:bg-muted rounded-lg transition-colors text-left">
              <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center">
                <ShoppingCart className="w-5 h-5 text-primary" />
              </div>
              <div>
                <p className="font-medium">Nova Venda</p>
                <p className="text-sm text-muted-foreground">Registrar venda rápida</p>
              </div>
            </button>
            <button className="w-full flex items-center gap-3 p-3 hover:bg-muted rounded-lg transition-colors text-left">
              <div className="w-10 h-10 bg-success/10 rounded-lg flex items-center justify-center">
                <Package className="w-5 h-5 text-success" />
              </div>
              <div>
                <p className="font-medium">Novo Produto</p>
                <p className="text-sm text-muted-foreground">Cadastrar produto</p>
              </div>
            </button>
            <button className="w-full flex items-center gap-3 p-3 hover:bg-muted rounded-lg transition-colors text-left">
              <div className="w-10 h-10 bg-accent/10 rounded-lg flex items-center justify-center">
                <Users className="w-5 h-5 text-accent" />
              </div>
              <div>
                <p className="font-medium">Novo Cliente</p>
                <p className="text-sm text-muted-foreground">Cadastrar cliente</p>
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
