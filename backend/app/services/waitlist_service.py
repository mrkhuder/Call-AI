from __future__ import annotations

from datetime import datetime, timedelta
from uuid import uuid4

from sqlmodel import Session, select

from ..schemas.waitlist import WaitlistEntry, WaitlistNotification
from ..models import Waitlist


class WaitlistService:
    """
    Automates waitlist prioritisation and slot notifications.
    Current implementation is in-memory mock logic.
    """

    def __init__(self, session: Session) -> None:
        self.session = session

    async def register_entry(self, payload: WaitlistEntry) -> str:
        entry = Waitlist(
            id=str(uuid4()),
            patient_id=payload.patient_id,
            visit_type=payload.visit_type,
            preferred_locations=",".join(payload.preferred_locations) if payload.preferred_locations else None,
            preferred_time_windows=",".join(
                f"{window[0]}-{window[1]}" for window in payload.preferred_time_windows
            )
            if payload.preferred_time_windows
            else None,
            risk_score=payload.risk_score,
            added_at=payload.added_at,
        )
        self.session.add(entry)
        self.session.commit()
        self.session.refresh(entry)
        return entry.id

    async def generate_notification(self, entry: WaitlistEntry) -> WaitlistNotification:
        slot_start = datetime.utcnow() + timedelta(hours=4)
        slot_end = slot_start + timedelta(minutes=30)
        expires_at = slot_start + timedelta(minutes=15)

        stored_entry = self.session.exec(
            select(Waitlist).where(Waitlist.patient_id == entry.patient_id).order_by(Waitlist.created_at.desc())
        ).first()

        preferred_locations = entry.preferred_locations
        if stored_entry and stored_entry.preferred_locations:
            preferred_locations = [loc.strip() for loc in stored_entry.preferred_locations.split(",") if loc]

        message = (
            f"Hi {entry.patient_id}, a {entry.visit_type} slot just opened at "
            f"{slot_start.strftime('%I:%M %p')}. Reply within 15 minutes to confirm."
        )

        return WaitlistNotification(
            slot_start=slot_start,
            slot_end=slot_end,
            location_id=preferred_locations[0] if preferred_locations else "loc-1",
            expires_at=expires_at,
            message=message,
        )
