import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { ChevronRight, ChevronLeft, Check, Building2, Palette, Plug } from 'lucide-react'
import { tenantService } from '@/services/tenantService'
import { useTenantStore } from '@/store/tenantStore'
import { cn } from '@/utils/helpers'

const businessTypes = [
  { id: 'varejo', label: 'Varejo/Loja', icon: '🏪' },
  { id: 'ecommerce', label: 'E-commerce', icon: '🛒' },
  { id: 'servicos', label: 'Prestação de Serviços', icon: '🔧' },
  { id: 'consultoria', label: 'Consultoria', icon: '💼' },
  { id: 'restaurante', label: 'Restaurante', icon: '🍽️' },
  { id: 'clinica', label: 'Clínica Médica', icon: '🏥' },
  { id: 'imobiliaria', label: 'Imobiliária', icon: '🏠' },
  { id: 'construcao', label: 'Construção Civil', icon: '🏗️' },
  { id: 'escola', label: 'Escola/Instituição', icon: '🎓' },
  { id: 'academia', label: 'Academia', icon: '💪' },
  { id: 'salao', label: 'Salão de Beleza', icon: '✂️' },
  { id: 'oficina', label: 'Oficina Mecânica', icon: '🔩' },
]

const features = [
  { id: 'vendas', label: 'Controle de Vendas', icon: Shopping2 },
  { id: 'estoque', label: 'Gestão de Estoque', icon: Package },
  { id: 'clientes', label: 'Cadastro de Clientes', icon: Users },
  { id: 'agendamentos', label: 'Agendamentos', icon: Calendar },
  { id: 'financeiro', label: 'Controle Financeiro', icon: DollarSign },
  { id: 'relatorios', label: 'Relatórios', icon: BarChart },
  { id: 'usuarios', label: 'Multi-usuários', icon: UserPlus },
  { id: 'api', label: 'API de Integração', icon: Code },
]

import { ShoppingCart, Package, Users, Calendar, DollarSign, BarChart3, UserPlus, Code } from 'lucide-react'

