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
├── ml-service/       Python FastAPI + triage model
│   └── triage_model.pt  Pre-traced TorchScript model
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
CORS_ORIGINS=http://localhost:5173
UPLOAD_DIR=./uploads
```

### ml-service/
```
MODEL_PATH=./triage_model.pt
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
                hrv_rmssd, spo2, stress_level, created_at)
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
GET    /api/recordings/{id}
GET    /api/patients/{id}/recordings

GET    /api/triage/{recordingId}
GET    /api/triage/stream          SSE live demo endpoint

GET    /api/dashboard/stats
```

## Build Commands
```bash
# Backend
mvn compile -f backend/pom.xml
mvn spring-boot:run -f backend/pom.xml

# Frontend (once scaffolded)
cd frontend && npm run dev

# ML Service (once scaffolded)
cd ml-service && uvicorn main:app --reload --port 8000
```

## What Is Built So Far
- [x] Project folder structure
- [x] TorchScript model exported (triage_model.pt in ml-service/)
- [x] Spring Boot scaffold (pom.xml, main class, application.properties)
- [x] JWT auth system (User, JwtUtil, JwtAuthFilter, SecurityConfig,
      AuthService, AuthController)
- [x] Patient CRUD (Patient, PatientRepository, PatientRequest/Response/Summary,
      PatientService, PatientController)
- [ ] Recording upload
- [ ] Python ML service
- [ ] Triage results
- [ ] Vue frontend
- [ ] Dashboard
- [ ] Landing page
- [ ] Live SSE demo

## What To Build Next
Recording upload — patient ECG/PPG file upload endpoint and
recordings entity, then wire into Vue after the frontend is scaffolded.