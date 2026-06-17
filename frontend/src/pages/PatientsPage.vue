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
    <div class="topbar">
      <div>
        <div class="pg-title">Patients</div>
        <div class="pg-sub">{{ patients.length }} records total</div>
      </div>
      <button class="btn primary" @click="router.push('/patients/new')"><i class="ti ti-plus"></i>Add patient</button>
    </div>

    <div class="body">
      <div class="search-bar">
        <i class="ti ti-search"></i>
        <input type="text" v-model="search" placeholder="Search patients by name…">
      </div>

      <div v-if="loading" style="display:flex;justify-content:center;padding:40px 0;">
        <div style="width:24px;height:24px;border:2px solid var(--border-color);border-top-color:var(--accent);border-radius:50%;animation:spin 1s linear infinite;"></div>
      </div>

      <div v-else-if="patients.length === 0" class="card" style="padding:32px;text-align:center;color:var(--text-3);font-size:13px;">
        No patients yet. Add your first patient.
      </div>

      <div v-else-if="filteredPatients.length === 0" class="card" style="padding:32px;text-align:center;color:var(--text-3);font-size:13px;">
        No patients match your search.
      </div>

      <template v-else>
        <div
          v-for="p in filteredPatients"
          :key="p.id"
          class="row-card"
          @click="router.push(`/patients/${p.id}`)"
        >
          <div class="av" :class="p.lastRecording?.triageResult?.severity === 'RED' ? 'red' : p.lastRecording?.triageResult?.severity === 'GREEN' ? 'green' : p.lastRecording?.triageResult?.severity === 'YELLOW' ? 'purple' : 'teal'">
            {{ (p.name || '?').split(' ').map(w => w[0]).join('').slice(0,2).toUpperCase() }}
          </div>
          <div class="flex-1">
            <div class="row-name">{{ p.name }}</div>
            <div class="row-sub">{{ p.age }} · {{ p.gender || '—' }} · {{ p.conditions || 'No conditions' }}</div>
          </div>
          <span class="badge" :class="severityBadgeClass(p.lastRecording?.triageResult?.severity)">{{ p.lastRecording?.triageResult?.severity ?? '—' }}</span>
          <div style="display:flex;gap:6px;margin-left:6px;" @click.stop>
            <button class="btn ghost" style="padding:6px 10px;font-size:12px;" @click.stop="goToEdit(p.id)"><i class="ti ti-edit"></i></button>
            <button class="btn danger" style="padding:6px 10px;font-size:12px;" @click.stop="deletePatient(p.id)"><i class="ti ti-trash"></i></button>
          </div>
        </div>
      </template>
    </div>
  </AppLayout>
</template>