export default function Onboarding() {
  const [step, setStep] = useState(0)
  const [isLoading, setIsLoading] = useState(false)
  const [formData, setFormData] = useState({
    business_type: '',
    name: '',
    business_size: 'small',
    document: '',
    phone: '',
    email: '',
    features: [],
    primary_color: '#2563eb',
    integrations: [],
  })
  const navigate = useNavigate()
  const { setCurrentTenant } = useTenantStore()

  const steps = [
    { title: 'Tipo de Negócio', icon: Building2 },
    { title: 'Informações', icon: Building2 },
    { title: 'Funcionalidades', icon: Check },
    { title: 'Personalização', icon: Palette },
    { title: 'Integrações', icon: Plug },
  ]

  const handleBusinessTypeSelect = (type) => {
    setFormData((prev) => ({ ...prev, business_type: type }))
    setStep(1)
  }

  const handleFeatureToggle = (featureId) => {
    setFormData((prev) => ({
      ...prev,
      features: prev.features.includes(featureId)
        ? prev.features.filter((f) => f !== featureId)
        : [...prev.features, featureId],
    }))
  }

  const handleIntegrationToggle = (integrationId) => {
    setFormData((prev) => ({
      ...prev,
      integrations: prev.integrations.includes(integrationId)
        ? prev.integrations.filter((i) => i !== integrationId)
        : [...prev.integrations, integrationId],
    }))
  }

  const handleSubmit = async () => {
    setIsLoading(true)
    try {
      const response = await tenantService.create({
        business_info: {
          business_type: formData.business_type,
          business_size: formData.business_size,
          name: formData.name,
          document: formData.document,
          phone: formData.phone,
          email: formData.email,
        },
        features: formData.features,
        branding: {
          primary_color: formData.primary_color,
        },
        integrations: formData.integrations,
      })

      if (response.tenant_id) {
        setCurrentTenant(response.system_config.tenant)
        navigate('/')
      }
    } catch (error) {
      console.error('Erro ao criar sistema:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const renderStep = () => {
    switch (step) {
      case 0:
        return (
          <div className="space-y-6">
            <div className="text-center">
              <h2 className="text-2xl font-bold mb-2">Qual é o seu tipo de negócio?</h2>
              <p className="text-muted-foreground">
                Selecione a categoria que melhor descreve sua empresa
              </p>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              {businessTypes.map((type) => (
                <button
                  key={type.id}
                  onClick={() => handleBusinessTypeSelect(type.id)}
                  className={cn(
                    'p-6 rounded-xl border-2 transition-all text-center hover:border-primary hover:bg-primary/5',
                    formData.business_type === type.id
                      ? 'border-primary bg-primary/5'
                      : 'border-border'
                  )}
                >
                  <span className="text-4xl mb-3 block">{type.icon}</span>
                  <span className="font-medium">{type.label}</span>
                </button>
              ))}
            </div>
          </div>
        )

      case 1:
        return (
          <div className="space-y-6">
            <div className="text-center">
              <h2 className="text-2xl font-bold mb-2">Informações da Empresa</h2>
              <p className="text-muted-foreground">Conte-nos um pouco sobre sua empresa</p>
            </div>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Nome da Empresa</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData((prev) => ({ ...prev, name: e.target.value }))}
                  placeholder="Ex: Minha Empresa LTDA"
                  className="w-full px-4 py-3 bg-muted rounded-lg border border-transparent focus:border-primary focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Tamanho da Empresa</label>
                <select
                  value={formData.business_size}
                  onChange={(e) => setFormData((prev) => ({ ...prev, business_size: e.target.value }))}
                  className="w-full px-4 py-3 bg-muted rounded-lg border border-transparent focus:border-primary focus:outline-none"
                >
                  <option value="small">Pequena (1-10 funcionários)</option>
                  <option value="medium">Média (11-50 funcionários)</option>
                  <option value="large">Grande (51+ funcionários)</option>
                </select>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">CNPJ/CPF</label>
                  <input
                    type="text"
                    value={formData.document}
                    onChange={(e) => setFormData((prev) => ({ ...prev, document: e.target.value }))}
                    placeholder="00.000.000/0000-00"
                    className="w-full px-4 py-3 bg-muted rounded-lg border border-transparent focus:border-primary focus:outline-none"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Telefone</label>
                  <input
                    type="text"
                    value={formData.phone}
                    onChange={(e) => setFormData((prev) => ({ ...prev, phone: e.target.value }))}
                    placeholder="(00) 00000-0000"
                    className="w-full px-4 py-3 bg-muted rounded-lg border border-transparent focus:border-primary focus:outline-none"
                  />
                </div>
              </div>
            </div>
          </div>
        )

      case 2:
        return (
          <div className="space-y-6">
            <div className="text-center">
              <h2 className="text-2xl font-bold mb-2">Quais funcionalidades você precisa?</h2>
              <p className="text-muted-foreground">Selecione os recursos que deseja utilizar</p>
            </div>
            <div className="grid grid-cols-2 gap-4">
              {features.map((feature) => (
                <button
                  key={feature.id}
                  onClick={() => handleFeatureToggle(feature.id)}
                  className={cn(
                    'p-4 rounded-xl border-2 transition-all flex items-center gap-3',
                    formData.features.includes(feature.id)
                      ? 'border-primary bg-primary/5'
                      : 'border-border hover:border-primary/50'
                  )}
                >
                  <feature.icon className="w-5 h-5" />
                  <span className="font-medium">{feature.label}</span>
                  {formData.features.includes(feature.id) && (
                    <Check className="w-5 h-5 text-primary ml-auto" />
                  )}
                </button>
              ))}
            </div>
          </div>
        )

      case 3:
        return (
          <div className="space-y-6">
            <div className="text-center">
              <h2 className="text-2xl font-bold mb-2">Personalização</h2>
              <p className="text-muted-foreground">Personalize a aparência do seu sistema</p>
            </div>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Cor Principal</label>
                <div className="flex items-center gap-4">
                  <input
                    type="color"
                    value={formData.primary_color}
                    onChange={(e) => setFormData((prev) => ({ ...prev, primary_color: e.target.value }))}
                    className="w-16 h-16 rounded-lg cursor-pointer"
                  />
                  <div>
                    <p className="font-medium">{formData.primary_color}</p>
                    <p className="text-sm text-muted-foreground">
                      Esta cor será usada em botões, links e elementos principais
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )

      case 4:
        return (
          <div className="space-y-6">
            <div className="text-center">
              <h2 className="text-2xl font-bold mb-2">Integrações</h2>
              <p className="text-muted-foreground">Quais integrações você gostaria de configurar?</p>
            </div>
            <div className="space-y-3">
              {[
                { id: 'whatsapp', label: 'WhatsApp Business', description: 'Envie mensagens e notificações' },
                { id: 'mercadopago', label: 'Mercado Pago', description: 'Receba pagamentos online' },
                { id: 'google_calendar', label: 'Google Calendar', description: 'Sincronize agendamentos' },
                { id: 'email', label: 'Email Marketing', description: 'Envie campanhas de email' },
              ].map((integration) => (
                <button
                  key={integration.id}
                  onClick={() => handleIntegrationToggle(integration.id)}
                  className={cn(
                    'w-full p-4 rounded-xl border-2 transition-all flex items-center justify-between',
                    formData.integrations.includes(integration.id)
                      ? 'border-primary bg-primary/5'
                      : 'border-border hover:border-primary/50'
                  )}
                >
                  <div className="text-left">
                    <p className="font-medium">{integration.label}</p>
                    <p className="text-sm text-muted-foreground">{integration.description}</p>
                  </div>
                  {formData.integrations.includes(integration.id) && (
                    <Check className="w-5 h-5 text-primary" />
                  )}
                </button>
              ))}
            </div>
          </div>
        )

      default:
        return null
    }
  }

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <div className="w-full max-w-3xl">
        {/* Progress */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            {steps.map((s, index) => (
              <div key={index} className="flex items-center">
                <div
                  className={cn(
                    'w-10 h-10 rounded-full flex items-center justify-center transition-colors',
                    index <= step
                      ? 'bg-primary text-primary-foreground'
                      : 'bg-muted text-muted-foreground'
                  )}
                >
                  {index < step ? (
                    <Check className="w-5 h-5" />
                  ) : (
                    <s.icon className="w-5 h-5" />
                  )}
                </div>
                {index < steps.length - 1 && (
                  <div
                    className={cn(
                      'w-16 h-1 mx-2 transition-colors',
                      index < step ? 'bg-primary' : 'bg-muted'
                    )}
                  />
                )}
              </div>
            ))}
          </div>
          <div className="text-center">
            <p className="text-sm text-muted-foreground">
              Passo {step + 1} de {steps.length}: {steps[step].title}
            </p>
          </div>
        </div>

        {/* Content */}
        <div className="bg-card border border-border rounded-2xl p-8">
          {renderStep()}

          {/* Navigation */}
          <div className="flex justify-between mt-8">
            <button
              onClick={() => setStep((prev) => Math.max(0, prev - 1))}
              disabled={step === 0}
              className={cn(
                'flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-colors',
                step === 0
                  ? 'opacity-50 cursor-not-allowed'
                  : 'hover:bg-muted'
              )}
            >
              <ChevronLeft className="w-5 h-5" />
              Voltar
            </button>

            {step < steps.length - 1 ? (
              <button
                onClick={() => setStep((prev) => prev + 1)}
                disabled={step === 0 && !formData.business_type}
                className={cn(
                  'flex items-center gap-2 px-6 py-3 bg-primary text-primary-foreground rounded-lg font-medium transition-colors',
                  step === 0 && !formData.business_type
                    ? 'opacity-50 cursor-not-allowed'
                    : 'hover:bg-primary/90'
                )}
              >
                Próximo
                <ChevronRight className="w-5 h-5" />
              </button>
            ) : (
              <button
                onClick={handleSubmit}
                disabled={isLoading}
                className={cn(
                  'flex items-center gap-2 px-6 py-3 bg-primary text-primary-foreground rounded-lg font-medium transition-colors',
                  isLoading ? 'opacity-70 cursor-not-allowed' : 'hover:bg-primary/90'
                )}
              >
                {isLoading ? 'Criando...' : 'Criar Meu Sistema'}
                <Check className="w-5 h-5" />
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
