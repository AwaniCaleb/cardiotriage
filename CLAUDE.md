# CardioTriage — CLAUDE.md

## What This Project Is
A clinical web application that accepts wearable ECG/PPG recordings,
runs them through a pre-trained PyTorch triage model, and displays
waveforms + health triage results. Built as a school project.

## Architecture — Three Services
```
Vue.js (Vercel) → Spring Boot REST API (Render) → PostgreSQL (Neon)
                                                 → Python FastAPI (Render)
```

## Tech Stack
- Backend:    Java 21, Spring Boot 3.4.1, Maven, Spring Security, JWT (jjwt 0.12.3)
- Frontend:   Vue.js 3, Vite, Tailwind CSS, Chart.js
- ML Service: Python, FastAPI, PyTorch (CPU-only), TorchScript
- Database:   PostgreSQL 16 (Neon free tier)
- Hosting:    Render (backend + ml-service), Vercel (frontend), Neon (DB)

## Directory Structure
```
cardiotriage/
├── backend/          Java Spring Boot REST API
├── frontend/         Vue.js + Vite + Tailwind
│   └── src/
│       ├── api/          Axios API client modules
│       ├── layouts/      AppLayout, PublicLayout
│       ├── pages/        One .vue file per route
│       ├── router/       Vue Router config
│       ├── stores/       Pinia state stores
│       └── utils/        Shared helpers
├── ml-service/       Python FastAPI + triage model
│   ├── main.py           FastAPI app, /health /triage /triage/stream
│   ├── inference.py      TorchScript model loader + run_inference()
│   ├── preprocessor.py   ECG/PPG normalisation, feature extraction
│   ├── generator.py      Synthetic signal generator for live demo
│   ├── requirements.txt
│   └── triage_model.pt   Pre-traced TorchScript model (do not retrain here)
├── notebooks/        Original Jupyter notebook (do not modify)
└── CLAUDE.md
```

## Key Decisions & Constraints
- Java is MANDATED by the course — do not suggest replacing it
- ML model is TorchScript (.pt), NOT ONNX (ONNX export failed due to
  PyTorch 2.x dynamo incompatibility with BiLSTM)
- ML service uses CPU-only PyTorch to fit free hosting RAM limits
- Frontend is Vue 3 SPA (NOT Thymeleaf) — Spring Boot is pure REST API
- No emergency auto-dial/GPS features — scoped out for safety
- Add "Educational project — not for clinical use" disclaimer on all pages
- Git workflow: feature work on development branch, merge to main when stable

## Environment Variables Needed

### backend/
```
DB_URL=jdbc:postgresql://localhost:5432/cardiotriage
DB_USERNAME=postgres
DB_PASSWORD=yourpassword
JWT_SECRET=cardiotriage-dev-secret-change-in-production
ML_SERVICE_URL=http://localhost:8000
CORS_ALLOWED_ORIGINS=http://localhost:5173
FILE_UPLOAD_DIR=./uploads
```

### ml-service/
```
MODEL_PATH=./triage_model.pt
PORT=8000
```

## JDK 25 Fix (Already Applied)
Lombok requires explicit annotationProcessorPaths in pom.xml on JDK 25.
This is already in place — do not remove it.

## Database Schema
```sql
users          (id, email, password_hash, role, created_at)
patients       (id, name, age, gender, blood_type, conditions,
                medications, emergency_contact, created_at, updated_at)
recordings     (id, patient_id, device_type, ecg_file_path,
                ppg_file_path, uploaded_at)
triage_results (id, recording_id, severity, severity_score,
                rhythm_label, rhythm_probs, heart_rate,
                hrv_rmssd, spo2, stress_level, stress_probs, created_at)
```

## API Endpoints
```
POST   /api/auth/register
POST   /api/auth/login

GET    /api/patients
POST   /api/patients
GET    /api/patients/{id}
PUT    /api/patients/{id}
DELETE /api/patients/{id}

POST   /api/recordings/upload
GET    /api/recordings/{id}/signals   Raw ECG/PPG arrays for chart rendering
GET    /api/patients/{id}/recordings

GET    /api/triage/{recordingId}
GET    /api/triage/stream             SSE live demo endpoint

GET    /api/dashboard/stats
```

## Build Commands
```bash
# Backend (local profile loads application-local.properties with Neon credentials)
SPRING_PROFILES_ACTIVE=local ./backend/mvnw spring-boot:run -f backend/pom.xml

# Frontend
cd frontend && npm run dev

# ML Service
cd ml-service && uvicorn main:app --reload --port 8000
```

## What Is Built So Far
- [x] Project folder structure
- [x] TorchScript model exported (triage_model.pt in ml-service/)
- [x] Spring Boot scaffold (pom.xml, main class, application.properties)
- [x] JWT auth system (User, JwtUtil, JwtAuthFilter, SecurityConfig,
      AuthService, AuthController) — auth errors return 400/401/409, not 500
- [x] Patient CRUD (Patient, PatientRepository, PatientRequest/Response/Summary,
      PatientService, PatientController) — cascade-deletes recordings + triage on delete
- [x] Recording upload (Recording, RecordingController, RecordingService)
- [x] Python ML service (main.py, inference.py, preprocessor.py, generator.py)
- [x] Triage results (TriageResult, TriageResultRepository, GET /api/triage/{recordingId})
- [x] Vue frontend (13 pages: Landing, Login, Dashboard, Patients, Add/Edit/Detail,
      TriageResult, LiveDemo, Team — plus AppLayout/PublicLayout, router, stores, api)
- [x] Dashboard (DashboardController → /api/dashboard/stats, DashboardPage.vue)
- [x] Landing page (LandingPage.vue)
- [x] Live SSE demo (TriageStreamController, LiveDemoPage.vue)

## What To Build Next
- [ ] Wire recording upload form in frontend to POST /api/recordings/upload
- [ ] Display triage results page after upload (TriageResultPage.vue ↔ GET /api/triage/{id})
- [ ] Render ECG/PPG waveforms in frontend using GET /api/recordings/{id}/signals + Chart.js
- [ ] Deployment: Render services (backend + ml-service), Vercel (frontend), env vars
