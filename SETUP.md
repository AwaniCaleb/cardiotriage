# CardioTriage — Local Development Setup

This guide walks you through setting up the full CardioTriage stack on your local machine. It assumes you know basic Git but nothing else about the project. Follow each section in order.

---

## 1. Prerequisites

Install all of these before anything else.

| Tool | Version | Download |
|------|---------|----------|
| Node.js | 20+ | https://nodejs.org |
| Java JDK | 21 (Eclipse Temurin) | https://adoptium.net |
| Python | 3.11+ | https://python.org |
| Git | Any recent | https://git-scm.com |
| VS Code | Any recent (recommended) | https://code.visualstudio.com |

**VS Code extensions to install** (search by name in the Extensions panel):

- `Extension Pack for Java` — Microsoft
- `Jupyter` — Microsoft
- `Vue - Official` — Vue.js
- `Tailwind CSS IntelliSense` — Bradlc

---

## 2. Clone the Repository

```bash
git clone https://github.com/[username]/cardiotriage.git
cd cardiotriage
git checkout development
```

> All feature work happens on the `development` branch. Never work directly on `main`.

---

## 3. Set Up the Python Virtual Environment

From the project root:

```bash
python -m venv .venv
```

Activate it:

```bash
# Windows (PowerShell)
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
```

You should see `(.venv)` at the start of your terminal prompt. Now install the ML service dependencies:

```bash
pip install -r ml-service/requirements.txt
```

---

## 4. Configure the Backend Database

The backend requires a PostgreSQL database. The easiest free option is [Neon](https://neon.tech).

**Step-by-step:**

a) Go to https://neon.tech and sign up (GitHub login works).  
b) Create a new project — name it `cardiotriage`.  
c) In the Neon dashboard go to **SQL Editor** and run:
   ```sql
   CREATE DATABASE cardiotriage;
   ```
d) Go to **Connection Details**. Copy the **Direct** connection string.  
   > ⚠ Make sure the hostname does **NOT** contain `-pooler`. Use the direct connection, not the pooler URL.

**Create the local config file:**

Create this file (it is gitignored — never commit it):

```
backend/src/main/resources/application-local.properties
```

Paste and fill in your Neon credentials:

```properties
spring.datasource.url=jdbc:postgresql://[YOUR-NEON-HOST]/cardiotriage?sslmode=require&prepareThreshold=0
spring.datasource.username=[YOUR-NEON-USERNAME]
spring.datasource.password=[YOUR-NEON-PASSWORD]
spring.jpa.hibernate.ddl-auto=update
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.PostgreSQLDialect
jwt.secret=cardiotriage-local-dev-secret-32chars-min
jwt.expiration=86400000
ml.service.url=http://localhost:8000
file.upload-dir=./uploads
spring.servlet.multipart.max-file-size=10MB
spring.servlet.multipart.max-request-size=10MB
```

---

## 5. Create the ML Service Config

Create this file (also gitignored — never commit it):

```
ml-service/.env
```

Contents:

```env
MODEL_PATH=./triage_model.pt
PORT=8000
```

---

## 6. Running the Application

You need **three separate terminals** open at the same time — one for each service.

### Terminal 1 — ML Service (start this first)

```bash
# Windows
.venv\Scripts\activate
cd ml-service
uvicorn main:app --reload --port 8000

# Mac / Linux
source .venv/bin/activate
cd ml-service
uvicorn main:app --reload --port 8000
```

Ready when you see:
```
Uvicorn running on http://0.0.0.0:8000
```

---

### Terminal 2 — Spring Boot Backend

```bash
cd backend
```

**Windows PowerShell:**
```powershell
$env:SPRING_PROFILES_ACTIVE="local"; ./mvnw spring-boot:run
```

**Mac / Linux:**
```bash
SPRING_PROFILES_ACTIVE=local ./mvnw spring-boot:run
```

> ⚠ The first run downloads all Maven dependencies — this can take **3–5 minutes**. Be patient.

Ready when you see:
```
Started CardioTriageApplication in X.XXX seconds
```

---

### Terminal 3 — Vue Frontend

```bash
cd frontend
npm install
npm run dev
```

Ready when you see:
```
Local:   http://localhost:5173/
```

Open http://localhost:5173 in your browser.

---

## 7. Creating Your First Account

The application has no pre-seeded users locally. Register an account first.

**Option A — Browser console (fastest):**

Open http://localhost:5173, press `F12` to open DevTools, go to the **Console** tab, and paste:

```javascript
fetch('http://localhost:8080/api/auth/register', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    email: 'your@email.com',
    password: 'yourpassword',
    confirmPassword: 'yourpassword'
  })
}).then(r => r.json()).then(console.log)
```

Then go to http://localhost:5173/login and sign in with those credentials.

---

## 8. Common Issues and Fixes

**Issue: "Unknown lifecycle phase" error running mvnw**  
Fix: On Windows PowerShell, quote the `-D` flag:
```powershell
./mvnw spring-boot:run "-Dspring-boot.run.profiles=local"
```

---

**Issue: "database does not exist" or connection error**  
Fix: Make sure you used the **direct** Neon connection (no `-pooler` in the hostname). Also confirm the database name is exactly `cardiotriage` with no trailing spaces.

---

**Issue: Login works but the app shows no data**  
Fix: Your JWT token may have expired (24-hour lifetime). Log out and log back in.

---

**Issue: Live Demo waveforms are not animating**  
Fix: The strip-chart animation uses `requestAnimationFrame`, which pauses when the tab is in the background. Switch to the Live Demo tab directly and keep it in focus.

---

**Issue: ML service crashes on startup**  
Fix: Make sure your virtual environment is activated before running `uvicorn`. Also confirm that `triage_model.pt` exists in the `ml-service/` directory.

---

**Issue: First login on the deployed app is very slow**  
Fix: Render free tier services sleep after 15 minutes of inactivity. The first request after a sleep takes 30–60 seconds. Wait and retry — it will respond.

---

## 9. Project Architecture Overview

For a comprehensive technical overview of every decision made in this project — including the full API reference, database schema, environment variable documentation, and known issues — read **[CLAUDE.md](CLAUDE.md)** in the repo root.

---

## 10. Contributing

- Always work on the `development` branch
- Never push directly to `main`
- Merge `development` → `main` only when features are stable and tested
- `CLAUDE.md` is the source of truth for this project's technical decisions
