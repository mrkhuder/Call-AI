from __future__ import annotations

from collections import defaultdict
from datetime import date, timedelta
from random import randint

from ..schemas.analytics import DemandForecastResponse, NoShowRiskScore
from .no_show_model import NoShowRiskModel


class AnalyticsService:
    """
    Provides analytics endpoints including no-show risk explanations and
    demand forecasting. Uses placeholder heuristics awaiting real data pipelines.
    """

    def __init__(self, model: NoShowRiskModel | None = None) -> None:
        self.model = model or NoShowRiskModel()

    async def no_show_score(self, appointment_id: str) -> NoShowRiskScore:
        risk = await self.model.predict_no_show_risk_from_id(appointment_id)
        tier = "low"
        if risk >= 0.8:
            tier = "critical"
        elif risk >= 0.6:
            tier = "high"
        elif risk >= 0.4:
            tier = "medium"

        top_factors = self.model.last_explanations.get(appointment_id, ["insufficient history"])

        return NoShowRiskScore(
            appointment_id=appointment_id,
            risk_score=risk,
            risk_tier=tier,
            top_factors=top_factors,
        )

    async def demand_forecast(self, specialty: str, horizon_days: int = 7) -> list[DemandForecastResponse]:
        today = date.today()
        forecasts: list[DemandForecastResponse] = []

        # Placeholder seasonal pattern logic
        seasonal_modifier = defaultdict(lambda: 1.0, {"pediatrics": 1.2, "dermatology": 0.8, "cardiology": 1.1})

        for offset in range(horizon_days):
            target_day = today + timedelta(days=offset)
            base = 20 + randint(-3, 3)  # replace with model inference
            demand = int(base * seasonal_modifier[specialty.lower()])
            lower = max(demand - 5, 0)
            upper = demand + 7
            forecasts.append(
                DemandForecastResponse(
                    specialty=specialty,
                    date=target_day,
                    expected_demand=demand,
                    confidence_interval=(lower, upper),
                )
            )
        return forecasts
