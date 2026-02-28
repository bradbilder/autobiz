import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Eye, EyeOff, Mail, Lock, User, Phone } from 'lucide-react'
import { useAuthStore } from '@/store/authStore'
import { cn } from '@/utils/helpers'

export default function Register() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    password: '',
    confirmPassword: '',
  })
  const [showPassword, setShowPassword] = useState(false)
  const [acceptTerms, setAcceptTerms] = useState(false)
  const { register, isLoading, error, clearError } = useAuthStore()
  const navigate = useNavigate()

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    clearError()

    if (formData.password !== formData.confirmPassword) {
      // TODO: Mostrar erro
      return
    }

    const success = await register(
      formData.name,
      formData.email,
      formData.password,
      formData.phone
    )

    if (success) {
      navigate('/onboarding')
    }
  }

  return (
    <div className="bg-card rounded-2xl shadow-xl p-8">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold mb-2">Criar conta</h2>
        <p className="text-muted-foreground">
          Comece a gerenciar seu negócio hoje
        </p>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-destructive/10 border border-destructive/20 rounded-lg text-destructive text-sm">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-5">
        <div>
          <label className="block text-sm font-medium mb-2">Nome completo</label>
          <div className="relative">
            <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="Seu nome"
              className="w-full pl-10 pr-4 py-3 bg-muted rounded-lg border border-transparent focus:border-primary focus:outline-none transition-colors"
              required
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Email</label>
          <div className="relative">
            <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="seu@email.com"
              className="w-full pl-10 pr-4 py-3 bg-muted rounded-lg border border-transparent focus:border-primary focus:outline-none transition-colors"
              required
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Telefone</label>
          <div className="relative">
            <Phone className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
            <input
              type="tel"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              placeholder="(00) 00000-0000"
              className="w-full pl-10 pr-4 py-3 bg-muted rounded-lg border border-transparent focus:border-primary focus:outline-none transition-colors"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Senha</label>
          <div className="relative">
            <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
            <input
              type={showPassword ? 'text' : 'password'}
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="••••••••"
              className="w-full pl-10 pr-12 py-3 bg-muted rounded-lg border border-transparent focus:border-primary focus:outline-none transition-colors"
              required
              minLength={6}
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
            >
              {showPassword ? (
                <EyeOff className="w-5 h-5" />
              ) : (
                <Eye className="w-5 h-5" />
              )}
            </button>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Confirmar senha</label>
          <div className="relative">
            <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
            <input
              type={showPassword ? 'text' : 'password'}
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              placeholder="••••••••"
              className="w-full pl-10 pr-4 py-3 bg-muted rounded-lg border border-transparent focus:border-primary focus:outline-none transition-colors"
              required
            />
          </div>
        </div>

        <label className="flex items-start gap-3 cursor-pointer">
          <input
            type="checkbox"
            checked={acceptTerms}
            onChange={(e) => setAcceptTerms(e.target.checked)}
            className="mt-1 rounded border-muted"
            required
          />
          <span className="text-sm text-muted-foreground">
            Aceito os{' '}
            <Link to="/terms" className="text-primary hover:underline">
              Termos de Serviço
            </Link>{' '}
            e{' '}
            <Link to="/privacy" className="text-primary hover:underline">
              Política de Privacidade
            </Link>
          </span>
        </label>

        <button
          type="submit"
          disabled={isLoading || !acceptTerms}
          className={cn(
            'w-full py-3 px-4 bg-primary text-primary-foreground rounded-lg font-medium transition-all',
            isLoading || !acceptTerms
              ? 'opacity-70 cursor-not-allowed'
              : 'hover:bg-primary/90 active:scale-[0.98]'
          )}
        >
          {isLoading ? 'Criando conta...' : 'Criar conta'}
        </button>
      </form>

      <p className="mt-6 text-center text-sm text-muted-foreground">
        Já tem uma conta?{' '}
        <Link to="/login" className="text-primary hover:underline font-medium">
          Entrar
        </Link>
      </p>
    </div>
  )
}
