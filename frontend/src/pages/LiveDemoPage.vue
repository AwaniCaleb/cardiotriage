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

const ecgCanvas = ref(null)
const ppgCanvas = ref(null)

// plain JS — not reactive, so Vue re-renders can't touch it
const rhythmCache = {}

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

// ── strip chart state (plain JS, not reactive) ───────────────────────────────
let ecgDrawX = 0
let ppgDrawX = 0
const ECG_PX_PER_FRAME = 3
const PPG_PX_PER_FRAME = 3

function initCanvas(canvas, height) {
  canvas.width  = canvas.offsetWidth
  canvas.height = height
  const ctx = canvas.getContext('2d')
  ctx.fillStyle = '#060C18'
  ctx.fillRect(0, 0, canvas.width, canvas.height)
}

// ── strip chart drawing ───────────────────────────────────────────────────────
function stripECG() {
  const canvas = ecgCanvas.value
  if (!canvas || !canvas.width) return
  const ctx = canvas.getContext('2d')
  const w   = canvas.width
  const h   = canvas.height
  const mid = h * 0.55

  if (ecgDrawX < w) {
    // Phase 1: trace left to right
    ctx.strokeStyle = '#22D3EE'
    ctx.lineWidth   = 1.5
    ctx.beginPath()
    for (let i = 0; i < ECG_PX_PER_FRAME; i++) {
      const x = ecgDrawX + i
      const y = mid - nextEcgSample(currentRhythm) * h * 0.38
      i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y)
    }
    ctx.stroke()
    ecgDrawX += ECG_PX_PER_FRAME
  } else {
    // Phase 2: scroll canvas left, append on right
    ctx.drawImage(canvas, -ECG_PX_PER_FRAME, 0)
    ctx.fillStyle = '#060C18'
    ctx.fillRect(w - ECG_PX_PER_FRAME - 1, 0, ECG_PX_PER_FRAME + 1, h)
    ctx.strokeStyle = '#22D3EE'
    ctx.lineWidth   = 1.5
    ctx.beginPath()
    for (let i = 0; i < ECG_PX_PER_FRAME; i++) {
      const x = w - ECG_PX_PER_FRAME + i
      const y = mid - nextEcgSample(currentRhythm) * h * 0.38
      i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y)
    }
    ctx.stroke()
  }
}

function stripPPG() {
  const canvas = ppgCanvas.value
  if (!canvas || !canvas.width) return
  const ctx = canvas.getContext('2d')
  const w   = canvas.width
  const h   = canvas.height
  const mid = h * 0.6

  if (ppgDrawX < w) {
    // Phase 1: trace left to right
    ctx.strokeStyle = '#F97316'
    ctx.lineWidth   = 1.5
    ctx.beginPath()
    for (let i = 0; i < PPG_PX_PER_FRAME; i++) {
      const x = ppgDrawX + i
      const y = mid - nextPpgSample() * h * 0.55
      i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y)
    }
    ctx.stroke()
    ppgDrawX += PPG_PX_PER_FRAME
  } else {
    // Phase 2: scroll canvas left, append on right
    ctx.drawImage(canvas, -PPG_PX_PER_FRAME, 0)
    ctx.fillStyle = '#060C18'
    ctx.fillRect(w - PPG_PX_PER_FRAME - 1, 0, PPG_PX_PER_FRAME + 1, h)
    ctx.strokeStyle = '#F97316'
    ctx.lineWidth   = 1.5
    ctx.beginPath()
    for (let i = 0; i < PPG_PX_PER_FRAME; i++) {
      const x = w - PPG_PX_PER_FRAME + i
      const y = mid - nextPpgSample() * h * 0.55
      i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y)
    }
    ctx.stroke()
  }
}

// ── animation loop ────────────────────────────────────────────────────────────
let animFrameId   = null
let currentRhythm = 'Normal'

