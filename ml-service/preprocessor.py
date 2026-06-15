"""
Signal preprocessing, feature extraction, and severity classification.
Ported from notebooks/ecg_wearable_triage.ipynb — keep constants and
algorithms in sync with that notebook.
"""
from typing import Tuple

import numpy as np
from scipy import signal as scipy_signal

# ── Signal parameters ────────────────────────────────────────────────────────
ECG_FS = 256          # Hz — typical wearable ECG sampling rate
PPG_FS = 64           # Hz — typical wearable PPG sampling rate
WINDOW_SEC = 30       # seconds of signal per inference window
ECG_LEN = ECG_FS * WINDOW_SEC    # 7680 samples
PPG_LEN = PPG_FS * WINDOW_SEC    # 1920 samples

# ── Detection targets ────────────────────────────────────────────────────────
RHYTHM_CLASSES = ['Normal', 'AFib', 'Bradycardia', 'Tachycardia', 'Anomaly']
N_RHYTHM = len(RHYTHM_CLASSES)
STRESS_CLASSES = ['Low', 'Medium', 'High']

# ── Physiological thresholds ─────────────────────────────────────────────────
HR_BRADY_THRESH = 50      # bpm — below this → Bradycardia alert
HR_TACHY_THRESH = 120     # bpm — above this → Tachycardia alert
HR_CRITICAL_LOW = 40      # bpm — immediate emergency
HR_CRITICAL_HIGH = 150    # bpm — immediate emergency
SPO2_WARN_THRESH = 95.0   # % — below this → warning
SPO2_CRIT_THRESH = 90.0   # % — below this → emergency
HRV_LOW_THRESH = 20.0     # ms RMSSD — below this → high stress

# ── Severity score thresholds (0–1 scale) ────────────────────────────────────
YELLOW_THRESH = 0.40      # above → YELLOW alert
RED_THRESH = 0.72         # above → RED / emergency escalation


class ECGPreprocessor:
    """
    Cleans raw single-lead ECG from wearable.
    Handles baseline wander, powerline noise, and motion artefacts.
    """
    def __init__(self, fs: int = ECG_FS):
        self.fs = fs
        # Bandpass 0.5–40 Hz removes baseline wander + high-freq noise
        self.sos = scipy_signal.butter(
            4, [0.5, 40.0], btype='bandpass', fs=fs, output='sos'
        )

    def __call__(self, ecg: np.ndarray) -> np.ndarray:
        ecg = np.nan_to_num(ecg.astype(np.float32))
        ecg = scipy_signal.sosfiltfilt(self.sos, ecg)   # zero-phase filter
        # Clip extreme artefacts (> 5 std)
        mu, std = ecg.mean(), ecg.std() + 1e-8
        ecg = np.clip(ecg, mu - 5 * std, mu + 5 * std)
        # Z-score normalise
        return (ecg - mu) / std


class PPGPreprocessor:
    """
    Cleans raw PPG signal from optical wearable sensor.
    Removes DC offset and motion artefacts via bandpass filter.
    """
    def __init__(self, fs: int = PPG_FS):
        self.fs = fs
        # Bandpass 0.5–8 Hz — keeps cardiac pulse, removes motion/breathing
        self.sos = scipy_signal.butter(
            4, [0.5, 8.0], btype='bandpass', fs=fs, output='sos'
        )

    def __call__(self, ppg: np.ndarray) -> np.ndarray:
        ppg = np.nan_to_num(ppg.astype(np.float32))
        ppg = scipy_signal.sosfiltfilt(self.sos, ppg)
        mu, std = ppg.mean(), ppg.std() + 1e-8
        return (ppg - mu) / std


