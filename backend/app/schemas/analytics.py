from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field


class NoShowRiskScore(BaseModel):
    appointment_id: str
    risk_score: float = Field(ge=0, le=1)
    risk_tier: str
    top_factors: list[str] = Field(default_factory=list)


class DemandForecastResponse(BaseModel):
    specialty: str
    date: date
    expected_demand: int = Field(ge=0)
    confidence_interval: tuple[int, int]
