<script setup>
import { computed, onMounted, ref } from 'vue'
import AppLayout from '../layouts/AppLayout.vue'
import api from '../api'
import { avatarColors, formatRelativeTime, initials, rhythmDescription, severityBadgeClass } from '../utils/format'

const loading = ref(true)
const statsApi = ref(null)   // { totalPatients, totalRecordings, criticalAlerts } from API
const patients = ref([])
const recordings = ref([])

const todayLabel = new Date().toLocaleDateString(undefined, {
  weekday: 'long', day: 'numeric', month: 'long', year: 'numeric',
})

function daysAgo(dateStr) {
  if (!dateStr) return Infinity
  return (Date.now() - new Date(dateStr).getTime()) / 86400000
}

const stats = computed(() => {
  const criticalRecordings = recordings.value.filter((r) => r.triageResult?.severity === 'RED')
  // prefer exact counts from the stats endpoint; fall back to locally-computed values
  return {
    totalPatients:   statsApi.value?.totalPatients   ?? patients.value.length,
    totalRecordings: statsApi.value?.totalRecordings ?? recordings.value.length,
    critical:        statsApi.value?.criticalAlerts  ?? criticalRecordings.length,
    criticalPatient: criticalRecordings[0]?.patientName ?? null,
    newPatients:     patients.value.filter((p) => daysAgo(p.createdAt) < 7).length,
    recordingsToday: recordings.value.filter((r) => daysAgo(r.uploadedAt) < 1).length,
  }
})

const recentRecordings = computed(() =>
  [...recordings.value]
    .sort((a, b) => new Date(b.uploadedAt) - new Date(a.uploadedAt))
    .slice(0, 4)
)

onMounted(async () => {
  // fire stats + patient list in parallel
  const [statsRes, patientsRes] = await Promise.allSettled([
    api.get('/dashboard/stats'),
    api.get('/patients'),
  ])

  if (statsRes.status === 'fulfilled') {
    statsApi.value = statsRes.value.data   // { totalPatients, totalRecordings, criticalAlerts }
  }

  if (patientsRes.status === 'fulfilled') {
    patients.value = patientsRes.value.data
    // fetch per-patient recordings for the recent-activity list
    const all = []
    for (const p of patients.value) {
      try {
        const { data: recs } = await api.get(`/patients/${p.id}/recordings`)
        recs.forEach((r) => all.push({ ...r, patientName: p.name }))
      } catch { /* skip */ }
    }
    recordings.value = all
  }

  loading.value = false
})
</script>

<template>
  <AppLayout>
    <div class="page-header">
      <div>
        <div class="page-title">Dashboard</div>
        <div class="page-sub">{{ todayLabel }}</div>
      </div>
    </div>

    <div v-if="loading" style="color: var(--tm); font-size: 13px;">Loading...</div>

    <template v-else>
      <div class="stat-grid">
        <div class="stat-card">
          <div class="stat-label">Total Patients</div>
          <div class="stat-num">{{ stats.totalPatients }}</div>
          <div class="stat-sub" :style="{ color: stats.newPatients > 0 ? '#22C55E' : 'var(--tm)' }">
            {{ stats.newPatients > 0 ? `↑ ${stats.newPatients} this week` : 'No new patients this week' }}
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Recordings</div>
          <div class="stat-num">{{ stats.totalRecordings }}</div>
          <div class="stat-sub" :style="{ color: stats.recordingsToday > 0 ? '#22C55E' : 'var(--tm)' }">
            {{ stats.recordingsToday > 0 ? `↑ ${stats.recordingsToday} today` : 'No recordings today' }}
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Critical Alerts</div>
          <div class="stat-num" :style="{ color: stats.critical > 0 ? '#FCA5A5' : 'var(--tx)' }">{{ stats.critical }}</div>
          <div class="stat-sub" :style="{ color: stats.critical > 0 ? '#FCA5A5' : 'var(--tm)' }">
            {{ stats.critical > 0 ? `⚠ ${stats.criticalPatient}` : 'No critical alerts' }}
          </div>
        </div>
      </div>

      <div class="card">
        <div style="padding:14px 16px;border-bottom:1px solid var(--bd);">
          <div style="font-size:11px;font-weight:500;color:var(--tm);text-transform:uppercase;letter-spacing:.06em;">Recent recordings</div>
        </div>
        <div style="padding:0 16px;">
          <div v-if="recentRecordings.length === 0" style="padding:16px 0;color:var(--tm);font-size:13px;">
            No recordings yet.
          </div>
          <div v-for="rec in recentRecordings" :key="rec.id" class="activity-item">
            <div class="act-avatar" :style="avatarColors(rec.triageResult?.severity)">{{ initials(rec.patientName) }}</div>
            <div style="flex:1;">
              <div style="font-size:13px;color:var(--tx);font-weight:500;">{{ rec.patientName }}</div>
              <div style="font-size:11px;color:var(--tm);">{{ rhythmDescription(rec.triageResult?.rhythmLabel) }} · {{ formatRelativeTime(rec.uploadedAt) }}</div>
            </div>
            <span class="badge" :class="severityBadgeClass(rec.triageResult?.severity)">{{ rec.triageResult?.severity ?? 'No result' }}</span>
          </div>
        </div>
      </div>
    </template>
  </AppLayout>
</template>
