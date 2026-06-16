# CardioTriage — CLAUDE.md

## What This Project Is
A clinical web application that accepts wearable ECG/PPG recordings,
runs them through a pre-trained PyTorch triage model, and displays
waveforms + health triage results with a live streaming demo mode.
Built as a continuous assessment project at Rivers State University,
Department of Computer Science, Port Harcourt, Nigeria.

## Architecture — Three Services
```
Vue.js (Vercel) → Spring Boot REST API (Render) → PostgreSQL (Neon)
                                                 → Python FastAPI (Render)
```

## Live URLs
- Frontend:   https://cardiotriage.vercel.app
- Backend:    https://cardiotriage-backend.onrender.com
- ML Service: https://cardiotriage-ml.onrender.com
- Database:   Neon PostgreSQL (direct connection, not pooler)

## Tech Stack
- Backend:    Java 21, Spring Boot 3.4.1, Maven, Spring Security, JWT (jjwt 0.12.3)
- Frontend:   Vue.js 3, Vite, Tailwind CSS, Chart.js
- ML Service: Python, FastAPI, PyTorch (TorchScript, CPU-only)
- Database:   PostgreSQL 16 (Neon free tier)
- Hosting:    Render (backend + ml-service), Vercel (frontend), Neon (DB)

## Git Workflow
- Feature work on: development branch
- Stable releases on: main branch
- NEVER push directly to main — always merge from development
- CC must always: commit to development, then merge to main

## Directory Structure
```
cardiotriage/
├── backend/              Java Spring Boot REST API
│   ├── Dockerfile        Multi-stage Maven + JRE build for Render
│   └── src/main/
│       ├── java/com/cardiotriage/
│       │   ├── config/       SecurityConfig (CORS + JWT), RestTemplateConfig
│       │   ├── controller/   AuthController, PatientController, 
│       │   │                 RecordingController, TriageStreamController,
│       │   │                 DashboardController, HealthController
│       │   ├── dto/          Request/Response DTOs
│       │   ├── model/        User, Patient, Recording, TriageResult
│       │   ├── repository/   JPA repositories
│       │   ├── security/     JwtUtil, JwtAuthFilter, UserDetailsServiceImpl
│       │   └── service/      AuthService, PatientService, RecordingService
│       └── resources/
│           ├── application.properties
│           └── application-local.properties  ← gitignored, local only
├── frontend/             Vue.js 3 + Vite + Tailwind CSS
│   ├── vercel.json       SPA rewrite rule (all routes → index.html)
│   ├── design-reference/ mockup.html — approved UI reference
│   └── src/
│       ├── api/index.js      Axios instance, VITE_API_URL env var
│       ├── stores/           auth.js (Pinia), theme.js (Pinia)
│       ├── layouts/          AppLayout.vue, PublicLayout.vue
│       └── pages/            LandingPage, LoginPage, DashboardPage,
│                             PatientsPage, AddPatientPage, EditPatientPage,
│                             PatientDetailPage, TriageResultPage,
│                             LiveDemoPage, TeamPage
├── ml-service/           Python FastAPI + TorchScript model
│   ├── triage_model.pt   Pre-traced TorchScript model (committed)
│   ├── main.py           FastAPI app, endpoints
│   ├── preprocessor.py   ECG/PPG signal preprocessing (scipy)
│   ├── inference.py      TorchScript inference
│   └── generator.py      Synthetic signal generation for SSE demo
├── notebooks/            Original Jupyter notebook (do not modify)
│   └── ecg_wearable_triage.ipynb
└── CLAUDE.md

## Key Decisions & Constraints
- Java is MANDATED by the course — do not suggest replacing it
- ML model is TorchScript (.pt), NOT ONNX (ONNX export failed due to
  PyTorch 2.x dynamo incompatibility with BiLSTM)
- ML service uses CPU-only PyTorch to fit free hosting RAM limits
- Frontend is Vue 3 SPA (NOT Thymeleaf) — Spring Boot is pure REST API
- No emergency auto-dial/GPS features — scoped out for safety
- Always show "Educational project — not for clinical use" disclaimer
- Neon: use DIRECT connection (no -pooler in host), database = cardiotriage
- UptimeRobot pings both Render services every 5 min to prevent sleep

## JDK 25 Fix (Already Applied)
Lombok requires explicit annotationProcessorPaths in pom.xml on JDK 25.
Already in place — do not remove it.

## Known Issues / Watch Out For
- PowerShell: always quote -D flags: ./mvnw spring-boot:run "-Dspring-boot.run.profiles=local"
- Vercel: VITE_API_URL must be set in Vercel dashboard env vars
- EventSource (SSE) cannot send Authorization headers — /api/triage/stream is public (no auth)
- Canvas animation: all animation state (ecgDrawX, ppgDrawX, generators) must be plain JS variables, NOT Vue refs — Vue re-renders will disrupt animation

## Environment Variables

### backend/src/main/resources/application-local.properties (gitignored)
```
spring.datasource.url=jdbc:postgresql://ep-noisy-waterfall-add3lzoj.c-2.us-east-1.aws.neon.tech/cardiotriage?sslmode=require&prepareThreshold=0
spring.datasource.username=neondb_owner
spring.datasource.password=[see local file]
spring.jpa.hibernate.ddl-auto=update
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.PostgreSQLDialect
jwt.secret=cardiotriage-local-dev-secret-32chars-min
jwt.expiration=86400000
ml.service.url=http://localhost:8000
file.upload-dir=./uploads
spring.servlet.multipart.max-file-size=10MB
spring.servlet.multipart.max-request-size=10MB
```

### Render (backend) Environment Variables
```
DB_URL                 = jdbc:postgresql://ep-noisy-waterfall-add3lzoj.c-2.us-east-1.aws.neon.tech/cardiotriage?sslmode=require&prepareThreshold=0
DB_USERNAME            = neondb_owner
DB_PASSWORD            = [Neon password]
JWT_SECRET             = cardiotriage-prod-secret-min32chars-xyz
ML_SERVICE_URL         = https://cardiotriage-ml.onrender.com
CORS_ORIGINS           = https://cardiotriage.vercel.app
UPLOAD_DIR             = ./uploads
SPRING_PROFILES_ACTIVE = production
```

### Render (ml-service) Environment Variables
```
MODEL_PATH = ./triage_model.pt
```

### Vercel Environment Variables
```
VITE_API_URL = https://cardiotriage-backend.onrender.com/api
```

## Database Schema
```sql
users          (id, email, password_hash, role, created_at)
patients       (id, name, age, gender, blood_type, conditions,
                medications, emergency_contact, created_at, updated_at)
