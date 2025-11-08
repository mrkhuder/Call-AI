from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlmodel import Field, SQLModel


class Waitlist(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, index=True)
    patient_id: str = Field(index=True)
    visit_type: str
    preferred_locations: Optional[str] = Field(default=None, description="Comma-separated list.")
    preferred_time_windows: Optional[str] = Field(default=None, description="Comma-separated HH:MM-HH:MM ranges.")
    risk_score: Optional[float] = Field(default=None)
    added_at: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def touch(self) -> None:
        self.updated_at = datetime.utcnow()
