import { useState } from 'react'
import { useAuthStore } from '@/store/authStore'
import { useThemeStore } from '@/store/themeStore'
import {
  User,
  Bell,
  Shield,
  Palette,
  Building2,
  Save,
} from 'lucide-react'
import { cn } from '@/utils/helpers'

const settingsTabs = [
  { id: 'profile', label: 'Perfil', icon: User },
  { id: 'company', label: 'Empresa', icon: Building2 },
  { id: 'notifications', label: 'Notificações', icon: Bell },
  { id: 'security', label: 'Segurança', icon: Shield },
  { id: 'appearance', label: 'Aparência', icon: Palette },
]

export default function Settings() {
  const [activeTab, setActiveTab] = useState('profile')
  const { user } = useAuthStore()
  const { theme, toggleTheme, primaryColor, setPrimaryColor } = useThemeStore()

  const renderTabContent = () => {
    switch (activeTab) {
      case 'profile':
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold mb-4">Informações Pessoais</h3>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Nome</label>
                  <input
                    type="text"
                    defaultValue={user?.name}
                    className="w-full px-4 py-2 bg-muted rounded-lg border border-transparent focus:border-primary focus:outline-none"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Email</label>
                  <input
                    type="email"
                    defaultValue={user?.email}
                    className="w-full px-4 py-2 bg-muted rounded-lg border border-transparent focus:border-primary focus:outline-none"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Telefone</label>
                  <input
                    type="tel"
                    defaultValue={user?.phone}
                    className="w-full px-4 py-2 bg-muted rounded-lg border border-transparent focus:border-primary focus:outline-none"
                  />
                </div>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-4">Foto de Perfil</h3>
              <div className="flex items-center gap-4">
                <div className="w-20 h-20 bg-primary rounded-full flex items-center justify-center text-3xl text-primary-foreground">
                  {user?.name?.charAt(0).toUpperCase()}
                </div>
                <div className="space-y-2">
                  <button className="px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm">
                    Alterar foto
                  </button>
                  <button className="px-4 py-2 border border-border rounded-lg text-sm">
                    Remover
                  </button>
                </div>
              </div>
            </div>
          </div>
        )

      case 'company':
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold mb-4">Dados da Empresa</h3>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Razão Social</label>
                  <input
                    type="text"
                    className="w-full px-4 py-2 bg-muted rounded-lg border border-transparent focus:border-primary focus:outline-none"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">CNPJ</label>
                  <input
                    type="text"
                    className="w-full px-4 py-2 bg-muted rounded-lg border border-transparent focus:border-primary focus:outline-none"
                  />
                </div>
                <div className="col-span-2">
                  <label className="block text-sm font-medium mb-2">Endereço</label>
                  <textarea
                    rows={3}
                    className="w-full px-4 py-2 bg-muted rounded-lg border border-transparent focus:border-primary focus:outline-none"
                  />
                </div>
              </div>
            </div>
          </div>
        )

      case 'notifications':
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold mb-4">Preferências de Notificação</h3>
              <div className="space-y-4">
                {[
                  { id: 'email', label: 'Notificações por Email', description: 'Receba atualizações importantes por email' },
                  { id: 'sms', label: 'Notificações por SMS', description: 'Receba alertas por mensagem de texto' },
                  { id: 'push', label: 'Notificações Push', description: 'Receba notificações no navegador' },
                  { id: 'vendas', label: 'Alertas de Vendas', description: 'Seja notificado sobre novas vendas' },
                  { id: 'estoque', label: 'Alertas de Estoque', description: 'Receba alertas quando o estoque estiver baixo' },
                ].map((item) => (
                  <label key={item.id} className="flex items-start gap-3 p-4 bg-muted rounded-lg cursor-pointer">
                    <input type="checkbox" className="mt-1 rounded" defaultChecked />
                    <div>
                      <p className="font-medium">{item.label}</p>
                      <p className="text-sm text-muted-foreground">{item.description}</p>
                    </div>
                  </label>
                ))}
              </div>
            </div>
          </div>
        )

      case 'security':
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold mb-4">Alterar Senha</h3>
              <div className="space-y-4 max-w-md">
                <div>
                  <label className="block text-sm font-medium mb-2">Senha Atual</label>
                  <input
                    type="password"
                    className="w-full px-4 py-2 bg-muted rounded-lg border border-transparent focus:border-primary focus:outline-none"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Nova Senha</label>
                  <input
                    type="password"
                    className="w-full px-4 py-2 bg-muted rounded-lg border border-transparent focus:border-primary focus:outline-none"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Confirmar Nova Senha</label>
                  <input
                    type="password"
                    className="w-full px-4 py-2 bg-muted rounded-lg border border-transparent focus:border-primary focus:outline-none"
                  />
                </div>
                <button className="px-4 py-2 bg-primary text-primary-foreground rounded-lg">
                  Alterar Senha
                </button>
              </div>
            </div>

            <div className="pt-6 border-t border-border">
              <h3 className="text-lg font-semibold mb-4">Autenticação de Dois Fatores</h3>
              <div className="flex items-center justify-between p-4 bg-muted rounded-lg">
                <div>
                  <p className="font-medium">Autenticação 2FA</p>
                  <p className="text-sm text-muted-foreground">
                    Adicione uma camada extra de segurança
                  </p>
                </div>
                <button className="px-4 py-2 border border-border rounded-lg">
                  Configurar
                </button>
              </div>
            </div>
          </div>
        )

      case 'appearance':
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold mb-4">Tema</h3>
              <div className="flex gap-4">
                <button
                  onClick={() => toggleTheme()}
                  className={cn(
                    'p-4 rounded-xl border-2 transition-all flex flex-col items-center gap-2',
                    theme === 'light'
                      ? 'border-primary bg-primary/5'
                      : 'border-border'
                  )}
                >
                  <div className="w-16 h-16 bg-white border-2 border-gray-200 rounded-lg" />
                  <span className="font-medium">Claro</span>
                </button>
                <button
                  onClick={() => toggleTheme()}
                  className={cn(
                    'p-4 rounded-xl border-2 transition-all flex flex-col items-center gap-2',
                    theme === 'dark'
                      ? 'border-primary bg-primary/5'
                      : 'border-border'
                  )}
                >
                  <div className="w-16 h-16 bg-gray-900 border-2 border-gray-700 rounded-lg" />
                  <span className="font-medium">Escuro</span>
                </button>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-4">Cor Principal</h3>
              <div className="flex items-center gap-4">
                <input
                  type="color"
                  value={primaryColor}
                  onChange={(e) => setPrimaryColor(e.target.value)}
                  className="w-16 h-16 rounded-lg cursor-pointer"
                />
                <div>
                  <p className="font-medium">{primaryColor}</p>
                  <p className="text-sm text-muted-foreground">
                    Esta cor será usada em botões e elementos principais
                  </p>
                </div>
              </div>
            </div>
          </div>
        )

      default:
        return null
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold">Configurações</h1>
        <p className="text-muted-foreground">
          Gerencie suas preferências e configurações
        </p>
      </div>

      <div className="flex gap-6">
        {/* Sidebar */}
        <div className="w-64 flex-shrink-0">
          <nav className="space-y-1">
            {settingsTabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={cn(
                  'w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors text-left',
                  activeTab === tab.id
                    ? 'bg-primary text-primary-foreground'
                    : 'hover:bg-muted'
                )}
              >
                <tab.icon className="w-5 h-5" />
                <span className="font-medium">{tab.label}</span>
              </button>
            ))}
          </nav>
        </div>

        {/* Content */}
        <div className="flex-1 bg-card border border-border rounded-xl p-6">
          {renderTabContent()}

          <div className="mt-8 pt-6 border-t border-border flex justify-end">
            <button className="flex items-center gap-2 px-6 py-2 bg-primary text-primary-foreground rounded-lg font-medium hover:bg-primary/90 transition-colors">
              <Save className="w-5 h-5" />
              Salvar Alterações
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
