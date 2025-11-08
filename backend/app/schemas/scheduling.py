from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal, Optional

from pydantic import BaseModel, Field


class AppointmentCreateRequest(BaseModel):
    patient_id: Annotated[str, Field(min_length=1)]
    provider_id: Annotated[str, Field(min_length=1)]
    reason_for_visit: Annotated[str, Field(min_length=3)]
    appointment_start: datetime
    appointment_end: datetime
    channel: Literal["mobile", "web", "phone"]
    insurance_plan: Optional[str] = None
    location_id: Optional[str] = None
    metadata: dict[str, str | int | float | bool | None] = Field(default_factory=dict)


class AppointmentResponse(BaseModel):
    appointment_id: str
    status: Literal["confirmed", "pending", "waitlisted"]
    no_show_risk: Optional[float] = Field(default=None, ge=0, le=1)
    message: Optional[str] = None


class AppointmentSuggestionRequest(BaseModel):
    patient_id: Annotated[str, Field(min_length=1)]
    preferred_days: list[str] = Field(default_factory=list, description="Weekday names or ISO dates.")
    preferred_time_window: Optional[tuple[str, str]] = None
    visit_type: Optional[str] = None
    previous_provider_id: Optional[str] = None
    location_preferences: list[str] = Field(default_factory=list)


class AppointmentSuggestion(BaseModel):
    provider_id: str
    slot_start: datetime
    slot_end: datetime
    location_id: str
    visit_type: str
    confidence: float = Field(ge=0, le=1)
    personalization_reason: Optional[str] = None