class FeatureExtractor:
    """
    Extracts physiological features from preprocessed signals.
    Used for rule-based validation alongside model predictions.
    """
    def __init__(self, ecg_fs: int = ECG_FS, ppg_fs: int = PPG_FS):
        self.ecg_fs = ecg_fs
        self.ppg_fs = ppg_fs

    def extract_hr_from_ppg(self, ppg: np.ndarray) -> float:
        """Estimate heart rate from PPG peak detection."""
        peaks, _ = scipy_signal.find_peaks(
            ppg, distance=int(self.ppg_fs * 0.4),   # min 40bpm
            height=0.3
        )
        if len(peaks) < 2:
            return 75.0   # fallback
        rr_intervals = np.diff(peaks) / self.ppg_fs   # seconds
        return float(60.0 / np.median(rr_intervals))

    def extract_hrv_rmssd(self, ppg: np.ndarray) -> float:
        """RMSSD from successive RR interval differences — HRV proxy for stress."""
        peaks, _ = scipy_signal.find_peaks(
            ppg, distance=int(self.ppg_fs * 0.4), height=0.3
        )
        if len(peaks) < 3:
            return 30.0   # fallback — normal HRV
        rr_ms = np.diff(peaks) / self.ppg_fs * 1000   # ms
        successive_diffs = np.diff(rr_ms)
        return float(np.sqrt(np.mean(successive_diffs ** 2)))

    def estimate_spo2(self, ppg: np.ndarray) -> float:
        """
        Simplified SpO2 estimation from single-channel PPG.
        Real devices use red + infrared channels; this approximates
        from AC/DC ratio of the PPG waveform.
        In production, replace with actual red/IR channel ratio.
        """
        ac = ppg.std()
        dc = np.abs(ppg.mean()) + 1e-8
        r = ac / dc
        # Empirical calibration curve: SpO2 ≈ 110 - 25*R
        spo2 = float(np.clip(110.0 - 25.0 * r, 85.0, 100.0))
        return spo2

    def extract_all(self, ecg: np.ndarray, ppg: np.ndarray) -> dict:
        hr = self.extract_hr_from_ppg(ppg)
        hrv = self.extract_hrv_rmssd(ppg)
        spo2 = self.estimate_spo2(ppg)
        return {'heart_rate': hr, 'hrv_rmssd': hrv, 'spo2': spo2}


def classify_severity(score: float, vitals: dict, rhythm: str) -> Tuple[str, str]:
    """
    Determines severity tier from the model's severity score plus hard
    physiological rules.

    Hard RED overrides exist because the model should NEVER miss a
    critically dangerous vital sign, even if it hasn't been trained on it.

    Returns (severity, reason).
    """
    # ── Hard RED rules (physiological emergency overrides) ────────────
    if vitals['heart_rate'] < HR_CRITICAL_LOW:
        return 'RED', f'Critical bradycardia: {vitals["heart_rate"]:.0f} bpm'
    if vitals['heart_rate'] > HR_CRITICAL_HIGH:
        return 'RED', f'Critical tachycardia: {vitals["heart_rate"]:.0f} bpm'
    if vitals['spo2'] < SPO2_CRIT_THRESH:
        return 'RED', f'Critical hypoxia: SpO2 {vitals["spo2"]:.1f}%'

    # ── Model score tiers ─────────────────────────────────────────────
    if score >= RED_THRESH:
        reasons = [f'Severity score {score:.2f}']
        if vitals['spo2'] < SPO2_WARN_THRESH:
            reasons.append(f'Low SpO2 {vitals["spo2"]:.1f}%')
        return 'RED', ' + '.join(reasons)

    if score >= YELLOW_THRESH:
        reasons = []
        if vitals['spo2'] < SPO2_WARN_THRESH:
            reasons.append(f'SpO2 {vitals["spo2"]:.1f}%')
        if rhythm != 'Normal':
            reasons.append(f'{rhythm} detected')
        if vitals['hrv_rmssd'] < HRV_LOW_THRESH:
            reasons.append(f'Low HRV {vitals["hrv_rmssd"]:.1f}ms')
        reason = ' + '.join(reasons) if reasons else f'Score {score:.2f}'
        return 'YELLOW', reason

    return 'GREEN', ''
