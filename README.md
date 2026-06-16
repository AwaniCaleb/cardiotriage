# CardioTriage — AI-powered wearable ECG triage platform

[![Live App](https://img.shields.io/badge/Live%20App-cardiotriage.vercel.app-blue?style=flat-square)](https://cardiotriage.vercel.app)
[![Backend Health](https://img.shields.io/badge/Backend-health%20check-green?style=flat-square)](https://cardiotriage-backend.onrender.com/health)
[![Java](https://img.shields.io/badge/Java-21-orange?style=flat-square&logo=java)](https://adoptium.net)
[![Vue.js](https://img.shields.io/badge/Vue.js-3-41B883?style=flat-square&logo=vue.js)](https://vuejs.org)
[![Python](https://img.shields.io/badge/Python-FastAPI-009688?style=flat-square&logo=python)](https://fastapi.tiangolo.com)

CardioTriage is a clinical web application that accepts wearable ECG and PPG recordings, runs them through a pre-trained AI triage model, and displays waveform visualisations alongside severity-graded health assessments. It is designed for use by medical professionals who need rapid, first-pass screening of cardiac data from wearable devices. The platform was built as a continuous assessment project at Rivers State University, Department of Computer Science, Port Harcourt, Nigeria, for the 2025/2026 academic session.

---

## Features

- 🫀 12-lead ECG/PPG waveform visualisation from uploaded recordings
- 🤖 AI triage with severity grading (GREEN / YELLOW / RED)
- 📊 Real-time live demo with scrolling strip-chart animation
- 👥 Patient management — create, view, edit, and delete records
- 🔐 JWT authentication with 24-hour token expiry
- 🌙 Dark/light theme toggle
- 📱 Responsive design for desktop and tablet

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Vue.js 3, Vite, Tailwind CSS, Chart.js |
| Backend | Java 21, Spring Boot 3.4.1, Spring Security |
| ML Service | Python, FastAPI, PyTorch (TorchScript) |
| Database | PostgreSQL 16 (Neon) |
| Hosting | Vercel (frontend), Render (backend + ML) |

---

## Architecture

```
Browser (Vercel) ──→ Spring Boot API (Render) ──→ Neon PostgreSQL
                                              └──→ Python ML Service (Render)
```

The frontend is a Vue.js SPA served from Vercel. It communicates exclusively with the Spring Boot REST API on Render. The backend delegates AI inference to a separate Python FastAPI service that loads a TorchScript model. Data is persisted in a Neon PostgreSQL database using a direct (non-pooler) connection.

---

## Live Demo

**URL:** https://cardiotriage.vercel.app

**Demo credentials:**

| Field | Value |
|-------|-------|
| Email | doctor@cardiotriage.com |
| Password | password123 |

> **Note:** Render free tier services sleep after 15 minutes of inactivity. The first request after a sleep period may take 30–60 seconds. If the app appears unresponsive on first load, wait a moment and retry.

---

## Project Structure

```
cardiotriage/
├── backend/       Java Spring Boot REST API
├── frontend/      Vue.js 3 SPA
├── ml-service/    Python FastAPI + PyTorch model
├── notebooks/     Original Jupyter notebook (model training)
├── README.md
├── SETUP.md
└── CLAUDE.md
```

---

## Quick Start

See **[SETUP.md](SETUP.md)** for full local development instructions.

---

## Academic Context

**Institution:** Rivers State University  
**Department:** Computer Science  
**Programme:** Continuous Assessment Project — 2025/2026 Academic Session

> ⚠ **Educational project — not for clinical use.**  
> This system is built for academic demonstration purposes only. It must not be used to make real medical decisions.

---

## Team

Built by a team of Computer Science students at Rivers State University. See the [/team](https://cardiotriage.vercel.app/team) page for full team details.
