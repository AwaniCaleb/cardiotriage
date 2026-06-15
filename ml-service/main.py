"""
CardioTriage ML Service — FastAPI app.

Educational project — not for clinical use.
"""
import asyncio
import json

import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from sse_starlette.sse import EventSourceResponse

from preprocessor import ECG_LEN, PPG_LEN, RHYTHM_CLASSES
from generator import generate_ecg, generate_ppg, get_demo_vitals
from inference import run_inference

app = FastAPI(title="CardioTriage ML Service")

# CORS: allow all origins for now (we lock this down at deployment)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TriageRequest(BaseModel):
    ecg_signal: list[float] = Field(..., description=f"ECG samples, length {ECG_LEN}")
    ppg_signal: list[float] = Field(..., description=f"PPG samples, length {PPG_LEN}")
    device_type: str = "generic_wearable"

    @field_validator("ecg_signal")
    @classmethod
    def validate_ecg_length(cls, v: list[float]) -> list[float]:
        if len(v) != ECG_LEN:
            raise ValueError(f"ecg_signal must contain exactly {ECG_LEN} samples, got {len(v)}")
        return v

    @field_validator("ppg_signal")
    @classmethod
    def validate_ppg_length(cls, v: list[float]) -> list[float]:
        if len(v) != PPG_LEN:
            raise ValueError(f"ppg_signal must contain exactly {PPG_LEN} samples, got {len(v)}")
        return v


class TriageResponse(BaseModel):
    severity: str
    severity_score: float
    rhythm_label: str
    rhythm_probs: dict
    heart_rate: float
    hrv_rmssd: float
    spo2: float
    stress_level: str
    stress_probs: dict


@app.get("/health")
def health():
    return {"status": "ok", "model": "loaded"}


@app.post("/triage", response_model=TriageResponse)
def triage(request: TriageRequest):
    try:
        ecg = np.array(request.ecg_signal, dtype=np.float32)
        ppg = np.array(request.ppg_signal, dtype=np.float32)
        result = run_inference(ecg, ppg)
        return TriageResponse(**result)
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/triage/stream")
async def triage_stream(rhythm: str = "Normal"):
    if rhythm not in RHYTHM_CLASSES:
        rhythm = "Normal"

    async def event_generator():
        for _ in range(30):
            vitals = get_demo_vitals(rhythm)
            ecg = generate_ecg(rhythm)
            ppg = generate_ppg(vitals["hr"], vitals["spo2"], vitals["stress"])
            result = run_inference(ecg, ppg)
            yield {"event": "triage", "data": json.dumps(result)}
            await asyncio.sleep(5)

    return EventSourceResponse(event_generator())
