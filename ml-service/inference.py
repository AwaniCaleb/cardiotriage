"""
Model loading and inference logic for the wearable cardiac triage model.

The TorchScript model (triage_model.pt) is a traced wrapper that takes
(ecg, ppg) tensors of shape (1, 1, ECG_LEN) / (1, 1, PPG_LEN) and returns a
tuple: (rhythm_logits, stress_logits, spo2_pred, severity_score).
spo2_pred and severity_score already have sigmoid scaling applied inside the
model (spo2_pred in [85, 100], severity_score in [0, 1]).
"""
import os

import numpy as np
import torch
import torch.nn.functional as F

from preprocessor import (
    ECG_LEN,
    PPG_LEN,
    RHYTHM_CLASSES,
    STRESS_CLASSES,
    ECGPreprocessor,
    PPGPreprocessor,
    FeatureExtractor,
    classify_severity,
)

MODEL_PATH = os.getenv("MODEL_PATH", "./triage_model.pt")

model = torch.jit.load(MODEL_PATH, map_location="cpu")
model.eval()

_ecg_prep = ECGPreprocessor()
_ppg_prep = PPGPreprocessor()
_feat_ext = FeatureExtractor()


@torch.no_grad()
def run_inference(ecg_raw: np.ndarray, ppg_raw: np.ndarray) -> dict:
    """Runs the full triage pipeline on raw ECG/PPG signals."""
    # Preprocess
    ecg = _ecg_prep(ecg_raw)
    ppg = _ppg_prep(ppg_raw)

    # Rule-based vitals from preprocessed signals
    vitals = _feat_ext.extract_all(ecg, ppg)

    # Model inference
    ecg_t = torch.from_numpy(ecg.astype(np.float32)).reshape(1, 1, ECG_LEN)
    ppg_t = torch.from_numpy(ppg.astype(np.float32)).reshape(1, 1, PPG_LEN)

    rhythm_logits, stress_logits, spo2_pred, severity_score = model(ecg_t, ppg_t)

    rhythm_probs = F.softmax(rhythm_logits, dim=1).cpu().numpy()[0]
    stress_probs = F.softmax(stress_logits, dim=1).cpu().numpy()[0]

    rhythm_label = RHYTHM_CLASSES[int(rhythm_probs.argmax())]
    stress_label = STRESS_CLASSES[int(stress_probs.argmax())]

    severity_score_val = float(severity_score.cpu().item())
    spo2_pred_val = float(spo2_pred.cpu().item())

    # Blend model SpO2 estimate (60%) with feature-derived SpO2 (40%)
    blended_spo2 = 0.6 * spo2_pred_val + 0.4 * vitals['spo2']
    vitals['spo2'] = blended_spo2

    severity, reason = classify_severity(severity_score_val, vitals, rhythm_label)

    return {
        'severity': severity,
        'severity_score': severity_score_val,
        'rhythm_label': rhythm_label,
        'rhythm_probs': {c: float(p) for c, p in zip(RHYTHM_CLASSES, rhythm_probs)},
        'heart_rate': vitals['heart_rate'],
        'hrv_rmssd': vitals['hrv_rmssd'],
        'spo2': blended_spo2,
        'stress_level': stress_label,
        'stress_probs': {c: float(p) for c, p in zip(STRESS_CLASSES, stress_probs)},
    }
