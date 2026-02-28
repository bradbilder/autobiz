import { useState, useEffect } from 'react'
import {
  Building2,
  Users,
  TrendingUp,
  DollarSign,
  Activity,
  Server,
} from 'lucide-react'
import { adminService } from '@/services/adminService'
import { formatCurrency } from '@/utils/helpers'
import KPICard from '@/components/dashboard/KPICard'

export default function AdminDashboard() {
  const [stats, setStats] = useState(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    loadStats()
  }, [])

  const loadStats = async () => {
    try {
      const data = await adminService.getStats()
      setStats(data)
    } catch (error) {
      console.error('Erro ao carregar estatísticas:', error)
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

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold">Painel Administrativo</h1>
        <p className="text-muted-foreground">
          Visão geral da plataforma Autobiz
        </p>
      </div>

      {/* KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard
          title="Total de Tenants"
          value={stats?.tenants?.total_tenants || 0}
          change={`+${stats?.tenants?.new_this_month || 0} este mês`}
          trend="up"
          icon={Building2}
          color="primary"
        />
        <KPICard
          title="Total de Usuários"
          value={stats?.users?.total_users || 0}
          change={`+${stats?.users?.new_this_month || 0} este mês`}
          trend="up"
          icon={Users}
          color="success"
        />
        <KPICard
          title="Tenants Ativos"
          value={stats?.tenants?.active_tenants || 0}
          change={`${Math.round(
            ((stats?.tenants?.active_tenants || 0) /
              (stats?.tenants?.total_tenants || 1)) *
              100
          )}% ativos`}
          trend="up"
          icon={Activity}
          color="accent"
        />
        <KPICard
          title="Server Status"
          value="Healthy"
          change="100% uptime"
          trend="up"
          icon={Server}
          color="secondary"
        />
      </div>

      {/* Tenants by Plan */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-card border border-border rounded-xl p-6">
          <h3 className="font-semibold mb-4">Tenants por Plano</h3>
          <div className="space-y-4">
            {stats?.tenants?.by_plan &&
              Object.entries(stats.tenants.by_plan).map(([plan, count]) => (
                <div key={plan} className="flex items-center justify-between">
                  <span className="capitalize">{plan}</span>
                  <div className="flex items-center gap-4">
                    <div className="w-32 h-2 bg-muted rounded-full overflow-hidden">
                      <div
                        className="h-full bg-primary rounded-full"
                        style={{
                          width: `${
                            (count / (stats.tenants.total_tenants || 1)) * 100
                          }%`,
                        }}
                      />
                    </div>
                    <span className="font-medium w-8">{count}</span>
                  </div>
                </div>
              ))}
          </div>
        </div>

        <div className="bg-card border border-border rounded-xl p-6">
          <h3 className="font-semibold mb-4">Tenants por Tipo de Negócio</h3>
          <div className="space-y-4">
            {stats?.tenants?.by_business_type &&
              Object.entries(stats.tenants.by_business_type)
                .slice(0, 6)
                .map(([type, count]) => (
                  <div key={type} className="flex items-center justify-between">
                    <span className="capitalize">{type}</span>
                    <div className="flex items-center gap-4">
                      <div className="w-32 h-2 bg-muted rounded-full overflow-hidden">
                        <div
                          className="h-full bg-success rounded-full"
                          style={{
                            width: `${
                              (count / (stats.tenants.total_tenants || 1)) * 100
                            }%`,
                          }}
                        />
                      </div>
                      <span className="font-medium w-8">{count}</span>
                    </div>
                  </div>
                ))}
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-card border border-border rounded-xl p-6">
        <h3 className="font-semibold mb-4">Atividade Recente</h3>
        <div className="space-y-4">
          <div className="flex items-center gap-4 p-4 bg-muted rounded-lg">
            <div className="w-10 h-10 bg-success/10 rounded-lg flex items-center justify-center">
              <Building2 className="w-5 h-5 text-success" />
            </div>
            <div>
              <p className="font-medium">Novo tenant criado</p>
              <p className="text-sm text-muted-foreground">Minha Loja LTDA - há 5 minutos</p>
            </div>
          </div>
          <div className="flex items-center gap-4 p-4 bg-muted rounded-lg">
            <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center">
              <Users className="w-5 h-5 text-primary" />
            </div>
            <div>
              <p className="font-medium">Novo usuário registrado</p>
              <p className="text-sm text-muted-foreground">joao@email.com - há 15 minutos</p>
            </div>
          </div>
          <div className="flex items-center gap-4 p-4 bg-muted rounded-lg">
            <div className="w-10 h-10 bg-accent/10 rounded-lg flex items-center justify-center">
              <TrendingUp className="w-5 h-5 text-accent" />
            </div>
            <div>
              <p className="font-medium">Upgrade de plano</p>
              <p className="text-sm text-muted-foreground">Tech Solutions - Free para Pro</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
