<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import PublicLayout from '../layouts/PublicLayout.vue'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleSubmit() {
  loading.value = true
  error.value = ''
  try {
    await authStore.login(email.value, password.value)
    router.push('/dashboard')
  } catch {
    error.value = 'Invalid email or password'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <PublicLayout>
    <div class="auth-wrap">
      <div class="auth-left">
        <div class="flex items-c gap-10" style="margin-bottom:40px">
          <div class="logo-icon"><i class="ti ti-activity-heartbeat"></i></div>
          <div><div class="logo-name" style="color:#E2E8F0">CardioTriage</div><div class="logo-sub">Clinical Platform</div></div>
        </div>
        <svg width="100%" height="55" viewBox="0 0 400 55" preserveAspectRatio="none" style="margin-bottom:28px">
          <polyline points="0,27 38,27 44,27 50,9 53,46 56,27 100,27 106,8 109,47 112,27 158,27 164,9 167,46 170,27 216,27 222,8 225,47 228,27 274,27 280,9 283,46 286,27 332,27 338,8 341,47 344,27 390,27 395,9 398,46 400,27"
            fill="none" stroke="#1E4A6E" stroke-width="1.6"/>
        </svg>
        <div class="auth-h1">Clinical triage,<br>powered by AI.</div>
        <div class="auth-p" style="margin-top:14px">Upload wearable ECG recordings and get instant triage assessment — severity, rhythm, and vital signs in seconds.</div>
        <div class="auth-warn"><i class="ti ti-alert-triangle" style="font-size:15px;flex-shrink:0"></i>Educational project · Not for clinical use</div>
      </div>
      <div class="auth-right">
        <div class="auth-form">
          <div class="auth-title">Welcome back</div>
          <div class="auth-sub">Sign in to your CardioTriage account</div>
          <form @submit.prevent="handleSubmit">
            <div class="form-group"><div class="form-label">Email address</div><input v-model="email" class="form-input" type="email" placeholder="doctor@cardiotriage.com" required></div>
            <div class="form-group"><div class="form-label">Password</div><input v-model="password" class="form-input" type="password" placeholder="••••••••" required></div>
            <p v-if="error" style="color:var(--red-text);font-size:12px;margin-bottom:12px;">{{ error }}</p>
            <button class="btn primary full" type="submit" :disabled="loading" style="margin-top:4px">{{ loading ? 'Signing in…' : 'Sign in' }}</button>
          </form>
          <div class="auth-lnk">Don't have an account? <span @click="router.push('/register')">Register →</span></div>
        </div>
      </div>
    </div>
  </PublicLayout>
</template>
