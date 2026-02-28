import {
  ShoppingCart,
  UserPlus,
  Package,
  AlertCircle,
  TrendingUp,
} from 'lucide-react'
import { formatDateTime } from '@/utils/helpers'

const iconMap = {
  venda: ShoppingCart,
  cliente: UserPlus,
  produto: Package,
  alerta: AlertCircle,
  sistema: TrendingUp,
}

const colorMap = {
  venda: 'bg-success/10 text-success',
  cliente: 'bg-primary/10 text-primary',
  produto: 'bg-accent/10 text-accent',
  alerta: 'bg-warning/10 text-warning',
  sistema: 'bg-secondary/10 text-secondary',
}

export default function ActivityFeed({ activities = [] }) {
  return (
    <div className="bg-card border border-border rounded-xl p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold">Atividades Recentes</h3>
        <button className="text-sm text-primary hover:underline">
          Ver todas
        </button>
      </div>

      {activities.length === 0 ? (
        <div className="text-center py-8 text-muted-foreground">
          <AlertCircle className="w-12 h-12 mx-auto mb-3 opacity-50" />
          <p>Nenhuma atividade recente</p>
        </div>
      ) : (
        <div className="space-y-4">
          {activities.map((activity, index) => {
            const Icon = iconMap[activity.type] || AlertCircle
            const colorClass = colorMap[activity.type] || 'bg-muted text-muted-foreground'

            return (
              <div key={index} className="flex items-start gap-4">
                <div className={`w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0 ${colorClass}`}>
                  <Icon className="w-5 h-5" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="font-medium truncate">{activity.description}</p>
                  {activity.client && (
                    <p className="text-sm text-muted-foreground">
                      Cliente: {activity.client}
                    </p>
                  )}
                  <p className="text-xs text-muted-foreground mt-1">
                    {activity.date ? formatDateTime(activity.date) : 'Agora'}
                  </p>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
