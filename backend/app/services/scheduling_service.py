from __future__ import annotations

from datetime import datetime, timedelta
from uuid import uuid4

from ..schemas.scheduling import (
    AppointmentCreateRequest,
    AppointmentResponse,
    AppointmentSuggestion,
    AppointmentSuggestionRequest,
)
from .no_show_model import NoShowRiskModel


class SchedulingService:
    """
    Coordinates appointment scheduling logic including EHR integration
    and no-show risk scoring. Currently provides mocked behaviour until
    downstream systems are connected.
    """

    def __init__(self, model: NoShowRiskModel | None = None) -> None:
        self.model = model or NoShowRiskModel()

    async def schedule_appointment(self, payload: AppointmentCreateRequest) -> AppointmentResponse:
        """
        Schedule the appointment within the EHR and return status.

        TODO: Implement EHR integration and conflict resolution.
        """
        appointment_id = str(uuid4())
        risk = await self.model.predict_no_show_risk(
            appointment_id=appointment_id,
            patient_id=payload.patient_id,
            appointment_start=payload.appointment_start,
            appointment_type=payload.reason_for_visit,
            channel=payload.channel,
        )

        status = "confirmed" if risk < 0.7 else "pending"
        message = (
            "Appointment confirmed."
            if status == "confirmed"
            else "Appointment pending coordinator review due to high no-show risk."
        )

        return AppointmentResponse(
            appointment_id=appointment_id, status=status, no_show_risk=risk, message=message
        )

    async def suggest_appointments(
        self, payload: AppointmentSuggestionRequest
    ) -> list[AppointmentSuggestion]:
        """
        Generate personalised slot suggestions using historical preferences.

        TODO: Replace with search across actual provider calendars.
        """
        base_time = datetime.utcnow().replace(hour=9, minute=0, second=0, microsecond=0)
        suggestions = []
        for offset in range(3):
            slot_start = base_time + timedelta(days=offset, hours=offset)
            slot_end = slot_start + timedelta(minutes=30)
            suggestions.append(
                AppointmentSuggestion(
                    provider_id=payload.previous_provider_id or "provider-123",
                    slot_start=slot_start,
                    slot_end=slot_end,
                    location_id=payload.location_preferences[0] if payload.location_preferences else "loc-1",
                    visit_type=payload.visit_type or "general_consult",
                    confidence=max(0.5, 0.9 - offset * 0.1),
                    personalization_reason="Matches your usual {day} {time} preference.".format(
                        day=slot_start.strftime("%A"), time=slot_start.strftime("%I:%M %p")
                    ),
                )
            )
        return suggestions
