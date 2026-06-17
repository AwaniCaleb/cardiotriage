<script setup>
import { useRouter } from 'vue-router'
import PublicLayout from '../layouts/PublicLayout.vue'

const router = useRouter()

// ⚠ REPLACE PLACEHOLDER DATA WITH ACTUAL TEAM MEMBER DETAILS
const team = [
  { name: 'Awani Torishetosan Caleb', matNo: 'DE.2022/7451', role: 'Project Lead · Full Stack Developer', initials: 'AT' },
  { name: 'Team Member 2',  matNo: 'REPLACE/MAT/NO', role: 'Backend Developer',    initials: 'TM' },
  { name: 'Team Member 3',  matNo: 'REPLACE/MAT/NO', role: 'Frontend Developer',   initials: 'TM' },
  { name: 'Team Member 4',  matNo: 'REPLACE/MAT/NO', role: 'ML/AI Engineer',       initials: 'TM' },
  { name: 'Team Member 5',  matNo: 'REPLACE/MAT/NO', role: 'Database Administrator', initials: 'TM' },
  { name: 'Team Member 6',  matNo: 'REPLACE/MAT/NO', role: 'UI/UX Designer',       initials: 'TM' },
  { name: 'Team Member 7',  matNo: 'REPLACE/MAT/NO', role: 'Backend Developer',    initials: 'TM' },
  { name: 'Team Member 8',  matNo: 'REPLACE/MAT/NO', role: 'Frontend Developer',   initials: 'TM' },
  { name: 'Team Member 9',  matNo: 'REPLACE/MAT/NO', role: 'QA Engineer',          initials: 'TM' },
  { name: 'Team Member 10', matNo: 'REPLACE/MAT/NO', role: 'DevOps Engineer',      initials: 'TM' },
  { name: 'Team Member 11', matNo: 'REPLACE/MAT/NO', role: 'Backend Developer',    initials: 'TM' },
  { name: 'Team Member 12', matNo: 'REPLACE/MAT/NO', role: 'ML/AI Engineer',       initials: 'TM' },
  { name: 'Team Member 13', matNo: 'REPLACE/MAT/NO', role: 'Frontend Developer',   initials: 'TM' },
  { name: 'Team Member 14', matNo: 'REPLACE/MAT/NO', role: 'UI/UX Designer',       initials: 'TM' },
  { name: 'Team Member 15', matNo: 'REPLACE/MAT/NO', role: 'Database Administrator', initials: 'TM' },
]

const AVATAR_BG = ['#0C2340', '#2D1B00', '#052E16', '#1A0033', '#1C1A00', '#1A0A00']
const AVATAR_FG = ['#22D3EE', '#FCD34D', '#86EFAC', '#C084FC', '#FDE68A', '#FCA5A5']

function avatarBg(index) {
  return AVATAR_BG[index % AVATAR_BG.length]
}

function avatarFg(index) {
  return AVATAR_FG[index % AVATAR_FG.length]
}

function avatarLabel(member) {
  return member.name.startsWith('Team Member') ? '?' : member.initials
}
</script>

<template>
  <PublicLayout>
    <div style="height:100%;overflow-y:auto;background:var(--bg-page)">
      <!-- Header -->
      <div class="team-header">
        <button class="team-back-btn" @click="router.push('/')">← Back to home</button>
        <div class="landing-badge">Rivers State University · Dept. of Computer Science</div>
        <h1 style="color:var(--text-1);font-size:28px;font-weight:500;margin:16px 0 10px;">Meet the Team</h1>
        <p style="color:var(--text-2);max-width:480px;margin:0 auto;line-height:1.7;">
          CardioTriage was developed by a team of Computer Science students as a continuous
          assessment project, 2025/2026 academic session.
        </p>
        <div class="team-project-card">
          <div style="color:var(--accent);font-size:13px;margin-bottom:4px;">Project: CardioTriage — Wearable ECG Triage System</div>
          <div style="color:var(--text-3);font-size:11px;">Submitted to the Department of Computer Science, RSU</div>
        </div>
      </div>

      <!-- Team grid -->
      <div class="team-grid-wrap" style="padding:0 60px 40px">
        <div class="team-grid">
          <div v-for="(member, index) in team" :key="member.matNo + index" class="team-card">
            <div class="team-av-wrap">
              <div class="team-avatar" :style="{ background: avatarBg(index), color: avatarFg(index) }">
                {{ avatarLabel(member) }}
              </div>
            </div>
            <div class="team-name">{{ member.name }}</div>
            <div v-if="member.matNo.includes('REPLACE')" class="team-mat-tbd">Mat. No. TBD</div>
            <div v-else class="team-mat">{{ member.matNo }}</div>
            <div class="team-role">{{ member.role }}</div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="team-footer">
        <div style="color:var(--text-3);font-size:12px;">Rivers State University · Department of Computer Science · Port Harcourt, Nigeria</div>
        <div style="color:var(--text-3);font-size:11px;margin-top:4px;">⚠ Educational project — not for clinical use</div>
      </div>
    </div>
  </PublicLayout>
</template>
