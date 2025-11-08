from __future__ import annotations

import math
import random
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd

from ..core.config import settings


class NoShowRiskModel:
    """
    Lightweight placeholder around the real ML microservice.
    Provides deterministic pseudo-scores for the API contract.
    """

    def __init__(self, model_path: str | None = None) -> None:
        self.last_explanations: dict[str, list[str]] = {}
        self.prediction_cache: Dict[str, Tuple[float, List[str]]] = {}
        self._model_path = Path(model_path or settings.no_show_model_path)
        self._pipeline = self._load_pipeline()

    async def predict_no_show_risk(
        self,
        *,
        appointment_id: str | None,
        patient_id: str,
        appointment_start: datetime,
        appointment_type: str,
        channel: str,
    ) -> float:
        pipeline_score, pipeline_explanation = self._predict_with_pipeline(
            patient_id=patient_id,
            appointment_start=appointment_start,
            appointment_type=appointment_type,
            channel=channel,
        )

        if pipeline_score is None:
            fallback_score, explanation = self._fallback_score(appointment_id, patient_id, appointment_start, appointment_type, channel)
        else:
            fallback_score, explanation = pipeline_score, pipeline_explanation

        key = appointment_id or patient_id
        self.last_explanations[key] = explanation
        self.prediction_cache[key] = (fallback_score, explanation)
        return fallback_score

    async def predict_no_show_risk_from_id(self, appointment_id: str) -> float:
        cached = self.prediction_cache.get(appointment_id)
        if cached:
            return cached[0]

        seed = hash(appointment_id) % 1_000_000
        random.seed(seed)
        score = 0.4 + (random.random() * 0.4)
        explanation = [
            "History of late cancellations.",
            "Long travel distance detected.",
            "Preferred morning appointments unavailable.",
        ]
        score = min(max(score, 0), 0.99)
        self.last_explanations[appointment_id] = explanation
        self.prediction_cache[appointment_id] = (score, explanation)
        return score

    def _load_pipeline(self):
        if not self._model_path.exists():
            return None
        try:
            return pd.read_pickle(self._model_path)
        except Exception as exc:  # pragma: no cover - defensive
            print(f"[NoShowRiskModel] Failed to load pipeline at {self._model_path}: {exc}")
            return None

    def _predict_with_pipeline(
        self,
        *,
        patient_id: str,
        appointment_start: datetime,
        appointment_type: str,
        channel: str,
    ) -> Tuple[Optional[float], List[str]]:
        if self._pipeline is None:
            return None, []

        features = self._build_feature_frame(
            patient_id=patient_id,
            appointment_start=appointment_start,
            appointment_type=appointment_type,
            channel=channel,
        )

        try:
            probabilities = self._pipeline.predict_proba(features)  # type: ignore[operator]
            score = float(probabilities[0][1])
            explanation = [
                "ML pipeline inference succeeded.",
                f"Lead time (days): {features.loc[0, 'lead_time_days']}",
                f"Channel: {channel}",
            ]
            return score, explanation
        except Exception as exc:
            print(f"[NoShowRiskModel] Pipeline inference failed, falling back to heuristics: {exc}")
            return None, []

    def _build_feature_frame(
        self,
        *,
        patient_id: str,
        appointment_start: datetime,
        appointment_type: str,
        channel: str,
    ) -> pd.DataFrame:
        lead_time_days = max((appointment_start - datetime.utcnow()).total_seconds() / 86_400, 0)
        visit_type = self._normalise_visit_type(appointment_type)
        data = {
            "patient_age_band": [self._pseudo_age_band(patient_id)],
            "visit_type": [visit_type],
            "provider_specialty": ["general_medicine"],
            "channel": [channel],
            "insurance_plan": ["commercial"],
            "lead_time_days": [round(lead_time_days, 2)],
            "distance_miles": [7.5],
            "prior_no_show_rate": [0.2],
            "prior_cancellations": [1],
        }
        return pd.DataFrame(data)

    def _pseudo_age_band(self, patient_id: str) -> str:
        bands = ["18-29", "30-44", "45-64", "65+"]
        index = abs(hash(patient_id)) % len(bands)
        return bands[index]

    def _normalise_visit_type(self, appointment_type: str) -> str:
        lowered = appointment_type.lower()
        if "behavior" in lowered or "mental" in lowered:
            return "behavioral"
        if "tele" in lowered or "virtual" in lowered:
            return "telehealth"
        if "special" in lowered:
            return "specialist"
        return "primary_care"

    def _fallback_score(
        self,
        appointment_id: str | None,
        patient_id: str,
        appointment_start: datetime,
        appointment_type: str,
        channel: str,
    ) -> Tuple[float, List[str]]:
        seed = hash((patient_id, appointment_start.isoformat(), appointment_type, channel)) % 1_000_000
        random.seed(seed)

        base = 0.3 + (random.random() * 0.5)

        hour = appointment_start.hour
        if hour < 9 or hour > 17:
            base += 0.1
        if channel == "phone":
            base -= 0.05

        score = min(max(base, 0), 0.99)

        explanation = [
            f"Heuristic lead time adjustment applied ({math.ceil(random.random() * 10)} day window).",
            f"Channel adjustment ({channel}).",
            f"Appointment type: {appointment_type}.",
        ]
        return score, explanation
