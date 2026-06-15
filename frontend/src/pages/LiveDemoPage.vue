<script setup>
import { computed, nextTick, onMounted, onUnmounted, ref } from 'vue'
import AppLayout from '../layouts/AppLayout.vue'
import { rhythmDescription } from '../utils/format'
import { drawECG, drawPPG } from '../utils/ecgCanvas'

const RHYTHMS = ['Normal', 'AFib', 'Bradycardia', 'Tachycardia', 'Anomaly']

const LIVE_RHYTHM_ROWS = [
  { name: 'Normal', color: '#22C55E' },
  { name: 'AFib', color: '#EF4444' },
  { name: 'Tachycardia', color: '#F97316' },
  { name: 'Bradycardia', color: '#06B6D4' },
  { name: 'Anomaly', color: '#8B5CF6' },
]

const selectedRhythm = ref('Normal')
const streaming = ref(true)

const heartRate = ref(78)
const spo2 = ref(98.1)
const hrvRmssd = ref(34.2)
const severity = ref('GREEN')
const rhythmLabel = ref('Normal')
const rhythmProbs = ref({ Normal: 0.88, AFib: 0.05, Tachycardia: 0.04, Bradycardia: 0.02, Anomaly: 0.01 })

const ecgCanvas = ref(null)
const ppgCanvas = ref(null)

let eventSource = null

const severityColor = computed(() => {
  switch (severity.value) {
    case 'RED': return '#FCA5A5'
    case 'YELLOW': return '#FDE68A'
    default: return '#86EFAC'
  }
})

function parseRhythmProbs(raw) {
  if (!raw) return {}
  if (typeof raw === 'string') {
    try { return JSON.parse(raw) } catch { return {} }
  }
  return raw
}

function redraw() {
  nextTick(() => {
    drawECG(ecgCanvas.value, rhythmLabel.value === 'AFib')
    drawPPG(ppgCanvas.value)
  })
}

function connect(rhythm) {
  if (eventSource) eventSource.close()
  streaming.value = true

  eventSource = new EventSource(`/api/triage/stream?rhythm=${encodeURIComponent(rhythm)}`)

  eventSource.addEventListener('triage', (e) => {
    try {
      const data = JSON.parse(e.data)
      heartRate.value = data.heartRate
      spo2.value = data.spo2
      hrvRmssd.value = data.hrvRmssd
      severity.value = data.severity
      rhythmLabel.value = data.rhythmLabel
      rhythmProbs.value = parseRhythmProbs(data.rhythmProbs)
      redraw()
    } catch {
      // ignore malformed event
    }
  })
}

function selectRhythm(rhythm) {
  selectedRhythm.value = rhythm
  connect(rhythm)
}

function stopStream() {
  if (eventSource) {
    eventSource.close()
    eventSource = null
  }
  streaming.value = false
}

onMounted(() => {
  redraw()
  connect(selectedRhythm.value)
})

onUnmounted(() => {
  if (eventSource) {
    eventSource.close()
    eventSource = null
  }
})
</script>

<template>
  <AppLayout>
    <div class="page-header">
      <div>
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
          <div class="page-title">Live Demo</div>
          <div v-if="streaming" class="live-badge"><div class="live-dot"></div>STREAMING</div>
          <span v-else style="font-size:11px;color:var(--tm);">Stream ended</span>
        </div>
        <div class="page-sub">Synthetic ECG/PPG · Updates every 5 seconds</div>
      </div>
      <button class="btn-secondary" :disabled="!streaming" @click="stopStream">⏹ Stop</button>
    </div>

    <div style="margin-bottom:14px;">
      <div style="font-size:11px;color:var(--tm);margin-bottom:8px;text-transform:uppercase;letter-spacing:.06em;">Select rhythm:</div>
      <div class="rhythm-selector">
        <button
          v-for="r in RHYTHMS"
          :key="r"
          class="rhythm-btn"
          :class="{ active: selectedRhythm === r }"
          @click="selectRhythm(r)"
        >{{ r }}</button>
      </div>
    </div>

    <div class="vitals-grid">
      <div class="vital-card">
        <div class="vital-label">Heart Rate</div>
        <div class="vital-val">{{ Math.round(heartRate) }}</div>
        <div class="vital-unit">bpm</div>
      </div>
      <div class="vital-card">
        <div class="vital-label">SpO₂</div>
        <div class="vital-val">{{ spo2?.toFixed(1) }}</div>
        <div class="vital-unit">%</div>
      </div>
      <div class="vital-card">
        <div class="vital-label">HRV RMSSD</div>
        <div class="vital-val">{{ hrvRmssd?.toFixed(1) }}</div>
        <div class="vital-unit">ms</div>
      </div>
      <div class="vital-card">
        <div class="vital-label">Severity</div>
        <div class="vital-val" :style="{ color: severityColor }">{{ severity }}</div>
        <div class="vital-unit">status</div>
      </div>
    </div>

    <div class="monitor">
      <div class="monitor-hdr">
        <span class="monitor-label">ECG · Live · 256 Hz</span>
        <span class="monitor-tag">{{ rhythmDescription(rhythmLabel) }}</span>
      </div>
      <canvas ref="ecgCanvas" width="700" height="80" style="width:100%;display:block;"></canvas>
    </div>

    <div class="monitor" style="margin-bottom:14px;">
      <div class="monitor-hdr">
        <span class="monitor-label">PPG · Live · 64 Hz</span>
      </div>
      <canvas ref="ppgCanvas" width="700" height="55" style="width:100%;display:block;"></canvas>
    </div>

    <div class="rhythm-bars">
      <div class="rhythm-title">Live classification</div>
      <div v-for="row in LIVE_RHYTHM_ROWS" :key="row.name" class="rhythm-row" style="margin-bottom:7px;">
        <span class="rhythm-name">{{ row.name }}</span>
        <div class="rhythm-track">
          <div class="rhythm-fill" :style="{ width: `${(rhythmProbs[row.name] ?? 0) * 100}%`, background: row.color }"></div>
        </div>
        <span class="rhythm-pct">{{ Math.round((rhythmProbs[row.name] ?? 0) * 100) }}%</span>
      </div>
    </div>
  </AppLayout>
</template>
