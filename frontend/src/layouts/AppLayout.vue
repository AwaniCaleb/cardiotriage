<script setup>
import { RouterLink } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
</script>

<template>
  <div class="min-h-screen flex flex-col bg-gray-50">
    <header class="flex items-center justify-between px-6 py-3 bg-white border-b border-gray-200">
      <span class="text-xl font-bold text-blue-700">CardioTriage</span>
      <div class="flex items-center gap-4">
        <span class="text-sm text-gray-600">{{ authStore.userEmail }}</span>
        <button
          class="px-3 py-1.5 text-sm font-medium text-white bg-blue-600 rounded hover:bg-blue-700"
          @click="authStore.logout"
        >
          Logout
        </button>
      </div>
    </header>

    <div class="px-6 py-2 text-sm font-medium text-center text-yellow-800 bg-yellow-200">
      ⚠️ Educational project — not for clinical use
    </div>

    <div class="flex flex-1">
      <aside class="w-56 bg-white border-r border-gray-200">
        <nav class="flex flex-col gap-1 p-4">
          <RouterLink
            to="/dashboard"
            class="px-3 py-2 rounded hover:bg-blue-50"
            active-class="bg-blue-100 text-blue-700 font-semibold"
          >
            Dashboard
          </RouterLink>
          <RouterLink
            to="/patients"
            class="px-3 py-2 rounded hover:bg-blue-50"
            active-class="bg-blue-100 text-blue-700 font-semibold"
          >
            Patients
          </RouterLink>
          <RouterLink
            to="/live"
            class="px-3 py-2 rounded hover:bg-blue-50"
            active-class="bg-blue-100 text-blue-700 font-semibold"
          >
            Live Demo
          </RouterLink>
        </nav>
      </aside>

      <main class="flex-1 p-6">
        <slot />
      </main>
    </div>
  </div>
</template>
