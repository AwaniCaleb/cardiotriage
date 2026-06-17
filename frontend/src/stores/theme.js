import { defineStore } from 'pinia'

export const useThemeStore = defineStore('theme', {
  state: () => ({
    theme: localStorage.getItem('ct-theme') || 'dark',
  }),

  getters: {
    isDark: (state) => state.theme !== 'light',
  },

  actions: {
    toggle() {
      const cycle = { light: 'dark', dark: 'night', night: 'light' }
      this.theme = cycle[this.theme] || 'dark'
      localStorage.setItem('ct-theme', this.theme)
      document.documentElement.setAttribute('data-theme', this.theme)
    },
  },
})
