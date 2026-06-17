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
    <div v-if="loading" class="body" style="padding-top:20px;color:var(--text-3);font-size:13px;">Loading…</div>

    <div v-else-if="!patient" class="body">
      <div class="card" style="padding:32px;text-align:center;color:var(--text-3);font-size:13px;">Patient not found.</div>
    </div>

    <template v-else>
      <div class="topbar">
        <div>
          <button class="btn ghost" style="margin-bottom:12px;font-size:12px;padding:6px 12px" @click="router.push('/patients')"><i class="ti ti-arrow-left"></i>Back to Patients</button>
          <div class="pg-title">{{ patient.name }}</div>
          <div class="pg-sub">Patient Record</div>
        </div>
        <div class="flex gap-10 items-c">
          <button class="btn ghost" @click="router.push(`/patients/${patientId}/edit`)"><i class="ti ti-edit"></i>Edit</button>
        </div>
      </div>

      <div class="body">
        <!-- Patient header card -->
        <div class="pt-hdr-card">
          <div class="av xl teal">{{ (patient.name || '?').split(' ').map(w => w[0]).join('').slice(0,2).toUpperCase() }}</div>
          <div class="flex-1">
            <div class="pt-name">{{ patient.name }}</div>
            <div class="pt-meta">{{ patient.age }} years · {{ patient.gender || '—' }} · Blood type: {{ patient.bloodType || '—' }}</div>
            <div class="info-grid">
              <div><div class="info-lbl">Conditions</div><div class="info-val">{{ patient.conditions || '—' }}</div></div>
              <div><div class="info-lbl">Medications</div><div class="info-val">{{ patient.medications || '—' }}</div></div>
              <div><div class="info-lbl">Emergency Contact</div><div class="info-val"><template v-if="emergencyContact">{{ emergencyContact.name }} · {{ emergencyContact.phone }}</template><template v-else>—</template></div></div>
            </div>
          </div>
        </div>

        <!-- Two-column: recordings + upload -->
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">
          <div>
            <div class="sec-hdr"><div class="sec-title">Recordings ({{ recordings.length }})</div></div>
            <div v-if="recordings.length === 0" class="card" style="padding:24px;text-align:center;color:var(--text-3);font-size:13px;">No recordings yet.</div>
            <div
              v-for="rec in recordings"
              :key="rec.id"
              class="row-card"
              @click="goToTriage(rec)"
            >
              <div class="av sm teal">{{ (patient.name || '?').split(' ').map(w => w[0]).join('').slice(0,2).toUpperCase() }}</div>
              <div class="flex-1">
                <div class="row-name" style="font-size:12.5px">Recording · {{ rec.deviceType }}</div>
                <div class="row-sub">{{ formatRecordingDate(rec.uploadedAt) }}</div>
              </div>
              <span class="badge" :class="severityBadgeClass(rec.triageResult?.severity)">{{ rec.triageResult?.severity ?? '—' }}</span>
            </div>
          </div>

          <div>
            <div class="sec-hdr"><div class="sec-title">Upload New Recording</div></div>
            <div class="card">
              <div class="upload-zone" @click="$el.querySelector('input[type=file]').click()" style="position:relative">
                <i class="ti ti-cloud-upload"></i>
                <div class="upload-zone-title">{{ selectedFile ? selectedFile.name : 'Drop .json file here' }}</div>
                <div class="upload-zone-sub">ECG/PPG wearable recording</div>
                <input type="file" accept=".json" style="display:none" @change="onFileChange">
              </div>
              <div class="form-group mt-14 mb-0">
                <div class="form-label">Device Type</div>
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
              <p v-if="uploadError" style="color:var(--red-text);font-size:12px;margin-top:10px;">{{ uploadError }}</p>
              <button class="btn primary full" style="margin-top:12px" :disabled="!selectedFile || uploading" @click="runTriage"><i class="ti ti-brain"></i>{{ uploading ? 'Analysing…' : 'Run Triage' }}</button>
            </div>
          </div>
        </div>
      </div>
    </template>
  </AppLayout>
</template>
