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
    <div class="topbar">
      <div>
        <button class="btn ghost" style="margin-bottom:12px;font-size:12px;padding:6px 12px" @click="router.push('/patients')"><i class="ti ti-arrow-left"></i>Back</button>
        <div class="pg-title">Add Patient</div>
        <div class="pg-sub">Create a new patient record</div>
      </div>
    </div>

    <div class="body">
      <form @submit.prevent="handleSubmit">
        <div class="card">
          <div class="card-title"><i class="ti ti-user"></i>Patient Information</div>
          <div class="grid-2">
            <div class="form-group"><div class="form-label">Full Name *</div><input v-model="name" class="form-input" type="text" placeholder="e.g. Amara Okafor" required></div>
            <div class="form-group"><div class="form-label">Age *</div><input v-model="age" class="form-input" type="number" placeholder="e.g. 54" min="0" max="150" required></div>
          </div>
          <div class="grid-3">
            <div class="form-group"><div class="form-label">Gender</div><select v-model="gender" class="form-select"><option value="">Select…</option><option>Male</option><option>Female</option><option>Other</option><option>Prefer not to say</option></select></div>
            <div class="form-group"><div class="form-label">Blood Type</div><select v-model="bloodType" class="form-select"><option value="">Select…</option><option>A+</option><option>A-</option><option>B+</option><option>B-</option><option>AB+</option><option>AB-</option><option>O+</option><option>O-</option><option>Unknown</option></select></div>
          </div>
          <div class="form-group"><div class="form-label">Known Conditions</div><textarea v-model="conditions" class="form-textarea" placeholder="e.g. Hypertension, Type 2 Diabetes"></textarea></div>
          <div class="form-group mb-0"><div class="form-label">Current Medications</div><textarea v-model="medications" class="form-textarea" placeholder="e.g. Lisinopril 10mg, Metformin 500mg"></textarea></div>
        </div>

        <div class="card" style="margin-top:14px">
          <div class="card-title"><i class="ti ti-phone"></i>Emergency Contact</div>
          <div class="grid-2">
            <div class="form-group mb-0"><div class="form-label">Contact Name</div><input v-model="ecName" class="form-input" type="text" placeholder="e.g. Emeka Okafor"></div>
            <div class="form-group mb-0"><div class="form-label">Phone Number</div><input v-model="ecPhone" class="form-input" type="tel" placeholder="+234 80 1234 5678"></div>
          </div>
        </div>

        <p v-if="error" style="color:var(--red-text);font-size:12px;margin-top:14px;">{{ error }}</p>

        <div class="flex gap-10" style="margin-top:14px">
          <button class="btn ghost" type="button" @click="router.push('/patients')"><i class="ti ti-x"></i>Cancel</button>
          <button class="btn primary" type="submit" :disabled="saving"><i class="ti ti-check"></i>{{ saving ? 'Saving…' : 'Save Patient' }}</button>
        </div>
      </form>
    </div>
  </AppLayout>
</template>
