from __future__ import annotations

from datetime import datetime, timedelta
from uuid import uuid4

from sqlmodel import Session

from ..schemas.scheduling import (
    AppointmentCreateRequest,
    AppointmentResponse,
    AppointmentSuggestion,
    AppointmentSuggestionRequest,
)
from ..models import Appointment
from ..integrations.ehr import BaseEHRClient, EHRAppointmentPayload, EHRSlotQuery
from .no_show_model import NoShowRiskModel


class SchedulingService:
    """
    Coordinates appointment scheduling logic including EHR integration
    and no-show risk scoring. Currently provides mocked behaviour until
    downstream systems are connected.
    """

    def __init__(
        self,
        session: Session,
        model: NoShowRiskModel | None = None,
        ehr_client: BaseEHRClient | None = None,
    ) -> None:
        self.session = session
        self.model = model or NoShowRiskModel()
        self.ehr_client = ehr_client

    async def schedule_appointment(self, payload: AppointmentCreateRequest) -> AppointmentResponse:
        """
        Schedule the appointment within the EHR and return status.

        TODO: Implement EHR integration and conflict resolution.
        """
        appointment = Appointment(
            id=str(uuid4()),
            patient_id=payload.patient_id,
            provider_id=payload.provider_id,
            reason_for_visit=payload.reason_for_visit,
            appointment_start=payload.appointment_start,
            appointment_end=payload.appointment_end,
            channel=payload.channel,
            insurance_plan=payload.insurance_plan,
            location_id=payload.location_id,
        )

        risk = await self.model.predict_no_show_risk(
            appointment_id=appointment.id,
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
        appointment.status = status
        appointment.no_show_risk = risk

        self.session.add(appointment)
        self.session.commit()
        self.session.refresh(appointment)

        if self.ehr_client is not None:
            await self.ehr_client.push_appointment(
                EHRAppointmentPayload(
                    appointment_id=appointment.id,
                    patient_id=appointment.patient_id,
                    provider_id=appointment.provider_id,
                    start=appointment.appointment_start,
                    end=appointment.appointment_end,
                    reason=appointment.reason_for_visit,
                    location_id=appointment.location_id,
                )
            )

        return AppointmentResponse(
            appointment_id=appointment.id,
            status=status,
            no_show_risk=risk,
            message=message,
        )

    async def suggest_appointments(
        self, payload: AppointmentSuggestionRequest
    ) -> list[AppointmentSuggestion]:
        """
        Generate personalised slot suggestions using historical preferences.

        TODO: Replace with search across actual provider calendars.
        """
        base_time = datetime.utcnow().replace(hour=9, minute=0, second=0, microsecond=0)

        slots: list[AppointmentSuggestion] = []
        if self.ehr_client is not None:
            query = EHRSlotQuery(
                provider_id=payload.previous_provider_id,
                visit_type=payload.visit_type,
                start_after=base_time,
                end_before=base_time + timedelta(days=14),
            )
            ehr_slots = await self.ehr_client.get_available_slots(query)
            for slot in ehr_slots:
                slots.append(
                    AppointmentSuggestion(
                        provider_id=slot.provider_id,
                        slot_start=slot.slot_start,
                        slot_end=slot.slot_end,
                        location_id=slot.location_id,
                        visit_type=payload.visit_type or "general_consult",
                        confidence=0.75,
                        personalization_reason="Recommended by availability feed.",
                    )
                )

        if slots:
            return slots[:5]

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
