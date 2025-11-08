from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlmodel import Field, SQLModel


class Appointment(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, index=True)
    patient_id: str = Field(index=True)
    provider_id: str = Field(index=True)
    reason_for_visit: str
    appointment_start: datetime
    appointment_end: datetime
    channel: str
    insurance_plan: Optional[str] = None
    location_id: Optional[str] = None
    status: str = Field(default="pending", index=True)
    no_show_risk: Optional[float] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def touch(self) -> None:
        self.updated_at = datetime.utcnow()
