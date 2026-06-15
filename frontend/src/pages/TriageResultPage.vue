<script setup>
import { computed, nextTick, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppLayout from '../layouts/AppLayout.vue'
import api from '../api'
import { formatRecordingDate, rhythmDescription, severityBadgeClass } from '../utils/format'
import { drawECG, drawPPG } from '../utils/ecgCanvas'

const route = useRoute()
const router = useRouter()
const recordingId = route.params.id

const loading = ref(true)
const triage = ref(null)
const ecgCanvas = ref(null)
const ppgCanvas = ref(null)

const patientName = route.query.patientName || 'Patient'
const deviceType = route.query.deviceType || ''
const patientIdQuery = route.query.patientId || ''

const RHYTHM_ROWS = [
  { name: 'AFib', color: '#EF4444' },
  { name: 'Tachycardia', color: '#F97316' },
  { name: 'Normal', color: '#22C55E' },
  { name: 'Anomaly', color: '#8B5CF6' },
  { name: 'Bradycardia', color: '#06B6D4' },
]

const rhythmProbs = computed(() => {
  if (!triage.value?.rhythmProbs) return {}
  try {
    return JSON.parse(triage.value.rhythmProbs)
  } catch {
    return {}
  }
})

const headerSub = computed(() => {
  const parts = [patientName, formatRecordingDate(triage.value?.createdAt)]
  if (deviceType) parts.push(deviceType)
  return parts.join(' · ')
})

const stressColor = computed(() => {
  switch (triage.value?.stressLevel) {
    case 'High': return '#FCA5A5'
    case 'Medium': return '#FCD34D'
    default: return 'var(--tx)'
  }
})

const severityBadgeText = computed(() => {
  switch (triage.value?.severity) {
    case 'RED': return '⚠ RED · Emergency'
    case 'YELLOW': return '⚠ YELLOW · Monitor'
    case 'GREEN': return '✓ GREEN · Normal'
    default: return triage.value?.severity ?? 'No result'
  }
})

function goBack() {
  if (patientIdQuery) router.push(`/patients/${patientIdQuery}`)
  else router.back()
}

onMounted(async () => {
  try {
    const { data } = await api.get(`/triage/${recordingId}`)
    triage.value = data
    await nextTick()
    drawECG(ecgCanvas.value, data.rhythmLabel === 'AFib')
    drawPPG(ppgCanvas.value)
  } catch {
    triage.value = null
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <AppLayout>
    <div v-if="loading" style="color: var(--tm); font-size: 13px;">Loading...</div>

    <div v-else-if="!triage" class="card" style="padding:32px;text-align:center;color:var(--tm);font-size:13px;">
      Triage result not found.
    </div>

    <template v-else>
      <div class="page-header" style="margin-bottom:12px;">
        <div>
          <button class="btn-secondary" style="margin-bottom:8px;font-size:11px;" @click="goBack">← Back to patient</button>
          <div class="page-title">Triage Result</div>
          <div class="page-sub">{{ headerSub }}</div>
        </div>
        <span class="badge" :class="severityBadgeClass(triage.severity)" style="font-size:12px;padding:6px 14px;">{{ severityBadgeText }}</span>
      </div>

      <div class="vitals-grid">
        <div class="vital-card">
          <div class="vital-label">Heart Rate</div>
          <div class="vital-val">{{ Math.round(triage.heartRate) }}</div>
          <div class="vital-unit">bpm</div>
        </div>
        <div class="vital-card">
          <div class="vital-label">SpO₂</div>
          <div class="vital-val" :style="{ color: triage.spo2 < 95 ? '#FCD34D' : 'var(--tx)' }">{{ triage.spo2?.toFixed(1) }}</div>
          <div class="vital-unit">%</div>
        </div>
        <div class="vital-card">
          <div class="vital-label">HRV RMSSD</div>
          <div class="vital-val">{{ triage.hrvRmssd?.toFixed(1) }}</div>
          <div class="vital-unit">ms</div>
        </div>
        <div class="vital-card">
          <div class="vital-label">Stress</div>
          <div class="vital-val" :style="{ color: stressColor }">{{ triage.stressLevel }}</div>
          <div class="vital-unit">level</div>
        </div>
      </div>

      <div class="monitor">
        <div class="monitor-hdr">
          <span class="monitor-label">ECG · Lead II · 256 Hz</span>
          <span class="monitor-tag">{{ rhythmDescription(triage.rhythmLabel) }}</span>
        </div>
        <canvas ref="ecgCanvas" width="700" height="80" style="width:100%;display:block;"></canvas>
      </div>

      <div class="monitor">
        <div class="monitor-hdr">
          <span class="monitor-label">PPG · 64 Hz</span>
          <span style="font-size:10px;color:#64748B;">SpO₂ proxy channel</span>
        </div>
        <canvas ref="ppgCanvas" width="700" height="55" style="width:100%;display:block;"></canvas>
      </div>

      <div class="rhythm-bars">
        <div class="rhythm-title">Rhythm classification</div>
        <div v-for="row in RHYTHM_ROWS" :key="row.name" class="rhythm-row" style="margin-bottom:7px;">
          <span class="rhythm-name">{{ row.name }}</span>
          <div class="rhythm-track">
            <div class="rhythm-fill" :style="{ width: `${(rhythmProbs[row.name] ?? 0) * 100}%`, background: row.color }"></div>
          </div>
          <span class="rhythm-pct">{{ Math.round((rhythmProbs[row.name] ?? 0) * 100) }}%</span>
        </div>
      </div>
    </template>
  </AppLayout>
</template>