function animationLoop() {
  stripECG()
  stripPPG()
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

function applyTriageData(data) {
  heartRate.value   = data.heart_rate
  spo2.value        = data.spo2
  hrvRmssd.value    = data.hrv_rmssd
  severity.value    = data.severity
  rhythmLabel.value = data.rhythm_label
  rhythmProbs.value = parseRhythmProbs(data.rhythm_probs)
  currentRhythm     = data.rhythm_label ?? currentRhythm
}

function connect(rhythm) {
  if (eventSource) eventSource.close()
  streaming.value = true

  eventSource = new EventSource(`${apiBase}/triage/stream?rhythm=${encodeURIComponent(rhythm)}`)

  eventSource.addEventListener('triage', (e) => {
    try {
      const data  = JSON.parse(e.data)
      applyTriageData(data)
      const label = data.rhythm_label ?? currentRhythm
      rhythmCache[label] = {
        heart_rate:   data.heart_rate,
        spo2:         data.spo2,
        hrv_rmssd:    data.hrv_rmssd,
        severity:     data.severity,
        rhythm_label: data.rhythm_label,
        rhythm_probs: data.rhythm_probs,
        stress_level: data.stress_level,
      }
    } catch { /* ignore malformed event */ }
  })
}

function selectRhythm(rhythm) {
  selectedRhythm.value = rhythm
  currentRhythm        = rhythm
  if (rhythmCache[rhythm]) applyTriageData(rhythmCache[rhythm])
  connect(rhythm)
}

function stopStream() {
  if (eventSource) { eventSource.close(); eventSource = null }
  streaming.value = false
}

// ── lifecycle ─────────────────────────────────────────────────────────────────
onMounted(() => {
  initCanvas(ecgCanvas.value, 80)
  initCanvas(ppgCanvas.value, 55)
  ecgDrawX = 0
  ppgDrawX = 0
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
    <!-- Stream header -->
    <div class="stream-hdr">
      <div>
        <div class="flex items-c gap-10">
          <div class="pg-title">Live Demo</div>
          <div v-if="streaming" class="stream-badge"><div class="stream-dot"></div>STREAMING</div>
          <span v-else style="font-size:11px;color:var(--text-3)">Stream ended</span>
        </div>
        <div class="pg-sub" style="margin-top:3px">Synthetic ECG/PPG · Updates every 5 seconds</div>
      </div>
      <button class="btn ghost" :disabled="!streaming" @click="stopStream"><i class="ti ti-player-stop"></i>Stop</button>
    </div>

    <!-- Rhythm selector tabs -->
    <div class="rhythm-tabs">
      <button
        v-for="r in RHYTHMS"
        :key="r"
        class="rhythm-tab"
        :class="{ active: selectedRhythm === r }"
        @click="selectRhythm(r)"
      >{{ r }}</button>
    </div>

    <!-- Vitals strip -->
    <div class="vitals-strip">
      <div class="vstrip-card"><div class="vital-lbl">Heart Rate</div><div class="vital-val">{{ Math.round(heartRate) }} <span style="font-size:12px;font-weight:400">bpm</span></div></div>
      <div class="vstrip-card"><div class="vital-lbl">SpO₂</div><div class="vital-val">{{ spo2?.toFixed(1) }} <span style="font-size:12px;font-weight:400">%</span></div></div>
      <div class="vstrip-card"><div class="vital-lbl">HRV RMSSD</div><div class="vital-val">{{ hrvRmssd?.toFixed(1) }} <span style="font-size:12px;font-weight:400">ms</span></div></div>
      <div class="vstrip-card"><div class="vital-lbl">Severity</div><div class="vital-val" style="font-size:20px" :style="{ color: severityColor }">{{ severity }}</div></div>
    </div>

    <!-- Canvas blocks -->
    <div style="padding:0 24px 14px">
      <div class="canvas-block" style="margin-bottom:10px">
        <div class="canvas-lbl"><span>ECG · LIVE · 256 HZ</span><span class="rhythm-tag">{{ rhythmDescription(rhythmLabel) }}</span></div>
        <div class="canvas-bg">
          <canvas ref="ecgCanvas" style="width:100%;height:90px;display:block;"></canvas>
        </div>
      </div>
      <div class="canvas-block" style="margin-bottom:14px">
        <div class="canvas-lbl"><span>PPG · LIVE · 64 HZ</span></div>
        <div class="canvas-bg">
          <canvas ref="ppgCanvas" style="width:100%;height:65px;display:block;"></canvas>
        </div>
      </div>

      <!-- Classification -->
      <div class="rhythm-probs">
        <div class="sec-title" style="margin-bottom:12px">Live Classification</div>
        <div v-for="row in LIVE_RHYTHM_ROWS" :key="row.name" class="rhythm-row">
          <div class="rhythm-name">{{ row.name }}</div>
          <div class="rhythm-track"><div class="rhythm-fill" :style="{ width: `${(rhythmProbs[row.name] ?? 0) * 100}%`, background: row.color }"></div></div>
          <div class="rhythm-pct">{{ Math.round((rhythmProbs[row.name] ?? 0) * 100) }}%</div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>
