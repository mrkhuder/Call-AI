from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class WaitlistEntry(BaseModel):
    patient_id: str
    visit_type: str
    preferred_locations: list[str] = Field(default_factory=list)
    preferred_time_windows: list[tuple[str, str]] = Field(
        default_factory=list, description="List of preferred HH:MM 24h time windows."
    )
    risk_score: Optional[float] = Field(default=None, ge=0, le=1)
    added_at: datetime


class WaitlistNotification(BaseModel):
    slot_start: datetime
    slot_end: datetime
    location_id: str
    expires_at: datetime
    message: str
