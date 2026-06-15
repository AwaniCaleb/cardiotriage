<script setup>
import { onMounted, watch } from 'vue'
import { useThemeStore } from '../stores/theme'

const themeStore = useThemeStore()

function applyDark(isDark) {
  if (isDark) {
    document.documentElement.setAttribute('data-dark', '')
  } else {
    document.documentElement.removeAttribute('data-dark')
  }
}

onMounted(() => applyDark(themeStore.isDark))
watch(() => themeStore.isDark, applyDark)
</script>

<template>
  <div class="h-screen overflow-hidden" :data-dark="themeStore.isDark ? '' : null" style="background: var(--bg)">
    <slot />
  </div>
</template>
