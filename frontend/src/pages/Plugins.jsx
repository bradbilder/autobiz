import { useState, useEffect } from 'react'
import { useTenantStore } from '@/store/tenantStore'
import {
  Puzzle,
  Download,
  Check,
  Settings,
  Trash2,
  Search,
  Star,
} from 'lucide-react'
import { cn } from '@/utils/helpers'

// Plugins de exemplo
const availablePlugins = [
  {
    id: 'advanced_reports',
    name: 'Relatórios Avançados',
    description: 'Relatórios customizados com exportação para PDF e Excel',
    author: 'Autobiz',
    version: '1.0.0',
    category: 'Relatórios',
    rating: 4.8,
    installs: 1250,
    installed: false,
  },
  {
    id: 'sms_notifications',
    name: 'Notificações SMS',
    description: 'Envie notificações por SMS para seus clientes',
    author: 'Autobiz',
    version: '1.0.0',
    category: 'Comunicação',
    rating: 4.5,
    installs: 890,
    installed: false,
  },
  {
    id: 'loyalty_program',
    name: 'Programa de Fidelidade',
    description: 'Sistema de pontos e recompensas para clientes',
    author: 'Autobiz',
    version: '1.0.0',
    category: 'Marketing',
    rating: 4.9,
    installs: 2100,
    installed: true,
  },
  {
    id: 'multi_branch',
    name: 'Multi-filial',
    description: 'Gerencie múltiplas filiais em um único sistema',
    author: 'Autobiz',
    version: '1.0.0',
    category: 'Gestão',
    rating: 4.7,
    installs: 650,
    installed: false,
  },
  {
    id: 'automation',
    name: 'Automação',
    description: 'Automatize tarefas repetitivas e workflows',
    author: 'Autobiz',
    version: '1.0.0',
    category: 'Produtividade',
    rating: 4.6,
    installs: 1500,
    installed: false,
  },
]

export default function Plugins() {
  const [search, setSearch] = useState('')
  const [activeCategory, setActiveCategory] = useState('all')
  const [plugins, setPlugins] = useState(availablePlugins)

  const categories = ['all', ...new Set(availablePlugins.map((p) => p.category))]

  const filteredPlugins = plugins.filter((plugin) => {
    const matchesSearch =
      plugin.name.toLowerCase().includes(search.toLowerCase()) ||
      plugin.description.toLowerCase().includes(search.toLowerCase())
    const matchesCategory =
      activeCategory === 'all' || plugin.category === activeCategory
    return matchesSearch && matchesCategory
  })

  const handleInstall = (pluginId) => {
    setPlugins((prev) =>
      prev.map((p) => (p.id === pluginId ? { ...p, installed: true } : p))
    )
  }

  const handleUninstall = (pluginId) => {
    setPlugins((prev) =>
      prev.map((p) => (p.id === pluginId ? { ...p, installed: false } : p))
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Plugins</h1>
          <p className="text-muted-foreground">
            Estenda as funcionalidades do seu sistema
          </p>
        </div>
      </div>

      {/* Filters */}
      <div className="flex items-center gap-4">
        <div className="flex-1 max-w-md relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Buscar plugins..."
            className="w-full pl-10 pr-4 py-2 bg-card border border-border rounded-lg focus:border-primary focus:outline-none"
          />
        </div>
        <select
          value={activeCategory}
          onChange={(e) => setActiveCategory(e.target.value)}
          className="px-4 py-2 bg-card border border-border rounded-lg"
        >
          <option value="all">Todas as categorias</option>
          {categories
            .filter((c) => c !== 'all')
            .map((cat) => (
              <option key={cat} value={cat}>
                {cat}
              </option>
            ))}
        </select>
      </div>

      {/* Installed Plugins */}
      <div>
        <h2 className="text-lg font-semibold mb-4">Plugins Instalados</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {plugins
            .filter((p) => p.installed)
            .map((plugin) => (
              <div
                key={plugin.id}
                className="bg-card border border-border rounded-xl p-6"
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center">
                      <Puzzle className="w-6 h-6 text-primary" />
                    </div>
                    <div>
                      <h3 className="font-semibold">{plugin.name}</h3>
                      <p className="text-sm text-muted-foreground">
                        {plugin.category} • v{plugin.version}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <button className="p-2 hover:bg-muted rounded-lg transition-colors">
                      <Settings className="w-5 h-5" />
                    </button>
                    <button
                      onClick={() => handleUninstall(plugin.id)}
                      className="p-2 hover:bg-destructive/10 text-destructive rounded-lg transition-colors"
                    >
                      <Trash2 className="w-5 h-5" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
        </div>
      </div>

      {/* Available Plugins */}
      <div>
        <h2 className="text-lg font-semibold mb-4">Plugins Disponíveis</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filteredPlugins
            .filter((p) => !p.installed)
            .map((plugin) => (
              <div
                key={plugin.id}
                className="bg-card border border-border rounded-xl p-6"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center">
                      <Puzzle className="w-6 h-6 text-primary" />
                    </div>
                    <div>
                      <h3 className="font-semibold">{plugin.name}</h3>
                      <p className="text-sm text-muted-foreground">
                        {plugin.category} • v{plugin.version}
                      </p>
                    </div>
                  </div>
                </div>

                <p className="text-muted-foreground mb-4">{plugin.description}</p>

                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4 text-sm text-muted-foreground">
                    <div className="flex items-center gap-1">
                      <Star className="w-4 h-4 text-warning fill-warning" />
                      <span>{plugin.rating}</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <Download className="w-4 h-4" />
                      <span>{plugin.installs.toLocaleString()}</span>
                    </div>
                  </div>
                  <button
                    onClick={() => handleInstall(plugin.id)}
                    className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
                  >
                    <Download className="w-4 h-4" />
                    Instalar
                  </button>
                </div>
              </div>
            ))}
        </div>
      </div>
    </div>
  )
}
