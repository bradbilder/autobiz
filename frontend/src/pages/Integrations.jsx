import { useState, useEffect } from 'react'
import { useTenantStore } from '@/store/tenantStore'
import { integrationService } from '@/services/integrationService'
import {
  MessageCircle,
  CreditCard,
  Calendar,
  Mail,
  Check,
  X,
  Settings,
  ExternalLink,
} from 'lucide-react'
import { cn } from '@/utils/helpers'

const integrationsList = [
  {
    id: 'whatsapp',
    name: 'WhatsApp Business',
    description: 'Envie mensagens e notificações via WhatsApp',
    icon: MessageCircle,
    color: 'bg-green-500',
    category: 'Comunicação',
  },
  {
    id: 'mercadopago',
    name: 'Mercado Pago',
    description: 'Receba pagamentos online',
    icon: CreditCard,
    color: 'bg-blue-500',
    category: 'Pagamento',
  },
  {
    id: 'google_calendar',
    name: 'Google Calendar',
    description: 'Sincronize agendamentos',
    icon: Calendar,
    color: 'bg-red-500',
    category: 'Produtividade',
  },
  {
    id: 'email',
    name: 'Email Marketing',
    description: 'Envie campanhas de email',
    icon: Mail,
    color: 'bg-purple-500',
    category: 'Marketing',
  },
]

export default function Integrations() {
  const { currentTenant } = useTenantStore()
  const [integrations, setIntegrations] = useState({})
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    if (currentTenant?.id) {
      loadIntegrations()
    }
  }, [currentTenant])

  const loadIntegrations = async () => {
    try {
      const data = await integrationService.getConfiguredIntegrations(currentTenant.id)
      const integrationsMap = {}
      data.integrations.forEach((int) => {
        integrationsMap[int.id] = int
      })
      setIntegrations(integrationsMap)
    } catch (error) {
      console.error('Erro ao carregar integrações:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleConnect = async (integrationId) => {
    // TODO: Implementar fluxo de conexão
    console.log('Conectar:', integrationId)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold">Integrações</h1>
        <p className="text-muted-foreground">
          Conecte seu sistema com outros serviços
        </p>
      </div>

      {/* Integrations Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {integrationsList.map((integration) => {
          const isConnected = integrations[integration.id]?.connected
          const Icon = integration.icon

          return (
            <div
              key={integration.id}
              className="bg-card border border-border rounded-xl p-6"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-4">
                  <div className={cn('w-12 h-12 rounded-xl flex items-center justify-center text-white', integration.color)}>
                    <Icon className="w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="font-semibold">{integration.name}</h3>
                    <p className="text-sm text-muted-foreground">{integration.category}</p>
                  </div>
                </div>
                <div
                  className={cn(
                    'flex items-center gap-1 px-3 py-1 rounded-full text-sm font-medium',
                    isConnected
                      ? 'bg-success/10 text-success'
                      : 'bg-muted text-muted-foreground'
                  )}
                >
                  {isConnected ? (
                    <>
                      <Check className="w-4 h-4" />
                      Conectado
                    </>
                  ) : (
                    <>
                      <X className="w-4 h-4" />
                      Desconectado
                    </>
                  )}
                </div>
              </div>

              <p className="text-muted-foreground mb-6">{integration.description}</p>

              <div className="flex gap-3">
                {isConnected ? (
                  <>
                    <button className="flex items-center gap-2 px-4 py-2 border border-border rounded-lg hover:bg-muted transition-colors">
                      <Settings className="w-4 h-4" />
                      Configurar
                    </button>
                    <button className="flex items-center gap-2 px-4 py-2 border border-border rounded-lg hover:bg-muted transition-colors text-destructive">
                      <X className="w-4 h-4" />
                      Desconectar
                    </button>
                  </>
                ) : (
                  <button
                    onClick={() => handleConnect(integration.id)}
                    className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
                  >
                    <ExternalLink className="w-4 h-4" />
                    Conectar
                  </button>
                )}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
