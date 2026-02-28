import axios from 'axios'
import { useAuthStore } from '@/store/authStore'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().token
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // Token expired
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      // TODO: Implementar refresh token
      // const refreshToken = useAuthStore.getState().refreshToken
      // const response = await api.post('/auth/refresh', { refresh_token: refreshToken })
      // useAuthStore.getState().setToken(response.data.access_token)
      // originalRequest.headers.Authorization = `Bearer ${response.data.access_token}`
      // return api(originalRequest)
      
      // Por enquanto, fazer logout
      useAuthStore.getState().logout()
      window.location.href = '/login'
    }

    return Promise.reject(error)
  }
)

export default api
