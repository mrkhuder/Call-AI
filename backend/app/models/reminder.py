from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlmodel import Field, SQLModel


class Reminder(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, index=True)
    appointment_id: str = Field(index=True)
    patient_id: str = Field(index=True)
    channel: str = Field(index=True)
    send_at: datetime
    template_id: str
    high_risk: bool = Field(default=False)
    additional_context: Optional[str] = None
    status: str = Field(default="scheduled")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def touch(self) -> None:
        self.updated_at = datetime.utcnow()
