from __future__ import annotations

from datetime import datetime, timedelta
from uuid import uuid4

from ..schemas.waitlist import WaitlistEntry, WaitlistNotification


class WaitlistService:
    """
    Automates waitlist prioritisation and slot notifications.
    Current implementation is in-memory mock logic.
    """

    async def register_entry(self, payload: WaitlistEntry) -> str:
        # TODO: Persist entry to datastore and integrate with patient comms.
        return str(uuid4())

    async def generate_notification(self, entry: WaitlistEntry) -> WaitlistNotification:
        slot_start = datetime.utcnow() + timedelta(hours=4)
        slot_end = slot_start + timedelta(minutes=30)
        expires_at = slot_start + timedelta(minutes=15)

        message = (
            f"Hi {entry.patient_id}, a {entry.visit_type} slot just opened at "
            f"{slot_start.strftime('%I:%M %p')}. Reply within 15 minutes to confirm."
        )

        return WaitlistNotification(
            slot_start=slot_start,
            slot_end=slot_end,
            location_id=entry.preferred_locations[0] if entry.preferred_locations else "loc-1",
            expires_at=expires_at,
            message=message,
        )
