import { defineStore } from 'pinia'
import api from '../api'
import router from '../router'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('ct_token') || null,
    user: JSON.parse(localStorage.getItem('ct_user') || 'null'),
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    userEmail: (state) => state.user?.email || null,
    userRole: (state) => state.user?.role || null,
  },

  actions: {
    async login(email, password) {
      const response = await api.post('/auth/login', { email, password })
      const { token, email: userEmail, role } = response.data

      this.token = token
      this.user = { email: userEmail, role }

      localStorage.setItem('ct_token', token)
      localStorage.setItem('ct_user', JSON.stringify(this.user))

      return true
    },

    logout() {
      this.token = null
      this.user = null

      localStorage.removeItem('ct_token')
      localStorage.removeItem('ct_user')

      router.push('/login')
    },
  },
})
