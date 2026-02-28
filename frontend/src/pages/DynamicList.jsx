import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import {
  Plus,
  Search,
  Filter,
  MoreHorizontal,
  Edit,
  Trash2,
  Eye,
  Download,
} from 'lucide-react'
import { useTenantStore } from '@/store/tenantStore'
import { dataService } from '@/services/dataService'
import { formatDate, formatCurrency, truncate } from '@/utils/helpers'
import { cn } from '@/utils/helpers'

export default function DynamicList() {
  const { entity } = useParams()
  const navigate = useNavigate()
  const { currentTenant } = useTenantStore()
  const [data, setData] = useState({ items: [], total: 0 })
  const [isLoading, setIsLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [page, setPage] = useState(1)
  const [selectedItems, setSelectedItems] = useState([])

  useEffect(() => {
    if (currentTenant?.id && entity) {
      loadData()
    }
  }, [currentTenant, entity, page, search])

  const loadData = async () => {
    try {
      setIsLoading(true)
      const result = await dataService.list(currentTenant.id, entity, {
        page,
        page_size: 10,
        search: search || undefined,
      })
      setData(result)
    } catch (error) {
      console.error('Erro ao carregar dados:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleDelete = async (id) => {
    if (!confirm('Tem certeza que deseja excluir este item?')) return

    try {
      await dataService.delete(currentTenant.id, entity, id)
      loadData()
    } catch (error) {
      console.error('Erro ao excluir:', error)
    }
  }

  const handleSelectAll = (e) => {
    if (e.target.checked) {
      setSelectedItems(data.items.map((item) => item.id))
    } else {
      setSelectedItems([])
    }
  }

  const handleSelectItem = (id) => {
    setSelectedItems((prev) =>
      prev.includes(id) ? prev.filter((i) => i !== id) : [...prev, id]
    )
  }

  const getEntityLabel = () => {
    const labels = {
      produtos: 'Produtos',
      clientes: 'Clientes',
      vendas: 'Vendas',
      agendamentos: 'Agendamentos',
    }
    return labels[entity] || entity
  }

  const renderCell = (item, key) => {
    const value = item[key]

    if (key === 'created_at' || key === 'updated_at') {
      return formatDate(value)
    }

    if (key.includes('preco') || key.includes('valor') || key.includes('total')) {
      return formatCurrency(value || 0)
    }

    if (key === 'ativo' || key === 'status') {
      return (
        <span
          className={cn(
            'px-2 py-1 rounded-full text-xs font-medium',
            value
              ? 'bg-success/10 text-success'
              : 'bg-destructive/10 text-destructive'
          )}
        >
          {value ? 'Ativo' : 'Inativo'}
        </span>
      )
    }

    if (typeof value === 'object') {
      return JSON.stringify(value)
    }

    return truncate(String(value || '-'), 50)
  }

  const columns = data.items.length > 0
    ? Object.keys(data.items[0]).filter(
        (key) => !['id', 'tenant_id', 'senha_hash'].includes(key)
      )
    : []

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">{getEntityLabel()}</h1>
          <p className="text-muted-foreground">
            Gerencie seus {getEntityLabel().toLowerCase()}
          </p>
        </div>
        <Link
          to={`/${entity}/new`}
          className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg font-medium hover:bg-primary/90 transition-colors"
        >
          <Plus className="w-5 h-5" />
          Novo
        </Link>
      </div>

      {/* Filters */}
      <div className="flex items-center gap-4">
        <div className="flex-1 max-w-md relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder={`Buscar ${getEntityLabel().toLowerCase()}...`}
            className="w-full pl-10 pr-4 py-2 bg-card border border-border rounded-lg focus:border-primary focus:outline-none"
          />
        </div>
        <button className="flex items-center gap-2 px-4 py-2 border border-border rounded-lg hover:bg-muted transition-colors">
          <Filter className="w-5 h-5" />
          Filtros
        </button>
        <button className="flex items-center gap-2 px-4 py-2 border border-border rounded-lg hover:bg-muted transition-colors">
          <Download className="w-5 h-5" />
          Exportar
        </button>
      </div>

      {/* Table */}
      <div className="bg-card border border-border rounded-xl overflow-hidden">
        {isLoading ? (
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary" />
          </div>
        ) : data.items.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-64 text-muted-foreground">
            <Search className="w-12 h-12 mb-4 opacity-50" />
            <p>Nenhum item encontrado</p>
            <p className="text-sm">Tente ajustar seus filtros</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-muted">
                <tr>
                  <th className="px-4 py-3 text-left">
                    <input
                      type="checkbox"
                      checked={selectedItems.length === data.items.length}
                      onChange={handleSelectAll}
                      className="rounded border-muted"
                    />
                  </th>
                  {columns.map((col) => (
                    <th
                      key={col}
                      className="px-4 py-3 text-left text-sm font-medium text-muted-foreground uppercase"
                    >
                      {col.replace(/_/g, ' ')}
                    </th>
                  ))}
                  <th className="px-4 py-3 text-right">Ações</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {data.items.map((item) => (
                  <tr key={item.id} className="hover:bg-muted/50">
                    <td className="px-4 py-3">
                      <input
                        type="checkbox"
                        checked={selectedItems.includes(item.id)}
                        onChange={() => handleSelectItem(item.id)}
                        className="rounded border-muted"
                      />
                    </td>
                    {columns.map((col) => (
                      <td key={col} className="px-4 py-3">
                        {renderCell(item, col)}
                      </td>
                    ))}
                    <td className="px-4 py-3 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <Link
                          to={`/${entity}/${item.id}`}
                          className="p-2 hover:bg-muted rounded-lg transition-colors"
                        >
                          <Eye className="w-4 h-4" />
                        </Link>
                        <Link
                          to={`/${entity}/${item.id}/edit`}
                          className="p-2 hover:bg-muted rounded-lg transition-colors"
                        >
                          <Edit className="w-4 h-4" />
                        </Link>
                        <button
                          onClick={() => handleDelete(item.id)}
                          className="p-2 hover:bg-destructive/10 text-destructive rounded-lg transition-colors"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Pagination */}
        {!isLoading && data.items.length > 0 && (
          <div className="flex items-center justify-between px-4 py-3 border-t border-border">
            <p className="text-sm text-muted-foreground">
              Mostrando {(page - 1) * 10 + 1} a {Math.min(page * 10, data.total)} de{' '}
              {data.total} resultados
            </p>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page === 1}
                className="px-3 py-1 border border-border rounded-lg disabled:opacity-50 hover:bg-muted transition-colors"
              >
                Anterior
              </button>
              <button
                onClick={() => setPage((p) => p + 1)}
                disabled={page >= data.total_pages}
                className="px-3 py-1 border border-border rounded-lg disabled:opacity-50 hover:bg-muted transition-colors"
              >
                Próximo
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