recordings     (id, patient_id, device_type, ecg_file_path,
                ppg_file_path, uploaded_at)
triage_results (id, recording_id, severity, severity_score,
                rhythm_label, rhythm_probs, heart_rate,
                hrv_rmssd, spo2, stress_level, created_at)
```

## API Endpoints
```
POST   /api/auth/register
POST   /api/auth/login
GET    /health                     ← public, used for UptimeRobot ping

GET    /api/patients
POST   /api/patients
GET    /api/patients/{id}
PUT    /api/patients/{id}
DELETE /api/patients/{id}          ← cascades to recordings + triage_results

POST   /api/recordings/upload
GET    /api/recordings/{id}
GET    /api/recordings/{id}/signals  ← downsampled ECG/PPG for charts
GET    /api/patients/{id}/recordings

GET    /api/triage/{recordingId}
GET    /api/triage/stream          ← SSE, PUBLIC (no auth), live demo

GET    /api/dashboard/stats
```

## Local Dev Commands
```bash
# Terminal 1 — Backend
cd backend
$env:SPRING_PROFILES_ACTIVE="local"; ./mvnw spring-boot:run

# Terminal 2 — ML Service
.venv\Scripts\activate
cd ml-service
uvicorn main:app --reload --port 8000

# Terminal 3 — Frontend
cd frontend
npm run dev
# App runs at http://localhost:5173
```

## What Is Complete
- [x] Spring Boot backend — all endpoints
- [x] Python ML service — preprocessing, inference, SSE stream
- [x] Vue frontend — all 10 pages
- [x] TorchScript model (triage_model.pt)
- [x] JWT auth (24-hour expiry)
- [x] CORS configured for production
- [x] Live Demo — strip chart ECG/PPG animation
- [x] TriageResultPage — real signals from /api/recordings/{id}/signals
- [x] Deployed: Vercel + Render + Neon
- [x] UptimeRobot keep-alive pings
- [x] Landing page (9 sections)
- [x] Team page (15 member slots — update data when available)
- [x] SPA routing (vercel.json rewrite)

## What Still Needs Doing
- [ ] Sidebar shows "Dr. Sarah Chen" placeholder — should show logged-in user email
- [ ] Dashboard stats showing 0 — investigate API call
- [ ] Team page — fill in real names, mat numbers, roles from group
- [ ] UI refinements (discussed, deferred)
- [ ] Technical report / documentation for submission
