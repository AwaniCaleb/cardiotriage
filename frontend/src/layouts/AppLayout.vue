<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { useThemeStore } from '../stores/theme'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const themeStore = useThemeStore()
const authStore = useAuthStore()

const sidebarOpen = ref(false)

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
  <div class="app-shell" :class="{ 'sb-open': sidebarOpen }">
    <!-- Mobile backdrop -->
    <div class="sidebar-backdrop" @click="sidebarOpen = false"></div>

    <!-- Sidebar -->
    <div class="sb">
      <div class="sb-logo">
        <div class="logo-icon"><i class="ti ti-activity-heartbeat"></i></div>
        <div>
          <div class="logo-name">CardioTriage</div>
          <div class="logo-sub">Clinical Platform</div>
        </div>
      </div>

      <div class="sb-ecg">
        <svg viewBox="0 0 180 18" preserveAspectRatio="none">
          <polyline points="0,9 22,9 28,9 32,2 36,16 40,9 60,9 65,2 67,0 69,14 71,9 95,9 100,9 104,2 108,16 112,9 135,9 140,2 142,0 144,14 146,9 180,9"
            fill="none" stroke="var(--ecg-stroke)" stroke-width="1.3"/>
        </svg>
      </div>

      <div class="sb-nav" @click="sidebarOpen = false">
        <div class="nav-lbl">Menu</div>
        <RouterLink class="nav-a" to="/dashboard" :class="{ active: route.path === '/dashboard' }">
          <i class="ti ti-layout-dashboard"></i>Dashboard
        </RouterLink>
        <RouterLink class="nav-a" to="/patients" :class="{ active: isPatientsActive }">
          <i class="ti ti-users"></i>Patients
        </RouterLink>
        <RouterLink class="nav-a" to="/live" :class="{ active: route.path === '/live' }">
          <i class="ti ti-radio"></i>Live Demo
        </RouterLink>
        <div class="nav-lbl">System</div>
        <RouterLink class="nav-a" to="/team" :class="{ active: route.path === '/team' }">
          <i class="ti ti-users-group"></i>Team
        </RouterLink>
        <a class="nav-a danger" @click="authStore.logout()">
          <i class="ti ti-logout"></i>Sign out
        </a>
      </div>

      <div class="sb-footer">
        <div class="user-row">
          <div class="user-av">{{ avatarInitials }}</div>
          <div>
            <div class="user-name">{{ displayName }}</div>
            <div class="user-role">{{ authStore.userRole ?? 'CLINICIAN' }}</div>
          </div>
          <button class="theme-cycle-btn" @click="themeStore.toggle()" :title="'Switch theme (' + themeStore.theme + ')'">
            <i :class="themeStore.theme === 'light' ? 'ti ti-moon' : themeStore.theme === 'night' ? 'ti ti-sun' : 'ti ti-brightness-down'"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- Main content -->
    <div class="main">
      <button class="hamburger-btn" @click="sidebarOpen = !sidebarOpen" aria-label="Open menu">
        <i class="ti ti-menu-2"></i>
      </button>
      <slot />
    </div>
  </div>
</template>
