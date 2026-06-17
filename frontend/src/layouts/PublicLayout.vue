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
  <div style="height:100%;background:var(--bg-page)">
    <slot />
  </div>
</template>
