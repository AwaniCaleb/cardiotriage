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
    <div class="topbar">
      <div>
        <div class="pg-title">Dashboard</div>
        <div class="pg-sub">{{ todayLabel }}</div>
      </div>
      <div class="warn-pill"><i class="ti ti-alert-triangle" style="font-size:12px"></i>Educational · not for clinical use</div>
    </div>

    <div class="body">
      <div v-if="loading" style="color:var(--text-3);font-size:13px;padding:20px 0">Loading…</div>

      <template v-else>
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-lbl"><i class="ti ti-users"></i>Total Patients</div>
            <div class="stat-val">{{ stats.totalPatients }}</div>
            <div class="stat-sub">
              <span v-if="stats.newPatients > 0" class="up">↑ {{ stats.newPatients }}</span>
              <span v-else>—</span>
              <span>{{ stats.newPatients > 0 ? 'this week' : 'No new this week' }}</span>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-lbl"><i class="ti ti-activity"></i>Recordings</div>
            <div class="stat-val">{{ stats.totalRecordings }}</div>
            <div class="stat-sub">
              <span v-if="stats.recordingsToday > 0" class="up">↑ {{ stats.recordingsToday }}</span>
              <span v-else>—</span>
              <span>{{ stats.recordingsToday > 0 ? 'today' : 'None today' }}</span>
            </div>
          </div>
          <div class="stat-card" :class="{ alert: stats.critical > 0 }">
            <div class="stat-lbl"><i class="ti ti-alert-circle" :style="{ color: 'var(--purple)' }"></i>Critical Alerts</div>
            <div class="stat-val" :class="{ red: stats.critical > 0 }">{{ stats.critical }}</div>
            <div class="stat-sub">
              <i v-if="stats.critical > 0" class="ti ti-alert-circle" style="font-size:11px;color:var(--purple)"></i>
              <span :class="stats.critical > 0 ? 'ref' : ''">{{ stats.critical > 0 ? stats.criticalPatient : 'No critical alerts' }}</span>
            </div>
          </div>
        </div>

        <div class="sec-hdr">
          <div class="sec-title">Recent Recordings</div>
          <button class="sec-action" @click="$router.push('/patients')">See all →</button>
        </div>

        <div v-if="recentRecordings.length === 0" style="color:var(--text-3);font-size:13px;padding:12px 0">No recordings yet.</div>

        <div
          v-for="rec in recentRecordings"
          :key="rec.id"
          class="row-card"
          @click="$router.push('/patients/' + rec.patientId)"
        >
          <div class="av" :class="rec.triageResult?.severity === 'RED' ? 'red' : rec.triageResult?.severity === 'GREEN' ? 'green' : rec.triageResult?.severity === 'YELLOW' ? 'purple' : 'teal'">{{ initials(rec.patientName) }}</div>
          <div class="flex-1">
            <div class="row-name">{{ rec.patientName }}</div>
            <div class="row-sub">{{ rhythmDescription(rec.triageResult?.rhythmLabel) }} · {{ formatRelativeTime(rec.uploadedAt) }}</div>
          </div>
          <span class="badge" :class="severityBadgeClass(rec.triageResult?.severity)">{{ rec.triageResult?.severity ?? '—' }}</span>
        </div>
      </template>
    </div>
  </AppLayout>
</template>
