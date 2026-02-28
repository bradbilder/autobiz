import { Outlet } from 'react-router-dom'

export default function AuthLayout() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-primary-100 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-primary mb-2">Autobiz</h1>
          <p className="text-muted-foreground">
            Sistema auto-modelável para gestão de negócios
          </p>
        </div>
        <Outlet />
      </div>
    </div>
  )
}
