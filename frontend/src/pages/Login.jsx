import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Eye, EyeOff, Mail, Lock } from 'lucide-react'
import { useAuthStore } from '@/store/authStore'
import { cn } from '@/utils/helpers'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const { login, isLoading, error, clearError } = useAuthStore()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    clearError()
    
    const success = await login(email, password)
    if (success) {
      navigate('/')
    }
  }

  return (
    <div className="bg-card rounded-2xl shadow-xl p-8">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold mb-2">Bem-vindo de volta</h2>
        <p className="text-muted-foreground">
          Entre com sua conta para continuar
        </p>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-destructive/10 border border-destructive/20 rounded-lg text-destructive text-sm">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-5">
        <div>
          <label className="block text-sm font-medium mb-2">Email</label>
          <div className="relative">
            <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="seu@email.com"
              className="w-full pl-10 pr-4 py-3 bg-muted rounded-lg border border-transparent focus:border-primary focus:outline-none transition-colors"
              required
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Senha</label>
          <div className="relative">
            <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
            <input
              type={showPassword ? 'text' : 'password'}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full pl-10 pr-12 py-3 bg-muted rounded-lg border border-transparent focus:border-primary focus:outline-none transition-colors"
              required
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

        <div className="flex items-center justify-between text-sm">
          <label className="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" className="rounded border-muted" />
            <span className="text-muted-foreground">Lembrar-me</span>
          </label>
          <Link
            to="/forgot-password"
            className="text-primary hover:underline"
          >
            Esqueceu a senha?
          </Link>
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className={cn(
            'w-full py-3 px-4 bg-primary text-primary-foreground rounded-lg font-medium transition-all',
            isLoading
              ? 'opacity-70 cursor-not-allowed'
              : 'hover:bg-primary/90 active:scale-[0.98]'
          )}
        >
          {isLoading ? 'Entrando...' : 'Entrar'}
        </button>
      </form>

      <p className="mt-6 text-center text-sm text-muted-foreground">
        Não tem uma conta?{' '}
        <Link to="/register" className="text-primary hover:underline font-medium">
          Criar conta
        </Link>
      </p>
    </div>
  )
}
