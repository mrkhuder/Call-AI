from __future__ import annotations

import math
import random
from datetime import datetime
from typing import Any


class NoShowRiskModel:
    """
    Lightweight placeholder around the real ML microservice.
    Provides deterministic pseudo-scores for the API contract.
    """

    def __init__(self) -> None:
        self.last_explanations: dict[str, list[str]] = {}

    async def predict_no_show_risk(
        self,
        *,
        appointment_id: str | None,
        patient_id: str,
        appointment_start: datetime,
        appointment_type: str,
        channel: str,
    ) -> float:
        seed = hash((patient_id, appointment_start.isoformat(), appointment_type, channel)) % 1_000_000
        random.seed(seed)

        base = 0.3 + (random.random() * 0.5)

        hour = appointment_start.hour
        if hour < 9 or hour > 17:
            base += 0.1
        if channel == "phone":
            base -= 0.05  # assume human confirmation reduces risk slightly

        score = min(max(base, 0), 0.99)

        explanation = [
            f"Lead time influence: {math.ceil(random.random() * 10)} days since booking.",
            f"Channel adjustment ({channel}).",
            f"Appointment type: {appointment_type}.",
        ]
        key = appointment_id or patient_id
        self.last_explanations[key] = explanation
        return score

    async def predict_no_show_risk_from_id(self, appointment_id: str) -> float:
        seed = hash(appointment_id) % 1_000_000
        random.seed(seed)
        score = 0.4 + (random.random() * 0.4)
        self.last_explanations[appointment_id] = [
            "History of late cancellations.",
            "Long travel distance detected.",
            "Preferred morning appointments unavailable.",
        ]
        return min(max(score, 0), 0.99)
