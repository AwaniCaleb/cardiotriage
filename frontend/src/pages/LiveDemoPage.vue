<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import AppLayout from '../layouts/AppLayout.vue'
import { rhythmDescription } from '../utils/format'

const RHYTHMS = ['Normal', 'AFib', 'Bradycardia', 'Tachycardia', 'Anomaly']

const LIVE_RHYTHM_ROWS = [
  { name: 'Normal',      color: '#22C55E' },
  { name: 'AFib',        color: '#EF4444' },
  { name: 'Tachycardia', color: '#F97316' },
  { name: 'Bradycardia', color: '#06B6D4' },
  { name: 'Anomaly',     color: '#8B5CF6' },
]

// ── reactive state ───────────────────────────────────────────────────────────
const selectedRhythm = ref('Normal')
const streaming       = ref(true)
const heartRate       = ref(78)
const spo2            = ref(98.1)
const hrvRmssd        = ref(34.2)
const severity        = ref('GREEN')
const rhythmLabel     = ref('Normal')
const rhythmProbs     = ref({ Normal: 0.88, AFib: 0.05, Tachycardia: 0.04, Bradycardia: 0.02, Anomaly: 0.01 })
const canvasWidth     = ref(700)

const ecgCanvas = ref(null)
const ppgCanvas = ref(null)

const severityColor = computed(() => {
  switch (severity.value) {
    case 'RED':    return '#FCA5A5'
    case 'YELLOW': return '#FDE68A'
    default:       return '#86EFAC'
  }
})

// ── signal generator ─────────────────────────────────────────────────────────
const ecgState = { t: 0 }
const ppgState = { t: 0 }

function nextEcgSample(rhythm) {
  ecgState.t += 1 / 256
  const t = ecgState.t

  const periods = {
    Normal:      0.80,
    Bradycardia: 1.33,
    Tachycardia: 0.44,
    Anomaly:     0.80,
  }

  if (rhythm === 'AFib') {
    const beatT    = t % (0.6 + Math.sin(t * 0.7) * 0.15)
    const qrs      = beatT < 0.05 ? Math.sin((beatT / 0.05) * Math.PI) * 1.0 : 0
    const baseline = Math.sin(t * 8.1) * 0.04 + Math.sin(t * 12.3) * 0.03
    return qrs + baseline + (Math.random() - 0.5) * 0.02
  }

  const period = periods[rhythm] ?? 0.80
  const beatT  = t % period

  const p  = beatT > 0.08 && beatT < 0.18 ? Math.sin(((beatT - 0.08) / 0.10) * Math.PI) * 0.15 : 0
  const q  = beatT > 0.20 && beatT < 0.23 ? -Math.sin(((beatT - 0.20) / 0.03) * Math.PI) * 0.15 : 0
  const r  = beatT > 0.23 && beatT < 0.30 ? Math.sin(((beatT - 0.23) / 0.07) * Math.PI) * 1.0  : 0
  const s  = beatT > 0.30 && beatT < 0.34 ? -Math.sin(((beatT - 0.30) / 0.04) * Math.PI) * 0.2 : 0
  const tw = beatT > 0.36 && beatT < 0.52 ? Math.sin(((beatT - 0.36) / 0.16) * Math.PI) * 0.25 : 0

  return p + q + r + s + tw + (Math.random() - 0.5) * 0.01
}

function nextPpgSample() {
  ppgState.t += 1 / 64
  const beatT = ppgState.t % 0.8
  if (beatT < 0.15) return Math.sin((beatT / 0.15) * Math.PI * 0.5) * 0.9
  if (beatT < 0.22) return 0.9 - ((beatT - 0.15) / 0.07) * 0.3
  if (beatT < 0.28) return 0.6 + Math.sin(((beatT - 0.22) / 0.06) * Math.PI) * 0.08
  return Math.max(0, 0.6 * Math.pow(1 - (beatT - 0.28) / 0.52, 1.5))
}

// ── circular buffers ─────────────────────────────────────────────────────────
const ECG_BUFFER_SIZE = 1024
const PPG_BUFFER_SIZE = 256
const ecgBuffer = new Float32Array(ECG_BUFFER_SIZE)
const ppgBuffer = new Float32Array(PPG_BUFFER_SIZE)
let ecgHead = 0
let ppgHead = 0

