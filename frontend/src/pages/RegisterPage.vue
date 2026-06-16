<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import PublicLayout from '../layouts/PublicLayout.vue'
import { useAuthStore } from '../stores/auth'
import api from '../api'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const error = ref('')

async function handleSubmit() {
  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match'
    return
  }
  loading.value = true
  error.value = ''
  try {
    await api.post('/auth/register', {
      email: email.value,
      password: password.value,
      confirmPassword: confirmPassword.value,
    })
    await authStore.login(email.value, password.value)
    router.push('/dashboard')
  } catch {
    error.value = 'Registration failed. Email may already be in use.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <PublicLayout>
    <div style="display:grid;grid-template-columns:1fr 1fr;width:100%;height:100%;">
      <!-- Left brand panel -->
      <div style="background:#0A1120;padding:40px;display:flex;flex-direction:column;justify-content:space-between;">
        <div>
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:30px;">
            <div class="sb-logo-icon">
              <svg viewBox="0 0 24 24"><polyline points="2,12 6,12 9,4 12,20 15,8 18,16 21,12" /></svg>
            </div>
            <span style="color:#F1F5F9;font-size:15px;font-weight:500;">CardioTriage</span>
          </div>
          <svg width="240" height="46" viewBox="0 0 240 46" style="margin-bottom:24px;display:block;">
            <polyline
              points="0,23 20,23 30,8 36,38 42,3 48,42 54,23 90,23 100,8 106,38 112,3 118,42 124,23 240,23"
              stroke="#22D3EE" stroke-width="1.6" fill="none" opacity="0.5"
            />
          </svg>
          <h2 style="color:#F1F5F9;font-size:22px;font-weight:500;line-height:1.3;margin-bottom:10px;">
            Clinical triage,<br />powered by AI.
          </h2>
          <p style="color:#3D5A7A;font-size:13px;line-height:1.65;">
            Upload wearable ECG recordings and get instant triage assessment — severity, rhythm, and vital signs in seconds.
          </p>
        </div>
        <div style="padding:10px 14px;border-radius:8px;background:#1A2740;border:1px solid #2D3F55;">
          <p style="color:#FDE68A;font-size:11px;display:flex;align-items:center;gap:6px;">
            ⚠ Educational project · Not for clinical use
          </p>
        </div>
      </div>

      <!-- Right form panel -->
      <div style="background:#F8FAFC;padding:40px;display:flex;flex-direction:column;overflow-y:auto;">
        <div style="margin:auto 0;">
          <h2 style="font-size:20px;font-weight:500;color:#0F172A;margin-bottom:4px;">Create account</h2>
          <p style="font-size:13px;color:#64748B;margin-bottom:26px;">Register to access CardioTriage</p>
          <form @submit.prevent="handleSubmit">
            <div class="form-group" style="margin-bottom:14px;--bd:#CBD5E1;--su:#fff;--tx:#0F172A;">
              <label class="form-label" style="color:#374151;">Email address</label>
              <input v-model="email" class="form-input" type="email" placeholder="doctor@hospital.org" required style="border-color:#CBD5E1;background:#fff;color:#0F172A;" />
            </div>
            <div class="form-group" style="margin-bottom:14px;--bd:#CBD5E1;--su:#fff;--tx:#0F172A;">
              <label class="form-label" style="color:#374151;">Password</label>
              <input v-model="password" class="form-input" type="password" placeholder="••••••••" required minlength="8" style="border-color:#CBD5E1;background:#fff;color:#0F172A;" />
            </div>
            <div class="form-group" style="margin-bottom:20px;--bd:#CBD5E1;--su:#fff;--tx:#0F172A;">
              <label class="form-label" style="color:#374151;">Confirm password</label>
              <input v-model="confirmPassword" class="form-input" type="password" placeholder="••••••••" required style="border-color:#CBD5E1;background:#fff;color:#0F172A;" />
            </div>
            <p v-if="error" style="color:#DC2626;font-size:12px;margin-bottom:14px;">{{ error }}</p>
            <button class="btn-primary" type="submit" :disabled="loading" style="width:100%;padding:10px;font-size:13px;font-weight:500;justify-content:center;background:#0891B2;border-color:#0891B2;">
              {{ loading ? 'Creating account…' : 'Create account' }}
            </button>
          </form>
          <p style="text-align:center;font-size:13px;color:#64748B;margin-top:18px;">
            Already have an account?
            <span style="color:#0891B2;cursor:pointer;" @click="router.push('/login')">Sign in</span>
          </p>
        </div>
      </div>
    </div>
  </PublicLayout>
</template>
