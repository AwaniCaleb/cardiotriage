<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppLayout from '../layouts/AppLayout.vue'
import api from '../api'
import { formatDate, formatRecordingDate, severityBadgeClass } from '../utils/format'

const route = useRoute()
const router = useRouter()
const patientId = route.params.id

const loading = ref(true)
const patient = ref(null)
const recordings = ref([])

const showUpload = ref(true)
const selectedFile = ref(null)
const deviceType = ref('generic_wearable')
const uploading = ref(false)
const uploadError = ref('')

const emergencyContact = computed(() => {
  if (!patient.value?.emergencyContact) return null
  try {
    return JSON.parse(patient.value.emergencyContact)
  } catch {
    return null
  }
})

onMounted(async () => {
  try {
    const [{ data: patientData }, { data: recordingsData }] = await Promise.all([
      api.get(`/patients/${patientId}`),
      api.get(`/patients/${patientId}/recordings`),
    ])
    patient.value = patientData
    recordings.value = recordingsData
  } catch {
    patient.value = null
  } finally {
    loading.value = false
  }
})

function onFileChange(e) {
  selectedFile.value = e.target.files[0] ?? null
}

async function runTriage() {
  if (!selectedFile.value) return
  uploading.value = true
  uploadError.value = ''
  try {
    const formData = new FormData()
    formData.append('patientId', patientId)
    formData.append('deviceType', deviceType.value)
    formData.append('file', selectedFile.value)

    const { data } = await api.post('/recordings/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })

    recordings.value.unshift({
      id: data.recordingId,
      patientId: Number(patientId),
      deviceType: deviceType.value,
      uploadedAt: new Date().toISOString(),
      triageResult: data,
    })

    router.push({
      path: `/recordings/${data.recordingId}/triage`,
      query: { patientName: patient.value?.name ?? '', deviceType: deviceType.value, patientId },
    })
  } catch {
    uploadError.value = 'Failed to analyse recording. Please check the file and try again.'
  } finally {
    uploading.value = false
  }
}

function goToTriage(rec) {
  router.push({
    path: `/recordings/${rec.id}/triage`,
    query: { patientName: patient.value?.name ?? '', deviceType: rec.deviceType, patientId },
  })
}
</script>

<template>
  <AppLayout>
    <div v-if="loading" style="color: var(--tm); font-size: 13px;">Loading...</div>

    <div v-else-if="!patient" class="card" style="padding:32px;text-align:center;color:var(--tm);font-size:13px;">
      Patient not found.
    </div>

    <template v-else>
      <div class="page-header" style="margin-bottom:14px;">
        <div>
          <button class="btn-secondary" style="margin-bottom:8px;font-size:11px;" @click="router.push('/patients')">← Back to patients</button>
          <div class="page-title">{{ patient.name }}</div>
          <div class="page-sub">Patient #{{ String(patient.id).padStart(3, '0') }} · Added {{ formatDate(patient.createdAt) }}</div>
        </div>
        <button class="btn-secondary" @click="router.push(`/patients/${patientId}/edit`)">✏ Edit patient</button>
      </div>

      <!-- Patient info card -->
      <div class="card" style="margin-bottom:14px;">
        <div style="padding:14px 16px;border-bottom:1px solid var(--bd);">
          <div style="font-size:12px;font-weight:500;color:var(--tm);text-transform:uppercase;letter-spacing:.06em;">Patient information</div>
        </div>
        <div style="padding:14px 16px;display:grid;grid-template-columns:repeat(3,1fr);gap:16px;">
          <div>
            <div style="font-size:10px;color:var(--tm);text-transform:uppercase;letter-spacing:.06em;margin-bottom:3px;">Age</div>
            <div style="font-size:14px;color:var(--tx);">{{ patient.age }} years</div>
          </div>
          <div>
            <div style="font-size:10px;color:var(--tm);text-transform:uppercase;letter-spacing:.06em;margin-bottom:3px;">Gender</div>
            <div style="font-size:14px;color:var(--tx);">{{ patient.gender || '—' }}</div>
          </div>
          <div>
            <div style="font-size:10px;color:var(--tm);text-transform:uppercase;letter-spacing:.06em;margin-bottom:3px;">Blood type</div>
            <div style="font-size:14px;color:var(--tx);">{{ patient.bloodType || '—' }}</div>
          </div>
          <div>
            <div style="font-size:10px;color:var(--tm);text-transform:uppercase;letter-spacing:.06em;margin-bottom:3px;">Conditions</div>
            <div style="font-size:13px;color:var(--tx);">{{ patient.conditions || '—' }}</div>
          </div>
          <div>
            <div style="font-size:10px;color:var(--tm);text-transform:uppercase;letter-spacing:.06em;margin-bottom:3px;">Medications</div>
            <div style="font-size:13px;color:var(--tx);">{{ patient.medications || '—' }}</div>
          </div>
          <div>
            <div style="font-size:10px;color:var(--tm);text-transform:uppercase;letter-spacing:.06em;margin-bottom:3px;">Emergency contact</div>
            <div style="font-size:13px;color:var(--tx);">
              <template v-if="emergencyContact">{{ emergencyContact.name }} · {{ emergencyContact.phone }}</template>
              <template v-else>—</template>
            </div>
          </div>
        </div>
      </div>

      <!-- Upload panel -->
      <div class="upload-panel">
        <div class="upload-title" style="display:flex;align-items:center;justify-content:space-between;cursor:pointer;" @click="showUpload = !showUpload">
          <span>Upload new recording</span>
          <span style="color:var(--tm);font-size:11px;font-weight:400;">{{ showUpload ? '▲ Hide' : '▼ Show' }}</span>
        </div>
        <div v-show="showUpload">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px;">
            <div class="form-group">
              <label class="form-label">ECG/PPG file (.json)</label>
              <input type="file" accept=".json" class="form-input" @change="onFileChange" />
            </div>
            <div class="form-group">
              <label class="form-label">Device type</label>
              <select v-model="deviceType" class="form-select">
                <option>generic_wearable</option>
                <option>apple_watch</option>
                <option>samsung_galaxy</option>
                <option>fitbit_sense</option>
                <option>garmin_venu</option>
                <option>kardia_mobile</option>
                <option>smartphone_camera</option>
              </select>
            </div>
          </div>
          <p v-if="uploadError" style="color:#EF4444;font-size:12px;margin-bottom:12px;">{{ uploadError }}</p>
          <button class="btn-primary" :disabled="!selectedFile || uploading" @click="runTriage">
            {{ uploading ? 'Analysing recording…' : '▶ Run triage' }}
          </button>
        </div>
      </div>

      <!-- Recordings table -->
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">
        <div style="font-size:14px;font-weight:500;color:var(--tx);">Recordings ({{ recordings.length }})</div>
      </div>
      <div v-if="recordings.length === 0" class="card" style="padding:32px;text-align:center;color:var(--tm);font-size:13px;">
        No recordings yet for this patient.
      </div>
      <div v-else class="card">
        <table class="data-table">
          <thead>
            <tr>
              <th style="width:28%;">Date uploaded</th>
              <th style="width:22%;">Device</th>
              <th style="width:22%;">Severity</th>
              <th style="width:28%;">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="rec in recordings" :key="rec.id">
              <td style="font-size:12px;color:var(--tm);">{{ formatRecordingDate(rec.uploadedAt) }}</td>
              <td style="font-size:12px;">{{ rec.deviceType }}</td>
              <td><span class="badge" :class="severityBadgeClass(rec.triageResult?.severity)">{{ rec.triageResult?.severity ?? 'No result' }}</span></td>
              <td><button class="btn-secondary" style="font-size:11px;padding:4px 10px;" @click="goToTriage(rec)">View result →</button></td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </AppLayout>
</template>
