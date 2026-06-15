import { defineStore } from 'pinia'

export const useThemeStore = defineStore('theme', {
  state: () => ({
    isDark: localStorage.getItem('ct_dark') !== 'false',
  }),

  actions: {
    toggle() {
      this.isDark = !this.isDark
      localStorage.setItem('ct_dark', String(this.isDark))
    },
  },
})
