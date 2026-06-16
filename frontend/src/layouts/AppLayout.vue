<script setup>
import { computed, onMounted, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { useThemeStore } from '../stores/theme'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const themeStore = useThemeStore()
const authStore = useAuthStore()

function applyDark(isDark) {
  if (isDark) {
    document.documentElement.setAttribute('data-dark', '')
  } else {
    document.documentElement.removeAttribute('data-dark')
  }
}

onMounted(() => applyDark(themeStore.isDark))
watch(() => themeStore.isDark, applyDark)

const isPatientsActive = computed(() =>
  route.path.startsWith('/patients') || route.path.startsWith('/recordings')
)

const displayName = computed(() => {
  const local = (authStore.userEmail || '').split('@')[0]
  const name = local.split(/[._]/).filter(Boolean)
    .map(w => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ')
  return name.length > 18 ? name.slice(0, 18) + '…' : name
})

const avatarInitials = computed(() => {
  const local = (authStore.userEmail || '').split('@')[0]
  const words = local.split(/[._]/).filter(Boolean)
  if (words.length >= 2) return (words[0][0] + words[1][0]).toUpperCase()
  return (words[0] || '??').slice(0, 2).toUpperCase()
})
</script>

<template>
  <div class="flex h-screen overflow-hidden" :data-dark="themeStore.isDark ? '' : null">
    <aside class="sidebar">
      <div class="sb-logo">
        <div class="sb-logo-icon">
          <svg viewBox="0 0 24 24"><polyline points="2,12 6,12 9,4 12,20 15,8 18,16 21,12" /></svg>
        </div>
        <div>
          <div class="sb-logo-name">CardioTriage</div>
          <div class="sb-logo-sub">Clinical Platform</div>
        </div>
      </div>

      <div class="sb-ecg">
        <svg width="158" height="22" viewBox="0 0 158 22">
          <polyline
            points="0,11 16,11 23,4 27,19 31,1 35,20 39,11 65,11 72,4 76,19 80,1 84,20 88,11 158,11"
            stroke="#22D3EE" stroke-width="1.2" fill="none" opacity="0.35"
          />
        </svg>
      </div>

      <nav class="sb-nav">
        <RouterLink to="/dashboard" :class="{ active: route.path === '/dashboard' }">
          <svg viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" /><rect x="14" y="3" width="7" height="7" /><rect x="3" y="14" width="7" height="7" /><rect x="14" y="14" width="7" height="7" /></svg>
          Dashboard
        </RouterLink>
        <RouterLink to="/patients" :class="{ active: isPatientsActive }">
          <svg viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" /><circle cx="9" cy="7" r="4" /><path d="M23 21v-2a4 4 0 0 0-3-3.87" /><path d="M16 3.13a4 4 0 0 1 0 7.75" /></svg>
          Patients
        </RouterLink>
        <RouterLink to="/live" :class="{ active: route.path === '/live' }">
          <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="2" /><path d="M16.24 7.76a6 6 0 0 1 0 8.49" /><path d="M7.76 16.24a6 6 0 0 1 0-8.49" /><path d="M20.07 4.93a10 10 0 0 1 0 14.14" /><path d="M3.93 19.07a10 10 0 0 1 0-14.14" /></svg>
          Live Demo
        </RouterLink>
      </nav>

      <div class="sb-bottom">
        <div class="sb-user">
          <div class="sb-avatar">{{ avatarInitials }}</div>
          <div>
            <div class="sb-user-name">{{ displayName }}</div>
            <div class="sb-user-role">{{ authStore.userRole ?? 'CLINICIAN' }}</div>
          </div>
        </div>
        <button class="sb-theme-btn" @click="themeStore.toggle">
          {{ themeStore.isDark ? '☀ Switch to light' : '🌙 Switch to dark' }}
        </button>
      </div>
    </aside>

    <div class="main">
      <div class="warning-banner">
        ⚠ Educational project — not for clinical use
      </div>
      <div class="page-content">
        <slot />
      </div>
    </div>
  </div>
</template>
