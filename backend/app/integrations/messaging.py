from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from ..core.config import settings


@dataclass
class ReminderDispatch:
    reminder_id: str
    appointment_id: str
    patient_id: str
    channel: str
    send_at: datetime
    template_id: str
    high_risk: bool
    additional_context: str | None = None


class MessagingProvider(Protocol):
    async def enqueue(self, payload: ReminderDispatch) -> str:
        ...


class MockMessagingProvider:
    async def enqueue(self, payload: ReminderDispatch) -> str:  # pragma: no cover - simple side effects
        print(
            f"[MockMessaging] Scheduled reminder {payload.reminder_id} for patient {payload.patient_id} "
            f"via {payload.channel} at {payload.send_at.isoformat()} (template={payload.template_id})."
        )
        return payload.reminder_id


def get_messaging_provider() -> MessagingProvider:
    if settings.feature_flags.get("use_mock_messaging", True):
        return MockMessagingProvider()

    raise NotImplementedError("External messaging integration not configured.")