// ── drawing ───────────────────────────────────────────────────────────────────
function drawScrollingECG() {
  const canvas = ecgCanvas.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  const w   = canvas.width
  const h   = canvas.height
  const mid = h * 0.55

  ctx.clearRect(0, 0, w, h)

  ctx.strokeStyle = 'rgba(34,211,238,0.07)'
  ctx.lineWidth   = 0.5
  for (let x = 0; x < w; x += 50) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke() }
  for (let y = 0; y < h; y += 20) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke() }

  ctx.strokeStyle = '#22D3EE'
  ctx.lineWidth   = 1.5
  ctx.beginPath()
  for (let i = 0; i < w; i++) {
    const bufIdx = (ecgHead - w + i + ECG_BUFFER_SIZE * 10) % ECG_BUFFER_SIZE
    const y = mid - ecgBuffer[bufIdx] * h * 0.38
    i === 0 ? ctx.moveTo(i, y) : ctx.lineTo(i, y)
  }
  ctx.stroke()
}

function drawScrollingPPG() {
  const canvas = ppgCanvas.value
  if (!canvas) return
  const ctx   = canvas.getContext('2d')
  const w     = canvas.width
  const h     = canvas.height
  const mid   = h * 0.6
  const scale = w / PPG_BUFFER_SIZE

  ctx.clearRect(0, 0, w, h)

  ctx.strokeStyle = 'rgba(249,115,22,0.12)'
  ctx.lineWidth   = 0.5
  for (let x = 0; x < w; x += 50) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke() }

  ctx.strokeStyle = '#F97316'
  ctx.lineWidth   = 1.5
  ctx.beginPath()
  for (let i = 0; i < PPG_BUFFER_SIZE; i++) {
    const bufIdx = (ppgHead - PPG_BUFFER_SIZE + i + PPG_BUFFER_SIZE * 10) % PPG_BUFFER_SIZE
    const x = i * scale
    const y = mid - ppgBuffer[bufIdx] * h * 0.55
    i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y)
  }
  ctx.stroke()
}

// ── animation loop ────────────────────────────────────────────────────────────
let animFrameId    = null
let currentRhythm  = 'Normal'

function animationLoop() {
  for (let i = 0; i < 4; i++) {
    ecgBuffer[ecgHead % ECG_BUFFER_SIZE] = nextEcgSample(currentRhythm)
    ecgHead++
  }
  ppgBuffer[ppgHead % PPG_BUFFER_SIZE] = nextPpgSample()
  ppgHead++

  drawScrollingECG()
  drawScrollingPPG()

  animFrameId = requestAnimationFrame(animationLoop)
}

// ── SSE ───────────────────────────────────────────────────────────────────────
let eventSource = null
const apiBase   = import.meta.env.VITE_API_URL || '/api'

function parseRhythmProbs(raw) {
  if (!raw) return {}
  if (typeof raw === 'string') { try { return JSON.parse(raw) } catch { return {} } }
  return raw
}

function connect(rhythm) {
  if (eventSource) eventSource.close()
  streaming.value = true

  eventSource = new EventSource(`${apiBase}/triage/stream?rhythm=${encodeURIComponent(rhythm)}`)

  eventSource.addEventListener('triage', (e) => {
    try {
      const data     = JSON.parse(e.data)
      heartRate.value  = data.heart_rate
      spo2.value       = data.spo2
      hrvRmssd.value   = data.hrv_rmssd
      severity.value   = data.severity
      rhythmLabel.value = data.rhythm_label
      rhythmProbs.value = parseRhythmProbs(data.rhythm_probs)
      currentRhythm    = data.rhythm_label ?? currentRhythm
    } catch { /* ignore malformed event */ }
  })
}

function selectRhythm(rhythm) {
  selectedRhythm.value = rhythm
  currentRhythm        = rhythm
  connect(rhythm)
}

function stopStream() {
  if (eventSource) { eventSource.close(); eventSource = null }
  streaming.value = false
}

// ── lifecycle ─────────────────────────────────────────────────────────────────
onMounted(() => {
  canvasWidth.value = Math.max(400, window.innerWidth - 220)
  animationLoop()
  connect(selectedRhythm.value)
})

onUnmounted(() => {
  if (animFrameId) cancelAnimationFrame(animFrameId)
  if (eventSource) { eventSource.close(); eventSource = null }
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
      <canvas ref="ecgCanvas" :width="canvasWidth" height="80" style="width:100%;display:block;"></canvas>
    </div>

    <div class="monitor" style="margin-bottom:14px;">
      <div class="monitor-hdr">
        <span class="monitor-label">PPG · Live · 64 Hz</span>
      </div>
      <canvas ref="ppgCanvas" :width="canvasWidth" height="55" style="width:100%;display:block;"></canvas>
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
