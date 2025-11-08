from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class ReminderCreate(BaseModel):
    appointment_id: str
    patient_id: str
    channel: Literal["sms", "email", "push"]
    send_at: datetime
    template_id: str
    high_risk: bool = Field(default=False)
    additional_context: Optional[str] = None


class ReminderResponse(BaseModel):
    reminder_id: str
    status: Literal["scheduled", "sent", "error"]
    message: Optional[str] = None
