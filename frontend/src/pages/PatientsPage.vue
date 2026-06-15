<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import AppLayout from '../layouts/AppLayout.vue'
import api from '../api'
import { formatRelativeTime, severityBadgeClass } from '../utils/format'

const router = useRouter()
const loading = ref(true)
const patients = ref([])
const search = ref('')

const filteredPatients = computed(() => {
  if (!search.value.trim()) return patients.value
  const q = search.value.trim().toLowerCase()
  return patients.value.filter((p) => p.name.toLowerCase().includes(q))
})

async function loadPatients() {
  loading.value = true
  try {
    const { data } = await api.get('/patients')
    patients.value = await Promise.all(
      data.map(async (p) => {
        try {
          const { data: recs } = await api.get(`/patients/${p.id}/recordings`)
          return { ...p, lastRecording: recs[0] ?? null }
        } catch {
          return { ...p, lastRecording: null }
        }
      })
    )
  } catch {
    patients.value = []
  } finally {
    loading.value = false
  }
}

onMounted(loadPatients)

function goToEdit(id) {
  router.push(`/patients/${id}/edit`)
}

async function deletePatient(id) {
  if (!window.confirm('Delete this patient? This cannot be undone.')) return
  try {
    await api.delete(`/patients/${id}`)
    patients.value = patients.value.filter((p) => p.id !== id)
  } catch {
    window.alert('Failed to delete patient.')
  }
}
</script>

<template>
  <AppLayout>
    <div class="page-header">
      <div>
        <div class="page-title">Patients</div>
        <div class="page-sub">{{ patients.length }} records total</div>
      </div>
      <button class="btn-primary" @click="router.push('/patients/new')">+ Add patient</button>
    </div>

    <div class="search-wrap">
      <span class="search-icon">🔍</span>
      <input type="text" v-model="search" placeholder="Search patients by name..." />
    </div>

    <div v-if="loading" style="display:flex;justify-content:center;padding:40px 0;">
      <div class="animate-spin" style="width:24px;height:24px;border:2px solid var(--bd);border-top-color:var(--ac);border-radius:50%;"></div>
    </div>

    <div v-else-if="patients.length === 0" class="card" style="padding:32px;text-align:center;color:var(--tm);font-size:13px;">
      No patients yet. Add your first patient.
    </div>

    <div v-else-if="filteredPatients.length === 0" class="card" style="padding:32px;text-align:center;color:var(--tm);font-size:13px;">
      No patients match your search.
    </div>

    <div v-else class="card">
      <table class="data-table">
        <thead>
          <tr>
            <th style="width:28%;">Name</th>
            <th style="width:11%;">Age</th>
            <th style="width:16%;">Gender</th>
            <th style="width:22%;">Last recording</th>
            <th style="width:23%;">Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in filteredPatients" :key="p.id" @click="router.push(`/patients/${p.id}`)">
            <td style="font-weight:500;">{{ p.name }}</td>
            <td>{{ p.age }}</td>
            <td>{{ p.gender || '—' }}</td>
            <td style="color:var(--tm);font-size:12px;">{{ p.lastRecording ? formatRelativeTime(p.lastRecording.uploadedAt) : '—' }}</td>
            <td>
              <div style="display:flex;align-items:center;justify-content:space-between;gap:6px;">
                <span class="badge" :class="severityBadgeClass(p.lastRecording?.triageResult?.severity)">
                  {{ p.lastRecording?.triageResult?.severity ?? 'No result' }}
                </span>
                <div style="display:flex;gap:4px;">
                  <button class="btn-secondary" style="padding:4px 7px;" title="Edit patient" @click.stop="goToEdit(p.id)">✏</button>
                  <button class="btn-danger" style="padding:4px 7px;" title="Delete patient" @click.stop="deletePatient(p.id)">🗑</button>
                </div>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </AppLayout>
</template>
