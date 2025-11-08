from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlmodel import Session

from ..schemas.reminders import ReminderCreate, ReminderResponse
from ..models import Reminder
from ..integrations.messaging import MessagingProvider, ReminderDispatch


class ReminderService:
    """
    Handles orchestration of multi-channel reminder delivery.
    Currently uses mocked delivery outcomes until comms providers are wired up.
    """

    def __init__(self, session: Session, messaging_provider: MessagingProvider | None = None) -> None:
        self.session = session
        self.messaging_provider = messaging_provider

    async def schedule_reminder(self, payload: ReminderCreate) -> ReminderResponse:
        reminder = Reminder(
            id=str(uuid4()),
            appointment_id=payload.appointment_id,
            patient_id=payload.patient_id,
            channel=payload.channel,
            send_at=payload.send_at,
            template_id=payload.template_id,
            high_risk=payload.high_risk,
            additional_context=payload.additional_context,
        )

        now = datetime.utcnow()
        status = "scheduled" if payload.send_at >= now else "sent"
        message = (
            "Reminder scheduled for dispatch."
            if status == "scheduled"
            else "Reminder dispatched immediately (past send_at)."
        )
        reminder.status = status

        self.session.add(reminder)
        self.session.commit()
        self.session.refresh(reminder)

        if self.messaging_provider is not None:
            await self.messaging_provider.enqueue(
                ReminderDispatch(
                    reminder_id=reminder.id,
                    appointment_id=reminder.appointment_id,
                    patient_id=reminder.patient_id,
                    channel=reminder.channel,
                    send_at=reminder.send_at,
                    template_id=reminder.template_id,
                    high_risk=reminder.high_risk,
                    additional_context=reminder.additional_context,
                )
            )

        return ReminderResponse(reminder_id=reminder.id, status=status, message=message)
