<script setup>
import { useRouter } from 'vue-router'
import PublicLayout from '../layouts/PublicLayout.vue'

const router = useRouter()

const devices = [
  'Apple Watch',
  'Samsung Galaxy Watch',
  'Fitbit Sense',
  'Garmin Venu',
  'KardiaMobile',
  'KardiaMobile 6L',
  'Smartphone camera',
  'Generic wearable',
]

const techStack = [
  'Java',
  'Spring Boot',
  'Vue.js 3',
  'Tailwind CSS',
  'Python',
  'FastAPI',
  'PyTorch',
  'PostgreSQL',
  'Chart.js',
]
</script>

<template>
  <PublicLayout>
    <div class="h-full overflow-y-auto">
      <div class="landing">
        <!-- SECTION 1 — Nav -->
        <div class="landing-nav">
          <div style="display:flex;align-items:center;gap:10px;">
            <div class="sb-logo-icon">
              <svg viewBox="0 0 24 24"><polyline points="2,12 6,12 9,4 12,20 15,8 18,16 21,12" /></svg>
            </div>
            <span style="color:#F1F5F9;font-size:15px;font-weight:500;">CardioTriage</span>
          </div>
          <div style="display:flex;gap:24px;align-items:center;">
            <a href="#how-it-works" style="color:#94A3B8;font-size:13px;text-decoration:none;">How it works</a>
            <a href="#features" style="color:#94A3B8;font-size:13px;text-decoration:none;">Features</a>
            <a href="#" style="color:#94A3B8;font-size:13px;text-decoration:none;" @click.prevent="router.push('/team')">Team</a>
            <button style="background:transparent;color:#0891B2;border:1px solid #0891B2;border-radius:6px;padding:7px 16px;font-size:13px;cursor:pointer;" @click="router.push('/register')">Register</button>
            <button style="background:#0891B2;color:#fff;border:none;border-radius:6px;padding:7px 16px;font-size:13px;cursor:pointer;" @click="router.push('/login')">Sign in</button>
          </div>
        </div>

        <!-- SECTION 2 — Hero -->
        <div class="landing-hero">
          <svg width="100%" height="52" viewBox="0 0 400 52" preserveAspectRatio="none" style="display:block;margin-bottom:24px;">
            <polyline
              points="0,26 30,26 42,8 50,44 58,4 66,46 74,26 120,26 132,8 140,44 148,4 156,46 164,26 210,26 222,8 230,44 238,4 246,46 254,26 320,26 332,8 340,44 348,4 356,46 364,26 400,26"
              stroke="#22D3EE" stroke-width="1.8" fill="none" opacity="0.6"
            />
          </svg>
          <div class="landing-badge">Rivers State University · Dept. of Computer Science</div>
          <h1 style="color:#F1F5F9;font-size:36px;font-weight:500;line-height:1.25;margin-bottom:14px;">
            Cardiac triage, <span style="color:#22D3EE;">instantly.</span>
          </h1>
          <p style="color:#64748B;max-width:520px;margin:0 auto 28px;line-height:1.7;">
            Upload a wearable ECG recording and receive a complete triage assessment — rhythm
            classification, vital signs, and severity grading within seconds. Designed for
            clinical review and patient monitoring.
          </p>
          <div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap;">
            <button
              style="background:#0891B2;color:#fff;padding:10px 24px;font-size:14px;border:none;border-radius:7px;cursor:pointer;"
              @click="router.push('/login')"
            >Get started →</button>
            <button
              style="background:transparent;border:1px solid #1A2740;color:#94A3B8;padding:10px 24px;font-size:14px;border-radius:7px;cursor:pointer;"
              @click="router.push('/login')"
            >View a result</button>
          </div>
          <p style="color:#3D5A7A;font-size:11px;margin-top:16px;">⚠ Educational project — not for clinical use</p>
        </div>

        <!-- SECTION 3 — How it works -->
        <div id="how-it-works" class="landing-section">
          <div class="landing-section-label" style="color:#22D3EE;">How it works</div>
          <h2 class="landing-section-title">From upload to triage in seconds</h2>
          <div class="landing-grid-3">
            <div class="feature-card">
              <div class="feature-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2" />
                  <polyline points="7 9 12 4 17 9" />
                  <line x1="12" y1="4" x2="12" y2="15" />
                </svg>
              </div>
              <div style="font-size:14px;font-weight:500;color:var(--tx);margin-bottom:6px;">Upload a recording</div>
              <div style="font-size:12px;color:var(--tm);line-height:1.6;">
                Select a .json file containing ECG and PPG signal data from any supported wearable
                device. The system accepts recordings from Apple Watch, Fitbit, Garmin, KardiaMobile,
                and more.
              </div>
            </div>
            <div class="feature-card">
              <div class="feature-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="4" y="4" width="16" height="16" rx="2" />
                  <rect x="9" y="9" width="6" height="6" />
                  <line x1="9" y1="1" x2="9" y2="4" /><line x1="15" y1="1" x2="15" y2="4" />
                  <line x1="9" y1="20" x2="9" y2="23" /><line x1="15" y1="20" x2="15" y2="23" />
                  <line x1="20" y1="9" x2="23" y2="9" /><line x1="20" y1="15" x2="23" y2="15" />
                  <line x1="1" y1="9" x2="4" y2="9" /><line x1="1" y1="15" x2="4" y2="15" />
                </svg>
              </div>
              <div style="font-size:14px;font-weight:500;color:var(--tx);margin-bottom:6px;">AI analyses the signal</div>
              <div style="font-size:12px;color:var(--tm);line-height:1.6;">
                Our trained PyTorch model processes the 30-second window through a dual-branch CNN
                + BiLSTM architecture, extracting rhythm, heart rate, HRV, SpO₂, and stress
                indicators simultaneously.
              </div>
            </div>
            <div class="feature-card">
              <div class="feature-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="5" y="3" width="14" height="18" rx="2" />
                  <line x1="9" y1="3" x2="15" y2="3" />
                  <path d="M8 13h2l1.5 3 2-6 1.5 3h2" />
                </svg>
              </div>
              <div style="font-size:14px;font-weight:500;color:var(--tx);margin-bottom:6px;">Review the triage result</div>
              <div style="font-size:12px;color:var(--tm);line-height:1.6;">
                Receive a severity grade (GREEN / YELLOW / RED), rhythm classification with
                confidence scores, and a full waveform visualisation of the ECG and PPG signal.
              </div>
            </div>
          </div>
        </div>

        <!-- SECTION 4 — Severity tiers -->
        <div style="background:#060C18;border-top:1px solid #0C2340;border-bottom:1px solid #0C2340;padding:48px 40px;">
          <div class="landing-section-label" style="color:#64748B;">Severity grading</div>
          <h2 class="landing-section-title" style="color:#F1F5F9;">Three-tier triage system</h2>
          <p class="landing-section-desc" style="margin:0;">
            Every recording is graded into one of three tiers based on rhythm classification,
            physiological thresholds, and a continuous severity score.
          </p>
          <div class="landing-grid-3">
            <div class="tier-card" style="background:#052E16;border:1px solid #064E23;">
              <div style="color:#86EFAC;font-size:22px;font-weight:500;margin-bottom:8px;">GREEN</div>
              <div style="color:#86EFAC;font-size:14px;margin-bottom:8px;">All clear</div>
              <div style="color:#4ADE80;opacity:0.7;font-size:13px;line-height:1.6;margin-bottom:12px;">
                Normal sinus rhythm. Vitals within expected ranges. Continue routine monitoring.
              </div>
              <div style="color:#86EFAC;opacity:0.5;font-size:11px;">Severity score &lt; 0.40</div>
            </div>
            <div class="tier-card" style="background:#422006;border:1px solid #7C2D12;">
              <div style="color:#FDE68A;font-size:22px;font-weight:500;margin-bottom:8px;">YELLOW</div>
              <div style="color:#FDE68A;font-size:14px;margin-bottom:8px;">Monitor closely</div>
              <div style="color:#FCD34D;opacity:0.7;font-size:13px;line-height:1.6;margin-bottom:12px;">
                Irregular rhythm or borderline vitals detected. Clinical review recommended.
              </div>
              <div style="color:#FDE68A;opacity:0.5;font-size:11px;">Severity score 0.40 – 0.72</div>
            </div>
            <div class="tier-card" style="background:#4C0519;border:1px solid #881337;">
              <div style="color:#FCA5A5;font-size:22px;font-weight:500;margin-bottom:8px;">RED</div>
              <div style="color:#FCA5A5;font-size:14px;margin-bottom:8px;">Urgent attention</div>
              <div style="color:#FCA5A5;opacity:0.7;font-size:13px;line-height:1.6;margin-bottom:12px;">
                Critical finding detected. High-confidence arrhythmia or physiological emergency
                threshold crossed.
              </div>
              <div style="color:#FCA5A5;opacity:0.5;font-size:11px;">Severity score &gt; 0.72</div>
            </div>
          </div>
        </div>

        <!-- SECTION 5 — Features -->
        <div id="features" class="landing-section">
          <div class="landing-section-label" style="color:var(--tm);">Features</div>
          <h2 class="landing-section-title">Everything you need for cardiac triage</h2>
          <div class="landing-grid-3">
            <div class="feature-card">
              <div class="feature-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M3 12h3l2-4 3 8 2-5 2 3h6" />
                  <path d="M19.5 12.6 12 20l-7.5-7.4a5 5 0 1 1 7.5-6.6 5 5 0 1 1 7.5 6.6Z" />
                </svg>
              </div>
              <div style="font-size:14px;font-weight:500;color:var(--tx);margin-bottom:6px;">Rhythm detection</div>
              <div style="font-size:12px;color:var(--tm);line-height:1.6;">
                Classifies Normal, AFib, Bradycardia, Tachycardia, and Anomaly with per-class
                probability scores.
              </div>
            </div>
            <div class="feature-card">
              <div class="feature-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="2 12 6 12 9 4 12 20 15 8 18 16 21 12" />
                </svg>
              </div>
              <div style="font-size:14px;font-weight:500;color:var(--tx);margin-bottom:6px;">Vital signs</div>
              <div style="font-size:12px;color:var(--tm);line-height:1.6;">
                Extracts heart rate, HRV (RMSSD), SpO₂ estimate, and stress level from ECG and PPG
                signals in a single inference pass.
              </div>
            </div>
            <div class="feature-card">
              <div class="feature-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="4 19 4 5" />
                  <polyline points="4 19 20 19" />
                  <polyline points="4 15 9 10 13 14 20 6" />
                </svg>
              </div>
              <div style="font-size:14px;font-weight:500;color:var(--tx);margin-bottom:6px;">Waveform visualisation</div>
              <div style="font-size:12px;color:var(--tm);line-height:1.6;">
                Renders the full 30-second ECG and PPG trace on a dark monitor panel — exactly as
                a clinician would review it.
              </div>
            </div>
            <div class="feature-card">
              <div class="feature-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="9" cy="7" r="4" />
                  <path d="M2 21v-2a4 4 0 0 1 4-4h6a4 4 0 0 1 4 4v2" />
                  <circle cx="17" cy="7" r="3" />
                  <path d="M22 21v-2a4 4 0 0 0-3-3.87" />
                </svg>
              </div>
              <div style="font-size:14px;font-weight:500;color:var(--tx);margin-bottom:6px;">Patient records</div>
              <div style="font-size:12px;color:var(--tm);line-height:1.6;">
                Create, update, and search patient profiles. Link unlimited recordings to each
                patient with full history.
              </div>
            </div>
            <div class="feature-card">
              <div class="feature-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="7" y="6" width="10" height="12" rx="2" />
                  <line x1="10" y1="2" x2="14" y2="2" />
                  <line x1="10" y1="22" x2="14" y2="22" />
                  <line x1="12" y1="9" x2="12" y2="12" />
                  <line x1="12" y1="12" x2="14" y2="13" />
                </svg>
              </div>
              <div style="font-size:14px;font-weight:500;color:var(--tx);margin-bottom:6px;">Multi-device support</div>
              <div style="font-size:12px;color:var(--tm);line-height:1.6;">
                Accepts recordings from Apple Watch, Samsung Galaxy Watch, Fitbit, Garmin,
                KardiaMobile, and generic wearables.
              </div>
            </div>
            <div class="feature-card">
              <div class="feature-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M7 8a5 5 0 0 0 0 8" />
                  <path d="M17 8a5 5 0 0 1 0 8" />
                  <path d="M4 5a9 9 0 0 0 0 14" />
                  <path d="M20 5a9 9 0 0 1 0 14" />
                  <circle cx="12" cy="12" r="2" />
                </svg>
              </div>
              <div style="font-size:14px;font-weight:500;color:var(--tx);margin-bottom:6px;">Live demo mode</div>
              <div style="font-size:12px;color:var(--tm);line-height:1.6;">
                Stream synthetic ECG/PPG in real time and watch the model classify rhythm and
                update severity live — no hardware required.
              </div>
            </div>
          </div>
        </div>

        <!-- SECTION 6 — Supported devices -->
        <div style="background:var(--su);border-top:1px solid var(--bd);border-bottom:1px solid var(--bd);padding:40px;">
          <div class="landing-section-label" style="color:var(--tm);text-align:center;margin-bottom:16px;">Compatible with</div>
          <div class="landing-devices">
            <span v-for="device in devices" :key="device" class="device-pill">{{ device }}</span>
          </div>
        </div>

        <!-- SECTION 7 — Tech stack -->
        <div class="landing-section" style="text-align:center;">
          <div class="landing-section-label" style="color:var(--tm);">Built with</div>
          <div class="landing-tech">
            <span v-for="tech in techStack" :key="tech" class="tech-pill">{{ tech }}</span>
          </div>
        </div>

        <!-- SECTION 8 — About the project -->
        <div style="background:#060C18;border-top:1px solid #0C2340;padding:48px 40px;text-align:center;">
          <div class="landing-badge">Academic project</div>
          <h2 style="color:#F1F5F9;font-size:22px;font-weight:500;margin-bottom:12px;">CardioTriage</h2>
          <p style="color:#64748B;max-width:500px;margin:0 auto;line-height:1.7;">
            Developed as a continuous assessment project at the Department of Computer Science,
            Rivers State University, Port Harcourt, Nigeria. This system is submitted in partial
            fulfillment of course requirements and is not intended for clinical deployment.
          </p>
          <button
            style="border:1px solid #1A2740;color:#94A3B8;background:transparent;border-radius:7px;padding:8px 20px;margin-top:20px;font-size:13px;cursor:pointer;"
            @click="router.push('/team')"
          >Meet the team →</button>
        </div>

        <!-- SECTION 9 — Footer -->
        <div class="landing-footer">
          <span style="color:#3D5A7A;font-size:12px;">CardioTriage · Rivers State University · 2026</span>
          <span style="color:#3D5A7A;font-size:11px;">⚠ Educational project — not for clinical use</span>
        </div>
      </div>
    </div>
  </PublicLayout>
</template>
