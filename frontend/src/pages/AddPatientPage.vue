<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AppLayout from '../layouts/AppLayout.vue'
import api from '../api'

const router = useRouter()

const name = ref('')
const age = ref('')
const gender = ref('')
const bloodType = ref('')
const conditions = ref('')
const medications = ref('')
const ecName = ref('')
const ecPhone = ref('')

const saving = ref(false)
const error = ref('')

async function handleSubmit() {
  saving.value = true
  error.value = ''
  try {
    const { data } = await api.post('/patients', {
      name: name.value,
      age: Number(age.value),
      gender: gender.value,
      bloodType: bloodType.value,
      conditions: conditions.value,
      medications: medications.value,
      emergencyContact: JSON.stringify({ name: ecName.value, phone: ecPhone.value }),
    })
    router.push(`/patients/${data.id}`)
  } catch {
    error.value = 'Failed to save patient. Please check the form and try again.'
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <AppLayout>
    <div style="margin-bottom:14px;">
      <button class="btn-secondary" style="margin-bottom:10px;font-size:11px;" @click="router.push('/patients')">← Back</button>
      <div class="page-title">Add new patient</div>
      <div class="page-sub">Fill in the patient's details below</div>
    </div>

    <form class="card" style="padding:20px;" @submit.prevent="handleSubmit">
      <div class="form-grid">
        <div class="form-group">
          <label class="form-label">Full name <span style="color:#EF4444;">*</span></label>
          <input v-model="name" class="form-input" type="text" placeholder="e.g. Amara Okafor" required />
        </div>
        <div class="form-group">
          <label class="form-label">Age <span style="color:#EF4444;">*</span></label>
          <input v-model="age" class="form-input" type="number" placeholder="e.g. 54" min="0" max="150" required />
        </div>
        <div class="form-group">
          <label class="form-label">Gender</label>
          <select v-model="gender" class="form-select">
            <option value="">Select…</option>
            <option>Male</option>
            <option>Female</option>
            <option>Other</option>
            <option>Prefer not to say</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">Blood type</label>
          <select v-model="bloodType" class="form-select">
            <option value="">Select…</option>
            <option>A+</option>
            <option>A-</option>
            <option>B+</option>
            <option>B-</option>
            <option>AB+</option>
            <option>AB-</option>
            <option>O+</option>
            <option>O-</option>
            <option>Unknown</option>
          </select>
        </div>
        <div class="form-group full">
          <label class="form-label">Known conditions</label>
          <textarea v-model="conditions" class="form-textarea" placeholder="e.g. Hypertension, Type 2 Diabetes"></textarea>
        </div>
        <div class="form-group full">
          <label class="form-label">Current medications</label>
          <textarea v-model="medications" class="form-textarea" placeholder="e.g. Lisinopril 10mg, Metformin 500mg"></textarea>
        </div>
        <div class="form-group">
          <label class="form-label">Emergency contact name</label>
          <input v-model="ecName" class="form-input" type="text" placeholder="e.g. Emeka Okafor" />
        </div>
        <div class="form-group">
          <label class="form-label">Emergency contact phone</label>
          <input v-model="ecPhone" class="form-input" type="tel" placeholder="e.g. +234 80 1234 5678" />
        </div>
      </div>

      <p v-if="error" style="color:#EF4444;font-size:12px;margin-top:14px;">{{ error }}</p>

      <div class="form-actions">
        <button class="btn-primary" type="submit" :disabled="saving">{{ saving ? 'Saving…' : 'Save patient' }}</button>
        <button class="btn-secondary" type="button" @click="router.push('/patients')">Cancel</button>
      </div>
    </form>
  </AppLayout>
</template>
