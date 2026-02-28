import { NavLink, useParams } from 'react-router-dom'
import {
  LayoutDashboard,
  ShoppingCart,
  Package,
  Users,
  Calendar,
  BarChart3,
  Settings,
  Plug,
  Link,
  ChevronLeft,
  ChevronRight,
  Building2,
  UserCog,
} from 'lucide-react'
import { useThemeStore } from '@/store/themeStore'
import { useAuthStore } from '@/store/authStore'
import { cn } from '@/utils/helpers'

const menuItems = [
  { icon: LayoutDashboard, label: 'Dashboard', path: '/' },
  { icon: ShoppingCart, label: 'Vendas', path: '/vendas' },
  { icon: Package, label: 'Produtos', path: '/produtos' },
  { icon: Users, label: 'Clientes', path: '/clientes' },
  { icon: Calendar, label: 'Agenda', path: '/agenda' },
  { icon: BarChart3, label: 'Relatórios', path: '/relatorios' },
]

const configItems = [
  { icon: Link, label: 'Integrações', path: '/integracoes' },
  { icon: Plug, label: 'Plugins', path: '/plugins' },
  { icon: Settings, label: 'Configurações', path: '/configuracoes' },
]

const adminItems = [
  { icon: Building2, label: 'Tenants', path: '/admin/tenants' },
  { icon: UserCog, label: 'Usuários', path: '/admin/users' },
]

export default function Sidebar() {
  const { sidebarCollapsed, toggleSidebar } = useThemeStore()
  const { user } = useAuthStore()
  const isAdmin = user?.is_master_admin

  return (
    <aside
      className={cn(
        'fixed left-0 top-0 h-full bg-card border-r border-border z-50 transition-all duration-300',
        sidebarCollapsed ? 'w-20' : 'w-64'
      )}
    >
      {/* Logo */}
      <div className="h-16 flex items-center justify-between px-4 border-b border-border">
        {!sidebarCollapsed && (
          <NavLink to="/" className="flex items-center gap-2">
            <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
              <span className="text-primary-foreground font-bold text-lg">A</span>
            </div>
            <span className="font-bold text-xl">Autobiz</span>
          </NavLink>
        )}
        {sidebarCollapsed && (
          <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center mx-auto">
            <span className="text-primary-foreground font-bold text-lg">A</span>
          </div>
        )}
        {!sidebarCollapsed && (
          <button
            onClick={toggleSidebar}
            className="p-1 rounded-lg hover:bg-muted transition-colors"
          >
            <ChevronLeft className="w-5 h-5" />
          </button>
        )}
      </div>

      {/* Toggle button when collapsed */}
      {sidebarCollapsed && (
        <button
          onClick={toggleSidebar}
          className="absolute -right-3 top-20 w-6 h-6 bg-primary rounded-full flex items-center justify-center text-primary-foreground shadow-lg"
        >
          <ChevronRight className="w-4 h-4" />
        </button>
      )}

      {/* Navigation */}
      <nav className="p-4 space-y-1 overflow-y-auto h-[calc(100%-4rem)]">
        {/* Main Menu */}
        <div className="space-y-1">
          {!sidebarCollapsed && (
            <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-2 px-3">
              Menu Principal
            </p>
          )}
          {menuItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                cn(
                  'flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors',
                  isActive
                    ? 'bg-primary text-primary-foreground'
                    : 'text-muted-foreground hover:bg-muted hover:text-foreground',
                  sidebarCollapsed && 'justify-center'
                )
              }
            >
              <item.icon className="w-5 h-5 flex-shrink-0" />
              {!sidebarCollapsed && <span className="font-medium">{item.label}</span>}
            </NavLink>
          ))}
        </div>

        {/* Configuration */}
        <div className="mt-6 space-y-1">
          {!sidebarCollapsed && (
            <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-2 px-3">
              Configurações
            </p>
          )}
          {configItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                cn(
                  'flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors',
                  isActive
                    ? 'bg-primary text-primary-foreground'
                    : 'text-muted-foreground hover:bg-muted hover:text-foreground',
                  sidebarCollapsed && 'justify-center'
                )
              }
            >
              <item.icon className="w-5 h-5 flex-shrink-0" />
              {!sidebarCollapsed && <span className="font-medium">{item.label}</span>}
            </NavLink>
          ))}
        </div>

        {/* Admin Section */}
        {isAdmin && (
          <div className="mt-6 space-y-1">
            {!sidebarCollapsed && (
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-2 px-3">
                Administração
              </p>
            )}
            {adminItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  cn(
                    'flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors',
                    isActive
                      ? 'bg-primary text-primary-foreground'
                      : 'text-muted-foreground hover:bg-muted hover:text-foreground',
                    sidebarCollapsed && 'justify-center'
                  )
                }
              >
                <item.icon className="w-5 h-5 flex-shrink-0" />
                {!sidebarCollapsed && <span className="font-medium">{item.label}</span>}
              </NavLink>
            ))}
          </div>
        )}
      </nav>
    </aside>
  )
}
