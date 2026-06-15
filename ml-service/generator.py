"""
Synthetic ECG/PPG signal generator for the live SSE demo.
Simplified port of the signal generators from
notebooks/ecg_wearable_triage.ipynb.
"""
import numpy as np
from scipy import signal as scipy_signal

from preprocessor import ECG_FS, PPG_FS, WINDOW_SEC


def generate_ecg(rhythm: str, fs: int = ECG_FS, duration: int = WINDOW_SEC) -> np.ndarray:
    """Generates synthetic single-lead ECG for a given rhythm class."""
    T = fs * duration
    t = np.linspace(0, duration, T)
    noise = np.random.normal(0, 0.05, T)

    if rhythm == 'Normal':
        hr = np.random.uniform(60, 100)
        rr = fs * 60 / hr
        beats = np.arange(0, T, rr).astype(int)
        ecg = noise.copy()
        for b in beats:
            if b + 30 < T:
                # P wave
                ecg[b:b + 10] += 0.15 * scipy_signal.windows.gaussian(10, 3)
                # QRS complex
                ecg[b + 10:b + 20] += 1.0 * scipy_signal.windows.gaussian(10, 2)
                # T wave
                ecg[b + 20:b + 30] += 0.25 * scipy_signal.windows.gaussian(10, 4)

    elif rhythm == 'AFib':
        # Irregular RR intervals + no P wave
        ecg = noise.copy()
        ecg += 0.08 * np.random.randn(T)   # fibrillatory baseline
        beat_pos = 0
        while beat_pos < T:
            rr = int(np.random.uniform(0.4, 1.2) * fs)
            if beat_pos + 20 < T:
                ecg[beat_pos:beat_pos + 15] += 0.9 * scipy_signal.windows.gaussian(15, 2)
            beat_pos += rr

    elif rhythm == 'Bradycardia':
        hr = np.random.uniform(40, 50)
        rr = int(fs * 60 / hr)
        ecg = noise.copy()
        for b in range(0, T, rr):
            if b + 30 < T:
                ecg[b + 10:b + 20] += 1.0 * scipy_signal.windows.gaussian(10, 2)
                ecg[b + 20:b + 30] += 0.2 * scipy_signal.windows.gaussian(10, 4)

    elif rhythm == 'Tachycardia':
        hr = np.random.uniform(120, 150)
        rr = int(fs * 60 / hr)
        ecg = noise.copy()
        for b in range(0, T, rr):
            if b + 15 < T:
                ecg[b:b + 10] += 0.8 * scipy_signal.windows.gaussian(10, 2)

    else:  # Anomaly
        ecg = noise + 0.3 * np.sin(2 * np.pi * 1.5 * t) + np.random.randn(T) * 0.2

    return ecg


def generate_ppg(hr: float, spo2: float, stress: str,
                 fs: int = PPG_FS, duration: int = WINDOW_SEC) -> np.ndarray:
    """Generates synthetic PPG matching given HR, SpO2, and stress level."""
    T = fs * duration
    rr = fs * 60 / hr
    # HRV jitter based on stress (high stress = low HRV = regular intervals)
    jitter_std = {'Low': 0.05, 'Medium': 0.02, 'High': 0.005}[stress]
    ppg = np.zeros(T)
    beat_pos = 0
    while beat_pos < T:
        jitter = int(np.random.normal(0, jitter_std * fs))
        pos = int(beat_pos) + jitter
        width = max(8, int(fs * 0.3))
        if 0 < pos < T - width:
            ppg[pos:pos + width] += scipy_signal.windows.gaussian(width, width // 4)
        beat_pos += rr
    # SpO2 amplitude effect: lower SpO2 → reduced AC amplitude
    amplitude = (spo2 - 85) / 15.0
    ppg *= amplitude
    ppg += np.random.normal(0, 0.03, T)
    return ppg


def get_demo_vitals(rhythm: str) -> dict:
    """Returns sensible HR/SpO2/stress values per rhythm for the demo stream."""
    vitals_map = {
        'Normal':      {'hr': 75,  'spo2': 98, 'stress': 'Low'},
        'AFib':        {'hr': 110, 'spo2': 94, 'stress': 'High'},
        'Bradycardia': {'hr': 45,  'spo2': 96, 'stress': 'Medium'},
        'Tachycardia': {'hr': 135, 'spo2': 95, 'stress': 'High'},
        'Anomaly':     {'hr': 88,  'spo2': 91, 'stress': 'Medium'},
    }
    return vitals_map.get(rhythm, vitals_map['Normal'])
