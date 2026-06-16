#!/usr/bin/env python3
"""
Seed rich demo data for CardioTriage production database.
Run from project root: python seed_demo_data.py
"""
import sys, os, json, tempfile
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ml-service'))
from generator import generate_ecg, generate_ppg, get_demo_vitals

BASE = "https://cardiotriage-backend.onrender.com/api"

# ── Step 0: Wake up the Render service ────────────────────────────────────────
print("Waking up Render backend (may take ~60 s if cold)...")
for attempt in range(1, 6):
    try:
        r = requests.get("https://cardiotriage-backend.onrender.com/health", timeout=90)
        if r.status_code == 200:
            print(f"  Backend awake (attempt {attempt})")
            break
    except requests.exceptions.Timeout:
        print(f"  Attempt {attempt} timed out, retrying...")
else:
    print("  WARNING: health check never returned 200, proceeding anyway")

# ── Step 1: Login ──────────────────────────────────────────────────────────────
print("Logging in...")
r = requests.post(f"{BASE}/auth/login",
                  json={"email": "doctor@cardiotriage.com", "password": "password123"},
                  timeout=120)
r.raise_for_status()
token = r.json()["token"]
AUTH  = {"Authorization": f"Bearer {token}"}
print(f"  OK — token starts {token[:20]}...")

# ── Step 2: Patient definitions ────────────────────────────────────────────────
PATIENTS = [
    {
        "name": "Ngozi Adeyemi", "age": 58, "gender": "Female", "bloodType": "AB+",
        "conditions": "Atrial Fibrillation, Hypertension",
        "medications": "Warfarin 5mg, Ramipril 10mg",
        "emergencyContact": json.dumps({"name": "Emeka Adeyemi", "phone": "+234 80 5555 6666"}),
        "_rhythm": "AFib",
    },
    {
        "name": "Tunde Bakare", "age": 72, "gender": "Male", "bloodType": "O-",
        "conditions": "Third-degree Heart Block, Bradycardia",
        "medications": "Atropine PRN, Digoxin 0.125mg",
        "emergencyContact": json.dumps({"name": "Bisi Bakare", "phone": "+234 81 7777 8888"}),
        "_rhythm": "Bradycardia",
    },
    {
        "name": "Chioma Obi", "age": 34, "gender": "Female", "bloodType": "B+",
        "conditions": "Paroxysmal Tachycardia",
        "medications": "Metoprolol 50mg, Flecainide 100mg",
        "emergencyContact": json.dumps({"name": "Ikenna Obi", "phone": "+234 80 1111 3333"}),
        "_rhythm": "Tachycardia",
    },
    {
        "name": "Seun Adesanya", "age": 45, "gender": "Male", "bloodType": "A+",
        "conditions": "None known",
        "medications": "None",
        "emergencyContact": json.dumps({"name": "Kemi Adesanya", "phone": "+234 80 9999 0000"}),
        "_rhythm": "Normal",
    },
]

# ── Helper: generate signal JSON, POST as multipart, return triage result ──────
def upload_recording(patient_id, rhythm, device_type="kardia_mobile"):
    vitals = get_demo_vitals(rhythm)
    ecg    = generate_ecg(rhythm).tolist()
    ppg    = generate_ppg(vitals["hr"], vitals["spo2"], vitals["stress"]).tolist()
    payload = {"ecg_signal": ecg, "ppg_signal": ppg, "device_type": device_type}

    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    json.dump(payload, tmp); tmp.close()
    try:
        with open(tmp.name, 'rb') as f:
            r = requests.post(
                f"{BASE}/recordings/upload",
                headers=AUTH,
                data={"patientId": patient_id, "deviceType": device_type},
                files={"file": (f"rec_{patient_id}_{rhythm}.json", f, "application/json")},
                timeout=120,
            )
        r.raise_for_status()
        return r.json()
    finally:
        os.unlink(tmp.name)

# ── Step 3: Create patients + upload recordings ────────────────────────────────
print()
for p in PATIENTS:
    rhythm = p.pop("_rhythm")
    body   = {k: v for k, v in p.items()}

    print(f"Creating {p['name']}...")
    r = requests.post(f"{BASE}/patients", json=body, headers=AUTH, timeout=60)
    r.raise_for_status()
    pid = r.json()["id"]
    print(f"  id={pid}")

    print(f"  Uploading {rhythm} recording (this may take ~30 s while Render wakes)...")
    result = upload_recording(pid, rhythm)
    print(f"  severity={result.get('severity'):<8} "
          f"rhythmLabel={result.get('rhythmLabel'):<12} "
          f"heartRate={result.get('heartRate', 0):.0f} bpm  "
          f"spo2={result.get('spo2', 0):.1f}%")

# ── Step 4: Extra AFib recording for Chidi Nwosu (id=5) ───────────────────────
print("\nUploading extra AFib recording for Chidi Nwosu (id=5)...")
result = upload_recording(5, "AFib")
print(f"  severity={result.get('severity'):<8} "
      f"rhythmLabel={result.get('rhythmLabel'):<12} "
      f"heartRate={result.get('heartRate', 0):.0f} bpm  "
      f"spo2={result.get('spo2', 0):.1f}%")

# ── Step 5: Final dashboard stats ─────────────────────────────────────────────
print("\nFetching dashboard stats...")
r = requests.get(f"{BASE}/dashboard/stats", headers=AUTH, timeout=30)
r.raise_for_status()
s = r.json()
print(f"  totalPatients={s['totalPatients']}  "
      f"totalRecordings={s['totalRecordings']}  "
      f"criticalAlerts={s['criticalAlerts']}")
print("\nDone.")
