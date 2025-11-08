from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from ..schemas.reminders import ReminderCreate, ReminderResponse


class ReminderService:
    """
    Handles orchestration of multi-channel reminder delivery.
    Currently uses mocked delivery outcomes until comms providers are wired up.
    """

    async def schedule_reminder(self, payload: ReminderCreate) -> ReminderResponse:
        reminder_id = str(uuid4())
        now = datetime.utcnow()
        status = "scheduled" if payload.send_at >= now else "sent"
        message = (
            "Reminder scheduled for dispatch."
            if status == "scheduled"
            else "Reminder dispatched immediately (past send_at)."
        )
        return ReminderResponse(reminder_id=reminder_id, status=status, message=message)
