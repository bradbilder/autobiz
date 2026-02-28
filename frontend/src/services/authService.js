import api from './api'

export const authService = {
  login: async (email, password) => {
    const formData = new FormData()
    formData.append('username', email)
    formData.append('password', password)
    
    const response = await api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  register: async (name, email, password, phone) => {
    const response = await api.post('/auth/register', {
      name,
      email,
      password,
      phone,
    })
    return response.data
  },

  logout: async () => {
    await api.post('/auth/logout')
  },

  getMe: async () => {
    const response = await api.get('/auth/me')
    return response.data
  },

  refreshToken: async (refreshToken) => {
    const response = await api.post('/auth/refresh', { refresh_token: refreshToken })
    return response.data
  },

  forgotPassword: async (email) => {
    const response = await api.post('/auth/forgot-password', { email })
    return response.data
  },

  changePassword: async (currentPassword, newPassword) => {
    const response = await api.post('/auth/change-password', {
      current_password: currentPassword,
      new_password: newPassword,
    })
    return response.data
  },
}
