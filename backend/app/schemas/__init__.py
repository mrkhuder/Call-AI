"""Pydantic schemas for CareFlow AI."""

from .analytics import DemandForecastResponse, NoShowRiskScore
from .reminders import ReminderCreate, ReminderResponse
from .scheduling import (
    AppointmentCreateRequest,
    AppointmentResponse,
    AppointmentSuggestion,
    AppointmentSuggestionRequest,
)
from .waitlist import WaitlistEntry, WaitlistNotification

__all__ = [
    "AppointmentCreateRequest",
    "AppointmentResponse",
    "AppointmentSuggestionRequest",
    "AppointmentSuggestion",
    "ReminderCreate",
    "ReminderResponse",
    "WaitlistEntry",
    "WaitlistNotification",
    "NoShowRiskScore",
    "DemandForecastResponse",
]
